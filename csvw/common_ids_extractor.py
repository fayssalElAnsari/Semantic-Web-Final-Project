import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
import requests
import xml.etree.ElementTree as ET

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

def query_custom_service(isbn, is_isbn10, base_url):
    url = f"{base_url}?keyword={isbn}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    isbn_predicate = "myonto:hasIsbn10" if is_isbn10 else "myonto:hasIsbn13"
    
    query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX myonto: <http://myonto.org/myonto_schema/>
        SELECT DISTINCT * WHERE {{
            ?serviceBook {isbn_predicate} "{isbn}".
            ?serviceBook myonto:hasIsbn13 ?serviceIsbn13.
            ?serviceBook myonto:googleBookLink ?googleBookLink.
            ?serviceBook myonto:hasCategory ?category.
            ?serviceBook myonto:name ?name.
        }} LIMIT 30
    """
    body = {'query': query}

    try:
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            #print(f"Response for ISBN {isbn}: {response.content}")  # Print the raw response content
            return response.content  # Return the raw XML content
        else:
            print(f"HTTP request failed for ISBN {isbn}: Status code {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error making HTTP request for ISBN {isbn}: {e}")
        return None

def parse_xml_response(xml_data):
    try:
        root = ET.fromstring(xml_data)
        categories = set()

        for result in root.findall('.//{http://www.w3.org/2005/sparql-results#}result'):
            category_binding = result.find('.//{http://www.w3.org/2005/sparql-results#}binding[@name="category"]')
            if category_binding is not None:
                category_uri = category_binding.find('.//{http://www.w3.org/2005/sparql-results#}uri')
                category_literal = category_binding.find('.//{http://www.w3.org/2005/sparql-results#}literal')

                if category_uri is not None:
                    categories.add(category_uri.text)
                elif category_literal is not None:
                    categories.add(category_literal.text)

        return categories

    except Exception as e:
        print(f"Error parsing XML response: {e}")
        return set()



# Main script
def main():
    ttl_file = 'books.ttl'  # Update with the path to your TTL file
    base_url = 'http://localhost/service/googleBooks/getBookByKeyword'  # Base URL of the custom service

    isbn10s, isbn13s = extract_isbns(ttl_file)

    if not (isbn10s or isbn13s):
        print("No ISBNs extracted. Exiting.")
        return

    with open('extracted_categories.txt', 'w') as file:
        for isbn in tqdm(isbn10s + isbn13s, desc="Processing ISBNs"):
            xml_response = query_custom_service(isbn, isbn in isbn10s, base_url)
            if xml_response:
                categories = parse_xml_response(xml_response)
                for category in categories:
                    file.write(f"{isbn}: {category}\n")
                    file.flush()

    print("Extracted categories saved to 'extracted_categories.txt'")

if __name__ == "__main__":
    main()