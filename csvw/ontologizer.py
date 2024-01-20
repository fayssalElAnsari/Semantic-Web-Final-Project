def format_category_name(category):
    """Format the category name into a valid OWL class name."""
    return category.replace(' ', '').replace('(', '').replace(')', '').replace('&', 'And')

def create_ontology_from_categories(input_file, output_file, base_ontology):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Write the base ontology to the output file
        outfile.write(base_ontology + "\n")

        # Process each category
        for line in infile:
            category = line.strip()
            if category:
                formatted_category = format_category_name(category)
                class_definition = f"""
myonto:{formatted_category} a owl:Class ;
    rdfs:subClassOf myonto:Category ;
    rdfs:label "{category}"@en ;
    rdfs:comment "Category representing {category}."@en .
"""
                outfile.write(class_definition)

    print(f"OWL ontology with categories saved to '{output_file}'")

if __name__ == "__main__":
    # Base ontology content
    base_ontology = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbo: <http://dbpedia.org/ontology/>.
@prefix dbr: <http://dbpedia.org/resource/>.
@prefix myonto: <http://myonto.org/myonto_schema#> .
    """

    create_ontology_from_categories('unique_categories.txt', 'categories.owl', base_ontology)
