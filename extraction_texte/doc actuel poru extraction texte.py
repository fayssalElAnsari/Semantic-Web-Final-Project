from transformers import pipeline
import networkx as nx
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import matplotlib.pyplot as plt
import requests
import networkx as nx
from rdflib import Graph, URIRef, Literal, Namespace


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
        return description
    else:
        print("No books found.")

triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')
def triple(text):
  sentences = text.split("\n")
  sentences_predicted_triplets = []

  for sentence in sentences:
    predicted_triplet = triplet_extractor.tokenizer.batch_decode([triplet_extractor(sentence, return_tensors=True, return_text=False)[0]["generated_token_ids"]])
    sentences_predicted_triplets.append(predicted_triplet)
  print(sentences_predicted_triplets)
  return sentences_predicted_triplets




def generate_graph(triplets):
  graph = nx.Graph()
  i = 0
  for triplet in triplets:
      subject = triplet["head"]
      predicate = triplet["type"]
      attribut = triplet["tail"]
      if subject not in graph.nodes:
        graph.add_node(subject)
      if attribut not in graph.nodes:
        graph.add_node(attribut)
      graph.add_edge(subject,attribut,label=predicate)

  plt.figure(figsize=(12,12))
  pos = nx.kamada_kawai_layout(graph)
  labels = nx.get_edge_attributes(graph, 'label')
  nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue", font_color="black")
  nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
  #plt.show()
  return graph


def fullpipelinetograph(que):
  
  books_data = get_books_data(que)
  text=display_first_book_description(books_data)
  sentences_predicted_triplets=triple(text)
  triplets = []
  for sentence_predicted_triplets in sentences_predicted_triplets:
    for sentence_predicted_triplet in sentence_predicted_triplets:
      triplets += extract_triplets(sentence_predicted_triplet)
  for triplet in triplets:
    print(triplet["head"], triplet["type"], triplet["tail"])
  G = nx.Graph()
  graph=generate_graph(triplets)
  return graph

query = "harry potter and the cursed child"
graph1=fullpipelinetograph(query)

q2="harry poter and the half-blood prince"
graphe2=fullpipelinetograph(q2)

q3="The Ultimate Hitchhikers Guide to the Galaxy"
graphe3=fullpipelinetograph(q3)

q4="The Changeling Sea"
graphe4=fullpipelinetograph(q4)

q5="Bill Brysons African Diary"
graphe5=fullpipelinetograph(q5)

q6="In a Sunburned Country"
graphe6=fullpipelinetograph(q6)

q7="Neither Here nor There A Travels in Europe"
graphe7=fullpipelinetograph(q7)

q8="Notes from a Small Island"
graphe8=fullpipelinetograph(q8)

q9="The Lord of the Rings A Weapons and Warfare"
graphe9=fullpipelinetograph(q9)

#q10="Hatchet Jobs A% Writings on Contemporary Fiction"
#graphe10=fullpipelinetograph(q10)




def generate_rdf(graph, livre_value="X"):
    rdf_graph = Graph()

    # Définir une base de l'espace de noms pour vos entités
    base_ns = Namespace("http://myonto.org/")
    schema = Namespace("http://myonto.org/myonto_schema/")
    rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    # Ajouter un objet "livre" avec des relations "contient" avec toutes les nodes du graph
    livre_uri = base_ns[livre_value]
    rdf_graph.add((livre_uri, rdf["type"], schema["Book"]))
    
    for node in graph.nodes:
        # Remplacez les espaces par des underscores dans les valeurs des nœuds
        sanitized_node_value = node.replace(" ", "_")
        rdf_graph.add((base_ns[sanitized_node_value], rdf["type"], schema["ElementsImportant"]))
        
        # Ajoutez le champ "livre" avec la valeur spécifiée
        rdf_graph.add((base_ns[sanitized_node_value], schema["IsInBook"], livre_uri))
        
        # Ajoutez une relation "contient" entre le livre et chaque node du graph
        rdf_graph.add((livre_uri, schema["Content"], base_ns[sanitized_node_value]))

    for edge in graph.edges(data=True):
        subject, attribut, predicate = edge
        # Remplacez les espaces par des underscores dans les valeurs des arêtes et des prédicats
        sanitized_subject = subject.replace(" ", "_")
        sanitized_attribut = attribut.replace(" ", "_")
        sanitized_predicate = predicate["label"].replace(" ", "_")
        rdf_graph.add((base_ns[sanitized_subject], schema[sanitized_predicate], base_ns[sanitized_attribut]))

    return rdf_graph

rdf_graph = generate_rdf(graph1, livre_value="Harry%20Potter%20and%20the%20Cursed%20Child")
rdf_graph2 = generate_rdf(graphe2, livre_value="Harry%20Potter%20and%20the%20Half-Blood%20Prince%20%28Harry%20Potter%20%20%236%29")
rdf_graph3 = generate_rdf(graphe3, livre_value="The%20Ultimate%20Hitchhikers%20Guide%20to%20the%20Galaxy")
rdf_graph4 = generate_rdf(graphe4, livre_value="The%20Changeling%20Sea")
rdf_graph5 = generate_rdf(graphe5, livre_value="Bill%20Brysons%20African%20Diary")
rdf_graph6 = generate_rdf(graphe6, livre_value="In%20a%20Sunburned%20Country")
rdf_graph7 = generate_rdf(graphe7, livre_value="Neither%20Here%20nor%20There%20A%20Travels%20in%20Europe")
rdf_graph8 = generate_rdf(graphe8, livre_value="Notes%20from%20a%20Small%20Island")
rdf_graph9 = generate_rdf(graphe9, livre_value="The%20Lord%20of%20the%20Rings%20A%20Weapons%20and%20Warfare")
#rdf_graph10 = generate_rdf(graphe10, livre_value="Hatchet%20Jobs%20A%%20Writings%20on%20Contemporary%20Fiction")
rdf_graph += rdf_graph2
rdf_graph += rdf_graph3
rdf_graph += rdf_graph4
rdf_graph += rdf_graph5
rdf_graph += rdf_graph6
rdf_graph += rdf_graph7
rdf_graph += rdf_graph8
rdf_graph += rdf_graph9
#rdf_graph += rdf_graph10
# Afficher le graph RDF
print(rdf_graph.serialize(format='n3'))
rdf_graph.serialize(destination='extractiontexte.ttl', format='turtle')
