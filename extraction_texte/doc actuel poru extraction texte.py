!pip install rdflib
from transformers import pipeline

triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')





# We need to use the tokenizer manually since we need special tokens.
#extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor("Punta Cana is a resort town in the municipality of Higuey, in La Altagracia Province, the eastern most province of the Dominican Republic", return_tensors=True, return_text=False)[0]["generated_token_ids"]])

#print(extracted_text[0])

# Function to parse the generated text and extract the triplets
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets
#extracted_triplets = extract_triplets(extracted_text[0])
#print(extracted_triplets)


import requests

def get_books_data(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def display_first_book_description(books_data):
    if 'items' in books_data and len(books_data['items']) > 0:
        first_book = books_data['items'][0]
        title = first_book['volumeInfo']['title']
        description = first_book['volumeInfo']['description']

        print(f"Title: {title}")
        print(f"Description: {description}")
    else:
        print("No books found.")

# Example usage
query = "harry potter"
books_data = get_books_data(query)
#le faire pour 10 oeuvre par ex
if books_data:
    display_first_book_description(books_data)


texteentier="Traduit de l’anglais par Nathalie Bru et Santiago Artozqui C’est l’une des images les plus marquantes du XXe siècle : deux jeunes garçons, deux princes, marchant derrière le cercueil de leur mère sous les regards éplorés – et horrifiés – du monde entier. Alors que Diana, princesse de Galles, rejoignait sa dernière demeure, des milliards de personnes se demandaient à quoi pouvaient bien penser les princes à cet instant, ce qu’ils ressentaient – et quelle tournure allait prendre leur vie désormais. Pour Harry, voici enfin venu le moment de raconter son histoire. Avant de perdre sa mère, le prince Harry, douze ans, était un enfant insouciant, un Suppléant rieur au côté d’un Héritier plus réservé. Le deuil a tout changé : difficultés à l’école, difficultés à gérer sa colère, à supporter la solitude – et, parce qu’il tenait la presse pour responsable de la mort de sa mère, difficultés à accepter que sa vie se déroule sous les feux des projecteurs. À vingt et un ans, il rejoint l’armée britannique. La discipline lui donne un cadre, et deux déploiements en opération extérieure font de lui un héros dans son pays. Bientôt pourtant, il se sent plus perdu que jamais, victime de stress post-traumatique et d’attaques de panique qui le paralysent. Par-dessus tout, il attend toujours le grand amour. Puis il rencontre Meghan. Le monde s’est passionné pour leur histoire d’amour digne d’Hollywood ; il s’est réjoui lors de leur mariage de conte de fées. Mais dès le début, Harry et Meghan sont harcelés par la presse, contraints de faire face, vague après vague, aux abus, au racisme et aux mensonges. Témoin des souffrances de sa femme, conscient du danger pour leur sécurité et leur santé mentale, Harry n’a pas trouvé meilleur moyen d’empêcher l’histoire de se répéter qu’en fuyant son pays natal. À travers les siècles, rares sont ceux qui ont osé quitter la famille royale. La dernière à avoir essayé, à vrai dire, fut sa mère... Pour la première fois, le prince Harry raconte sa propre histoire. D’une honnêteté brute et sans fard, Le Suppléant est un livre qui fera date, plein de perspicacité, de révélations, d’interrogations sur soi et de leçons durement apprises sur le pouvoir éternel de l’amour face au chagrin. Le prince Harry, duc de Sussex, est mari, père, acteur dans l’humanitaire et vétéran de guerre. Il milite pour l’écologie et s’engage pour la sensibilisation au bien-être mental. Il vit à Santa Barbara, en Californie, avec sa famille et leurs trois chiens."

extracted_textentier = triplet_extractor.tokenizer.batch_decode([triplet_extractor(texteentier, return_tensors=True, return_text=False)[0]["generated_token_ids"]])
extracted_tripletsentier = extract_triplets(extracted_textentier[0])
print(extracted_textentier[0])
print(extracted_textentier)
print(extracted_tripletsentier)


import networkx as nx
G = nx.Graph()


for triplet in extracted_tripletsentier:
    head = triplet['head']
    tail = triplet['tail']
    edge_type = triplet['type']

    # Add nodes
    G.add_node(head)
    G.add_node(tail)

    # Add edge with the specified type
    G.add_edge(head, tail, type=edge_type)

# Print nodes and edges
print("Nodes:", G.nodes())
print("Edges:", G.edges(data=True))


import matplotlib.pyplot as plt


# Visualize the graph
plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

# Subplot 1
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold', ax=subax1)



# Display the graph
plt.show()

import rdflib
import urllib.parse

def create_rdf_from_graph(graph):
    # Create an RDF Graph
    rdf_graph = rdflib.Graph()

    # Iterate through nodes and add triples
    for node in graph.nodes():
        encoded_node = urllib.parse.quote(node.replace(" ", "_"))
        #rdf_graph.add((rdflib.URIRef(f"urn:node:{encoded_node}"), rdflib.RDF.type, rdflib.URIRef(f"urn:type:{node}")))
        # Add additional properties if needed

    # Iterate through edges and add triples
    for edge in graph.edges(data=True):
        encoded_subject = urllib.parse.quote(edge[1].replace(" ", "_"))
        encoded_predicate = urllib.parse.quote(edge[2]['type'].replace(" ", "_"))
        encoded_object = urllib.parse.quote(edge[0].replace(" ", "_"))
        subject = rdflib.URIRef(f"urn:node:{encoded_subject}")
        predicate = rdflib.URIRef(f"urn:edge:{encoded_predicate}")
        object_ = rdflib.URIRef(f"urn:node:{encoded_object}")
        rdf_graph.add((subject, predicate, object_))
        # Add additional properties if needed

    return rdf_graph

# Example usage
rdf_graph = create_rdf_from_graph(G)

# Print the RDF graph in N3 format
print(rdf_graph.serialize(format='n3'))
# Save the RDF graph to a file
# rdf_graph.serialize(destination='output.rdf', format='xml')


import spacy
from spacy.cli.download import download

# Télécharger le modèle français
download('fr_core_news_sm')




import spacy

def extraction_personnes(texte):
    # Charger le modèle linguistique en français
    nlp = spacy.load('fr_core_news_sm')

    # Analyser le texte
    doc = nlp(texte)

    # Filtrer et afficher les entités de type "PERSON"
    personnes = set()
    for entite in doc.ents:
        if entite.label_ == "PER" and len(entite.text) > 2:  # Exclure les entités avec une seule lettre et une apostrophe
            personnes.add(entite.text)

    # Afficher les personnes
    if personnes:
        print("Personnes identifiées :")
        for personne in personnes:
            print(personne)
    else:
        print("Aucune personne identifiée dans le texte.")
    return personnes

# Exemple d'utilisation

entite=extraction_personnes(texteentier)



from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import FOAF

def creer_document_rdf(personnes):
    # Créer un graph RDF
    g = Graph()

    # Définir une namespace pour les entités et propriétés
    ex = Namespace("http://example.org/")
    sujet_book = ex["Book"]  # Créer un sujet pour le livre associé
    g.add((sujet_book, RDF.type, ex.Book))
    # Ajouter des triples pour chaque personne identifiée
    for personne in personnes:
        sujet_per = ex[personne.replace(" ", "_")]  # Utiliser le nom de la personne comme sujet
        sujet_book = ex["Book"]  # Créer un sujet pour le livre associé

        # Ajouter des triplets pour l'entité Personne
        g.add((sujet_per, RDF.type, FOAF.Person))
        g.add((sujet_per, FOAF.name, Literal(personne)))


        # Ajouter des triplets pour l'entité Book

        g.add((sujet_book, ex.hasCharacter, sujet_per))

    return g

graphentite=creer_document_rdf(entite)
print(graphentite.serialize(format='n3'))
