import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
import requests

def query_custom_service(isbn, base_url):
    url = f"{base_url}?keyword={isbn}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # Or response.json() based on the response format
    else:
        return None

# Function to read TTL file and extract ISBNs
def extract_isbns(ttl_file):
    try:
        g = rdflib.Graph()
        g.parse(ttl_file, format="ttl")

        isbn10_query = g.query("""
            SELECT DISTINCT ?isbn10 WHERE {
                ?book <http://myonto.org/myonto_schema/hasIsbn10> ?isbn10 .
            }
        """)

        isbn13_query = g.query("""
            SELECT DISTINCT ?isbn13 WHERE {
                ?book <http://myonto.org/myonto_schema/hasIsbn13> ?isbn13 .
            }
        """)

        isbn10s = [str(row[0]) for row in isbn10_query]
        isbn13s = [str(row[0]) for row in isbn13_query]

        return isbn10s, isbn13s

    except Exception as e:
        print(f"Error reading or parsing the TTL file: {e}")
        return [], []

# Function to run SPARQL query
def run_sparql_query(isbn, is_isbn10, base_endpoint_url):
    try:
        # Construct the full endpoint URL including the ISBN
        endpoint_url = f"{base_endpoint_url}?keyword={isbn}"
        sparql = SPARQLWrapper(endpoint_url)

        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX myonto: <http://myonto.org/myonto_schema/>
            SELECT DISTINCT * WHERE {
                  ?serviceBook myonto:hasIsbn10 ?serviceIsbn10.
                  ?serviceBook myonto:hasIsbn13 ?serviceIsbn13.
                  ?serviceBook myonto:googleBookLink ?googleBookLink.
                  ?serviceBook myonto:hasCategory ?category.
                  ?serviceBook myonto:name ?name.
            } LIMIT 30
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        if results["results"]["bindings"]:
            print(f"Results found for ISBN {isbn}")
            return True
        else:
            print(f"No results for ISBN {isbn}")
            return False

    except Exception as e:
        print(f"Error querying the SPARQL endpoint for ISBN {isbn}: {e}")
        return False

# Main script
# def main():
#     ttl_file = 'books_debug.ttl'  # Update with the path to your TTL file
#     endpoint_url = 'http://localhost/service/googleBooks/getBookByKeyword'  # Replace with your actual SPARQL endpoint URL

#     isbn10s, isbn13s = extract_isbns(ttl_file)

#     if not (isbn10s or isbn13s):
#         print("No ISBNs extracted. Exiting.")
#         return

#     with open('common_keywords.txt', 'w') as file:
#         for isbn in tqdm(isbn10s + isbn13s, desc="Processing ISBNs"):
#             if run_sparql_query(isbn, isbn in isbn10s, endpoint_url):
#                 file.write(f"{isbn}\n")
#                 file.flush()

#     print("Common keywords saved to 'common_keywords.txt'")

def main():
    ttl_file = 'books_debug.ttl'  # Update with the path to your TTL file
    base_url = 'http://localhost/service/googleBooks/getBookByKeyword'  # Base URL of the custom service

    isbn10s, isbn13s = extract_isbns(ttl_file)

    if not (isbn10s or isbn13s):
        print("No ISBNs extracted. Exiting.")
        return

    with open('common_keywords.txt', 'w') as file:
        for isbn in tqdm(isbn10s + isbn13s, desc="Processing ISBNs"):
            result = query_custom_service(isbn, base_url)
            if result:
                file.write(f"{isbn}\n")
                file.flush()
                print(f"ISBN {isbn} written to file.")
            else:
                print(f"No valid response for ISBN {isbn}.")

    print("Common keywords saved to 'common_keywords.txt'")

if __name__ == "__main__":
    main()
