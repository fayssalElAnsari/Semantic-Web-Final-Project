import re

def extract_categories(owl_file):
    categories = []
    with open(owl_file, 'r') as file:
        for line in file:
            match = re.search(r'myonto:(\w+) a owl:Class ;', line)
            if match:
                categories.append(match.group(1))
    return categories

def write_sparql_query(categories, sparql_file):
    base_query = """
@prefix myonto: <http://myonto.org/myonto_schema/>
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
CONSTRUCT {
    ?bookUri rdf:type ?type;
        myonto:name ?title;
        myonto:hasPublisher ?publisher;
        myonto:description ?description;
        myonto:publishedDate ?publishedDate;
        myonto:language ?language;
        myonto:hasIsbn10 ?isbn10;
        myonto:hasIsbn13 ?isbn13;
        myonto:hasCategory ?categoryUri;
        myonto:googleBookLink ?googleBookLink;
        myonto:hasAuthor ?author.

    ?authorUri a myonto:Author;
        myonto:name ?author.
} WHERE {   
    ?book
        api:volumeInfo [api:title ?title];
        api:volumeInfo [api:authors ?author];
        #api:volumeInfo [api:description ?description];
        api:volumeInfo [api:industryIdentifiers [api:identifier ?isbn; api:type ?isbnType]];
        api:volumeInfo [api:printType ?printType];
        api:volumeInfo [api:categories ?apiCategories];
        api:volumeInfo [api:publishedDate ?publishedDate];
        api:volumeInfo [api:language ?language];
        api:volumeInfo [api:infoLink ?googleBookLink];
        api:id ?id;
        api:volumeInfo [api:publisher ?publisher].

    bind (IRI(concat("http://localhost/ld/googleBooks/book/", ?id)) AS ?bookUri )
    bind (IRI(concat("http://localhost/ld/googleBooks/author/", ?id)) AS ?authorUri )
    BIND (IF(?printType = "BOOK", myonto:Book, myonto:Magazine) AS ?type)
    BIND (IF(?isbnType = "ISBN_10", ?isbn, "") AS ?isbn10)
    BIND (IF(?isbnType = "ISBN_13", ?isbn, "") AS ?isbn13)
"""

    # Build the BIND clause for categories
    bind_clause = "BIND (\n"
    for i, category in enumerate(categories):
        if i > 0:
            bind_clause += "        IF("
        bind_clause += f"CONTAINS(LCASE(?apiCategories), \"{category.lower()}\"), myonto:{category}, "
        if i < len(categories) - 1:
            bind_clause += "\n"
    bind_clause += "?apiCategories)\n" * len(categories)
    bind_clause += "    ) AS ?categoryUri\n}\n"

    with open(sparql_file, 'w') as file:
        file.write(base_query + bind_clause)

    print(f"SPARQL query saved to '{sparql_file}'")

if __name__ == "__main__":
    categories = extract_categories('categories.owl')
    write_sparql_query(categories, 'construct.sparql')
