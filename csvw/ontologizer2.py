import rdflib
import re

def load_ontology(file_path):
    g = rdflib.Graph()
    try:
        g.parse(file_path, format='turtle')
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:  # Replace 'ISO-8859-1' with the correct encoding
            data = f.read()
        g.parse(data=data, format='turtle')
    return g


def find_classes_with_keywords(graph, keyword):
    classes = set()
    for s, p, o in graph:
        if p == rdflib.RDFS.label and keyword.lower() in o.lower():
            classes.add(s)
    return classes

def add_disjoint_relationships(graph, class_sets):
    for class_set in class_sets:
        for cls in class_set:
            for other_cls in class_set:
                if cls != other_cls:
                    graph.add((cls, rdflib.OWL.disjointWith, other_cls))

def save_ontology(graph, file_path):
    graph.serialize(destination=file_path, format='turtle')

if __name__ == "__main__":
    ontology_file = 'categories.owl'
    output_file = 'owl_class_properties.owl'

    g = load_ontology(ontology_file)

    # Example: Finding classes related to mythology and education
    mythology_classes = find_classes_with_keywords(g, 'mythology')
    education_classes = find_classes_with_keywords(g, 'education')

    # Adding disjoint relationships
    add_disjoint_relationships(g, [mythology_classes, education_classes])

    save_ontology(g, output_file)
