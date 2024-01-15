## TODO

- [x] chosir un domaine (la literrature par exemple, Le choix de l'ontologie doit se baser sur la possibilite de demontrer les fonctionalites owl et skos, la quantite des donnees sur internet sur le domaine choisis. Et si c'est gratuit)

- [ ] Cree une ontology, c'est dire les classes, sous-classes et toutes les relations entre eux, en utilisant owl, skos et rdfs
    **NOT NECESSARY TO PROVIDE AN EXAMPLE OF EACH ONE**
    - [ ] RDFS Entailments
        - [x] rdfs:label
        - [x] rdfs:subClassOf
        - [x] rdfs:domain
        - [x] rdfs:range
        - [ ] rdfs:Resource
        - [ ] rdfs:subPropertyOf
        - [ ] rdfs:ContainerMembershipProperty
        - [ ] 

    - [ ] owl
        - [x] owl:ObjectProperty
        - [x] owl:DatatypeProperty
        - [x] owl:AnnotationProperty
        - [ ] owl:SymmetricProperty
        - [ ] owl:AsymmetricProperty
        - [x] owl:inverseOf
        - [ ] owl:TransitiveProperty
        - [ ] owl:propertyDisjointWith
        - [ ] owl:ReflexiveProperty
        - [ ] owl:IrreflexiveProperty
        - [ ] owl:propertyChainAxiom
        - [x] owl:FunctionalProperty
        - [ ] owl:InverseFunctionalProperty
        - [ ] owl:oneOf
        - [ ] owl:unionOf
        - [ ] owl:intersectionOf
        - [ ] owl:complementOf
        - [ ] owl:disjointWith
        - [x] owl:AllDisjointClasses
        - [ ] owl:disjointUnionOf
        - [x] owl:equivalentClass
        - [ ] owl:equivalentProperty
        - [ ] owl:sameAs
        - [ ] owl:differentFrom
        - [x] owl:hasKey
        - [ ] owl:onProperty
        - [ ] owl:allValuesFrom
        - [ ] owl:someValuesFrom
        - [ ] owl:hasValue
        - [ ] owl:hasSelf
        - [ ] owl:maxCardinality
        - [ ] owl:qualifiedCardinality
        - [ ] owl:priorVersion
        - [ ] owl:imports
        - [ ] owl:DeprecatedProperty
        - [ ] owl:DeprecatedClass

    - [ ] SHACL
        - [ ] sh:NodeShape
        - [ ] sh:targetClass
        - [ ] sh:property
            - [ ] sh:path
            - [ ] sh:dataType
            - [ ] sh:minCount
            - [ ] sh:maxCount
        - [ ] sh:targetSubjectsOf
        - [ ] sh:targetObjectsOf
        - [ ] sh:oneOrMorePath
        - [ ] sh:alternativePath
        - [ ] sh:nodeKind
        - [ ] ...



- [ ] enrichir l'ontology a l'aide des regles d'inference SPARQL. (Est ce qu'on peut utiliser protege pour faire ca automatiquement?)
- [ ] ajouter des contraintes SHACL pour valider les donnees 
- [ ] utiliser les techniques d'extraction d'information pour consruire un graph de connaisance (rebel)
- [x] enrichir le graphe de connaissance (csv2rdf)
- [x] relier les donnees locales avec les donnees externes 
    - [x] map isbn
- [ ] requettes sparql (une requette pour chaque principe appris)
- [ ] requettes SPARQL federees
    - [ ] 
- [ ] graph embeddings
- [ ] interface pour demo
    - [ ] serveur html

Rendu du projet le **23/01 à 9h** et soutenances le 23/01 après-midi

L'objectif du projet est de concevoir et de mettre en œuvre de bout en bout une application innovante qui réponde à un cas d’usage, basée sur les éléments suivants :

    Modélisation ontologique en OWL et SKOS en fonction du type des données. Celle-ci doit être conçue et réalisée spécifiquement pour les données du projet par chaque étudiant ou équipe (ne pas réutiliser un vocabulaire existant). Elle peut être enrichie par une base de règles d'inférence implémentées avec SPARQL.


    Caractérisation de la structure du graphe de connaissances attendu par un ensemble de contraintes SHACL (possiblement incluant des contraintes de respect des définitions des classes de l’ontologie).


    Population de l'ontologie (création et description d'instances) et/ou alimentation du thésaurus :


        Construire un graphe de connaissances à partir de données non structurées (textes) disponibles sur le web et pouvant être relatives à un ou plusieurs sujets d'intérêt pour l'application. Ceci en appliquant les techniques d'extraction de l'information (IE) les plus convenables et adaptées parmi celles étudiées, allant des techniques manuelles aux modèles de langage avancés comme les transformers et LLMs.


        Enrichissement du graphe de connaissances à l’aide de données structurées : données liftées depuis le format CSV avec csv2rdf, données d'une API web liftées avec un SPARQL micro-service, de la même manière que ce qui a été réalisé lors des sessions de TDs. Vous pouvez réutiliser des données utilisées lors du TDs (csv et AP web), mais le modèle ontologique cible doit être celui que vous avez défini dans ce projet, à la différence des TDs.


    Toutes les données RDF extraites à partir des données hétérogènes structurées et non structurées doivent être intégrées selon le modèle ontologique.


    Alignement (manuel ou automatique) de votre ontologie et thésaurus avec des vocabulaires du web de données liées (e.g. ontologie DBpedia, Wikidata, Schema.org …), et liage (manuel ou automatique) de vos données avec des ressources sur le web de données liées (e.g. DBpedia, WikiData,…).


    Exploitation du graphe de connaissances :


        Implémentation de questions de compétences avec des requêtes SPARQL (complexes et intéressantes): les principales fonctionnalités de l'application doivent être implémentées avec des requêtes SPARQL appliquées au graphe construit.


        Certaines requêtes SPARQL fédérées (clause SERVICE) doivent utiliser le dataset local (issu du texte + CSV), le SPARQL micro-service, et un ou plusieurs autres endpoints du web de données


        Optionnel : implémentation d’une question de compétences en calculant des graph embeddings et mettant en œuvre un algo de ML.


    L'application doit avoir une interface (minimale) pour communiquer avec ses utilisateurs cibles, illustrant le cas d’usage. Il est recommandé d'utiliser une interface web, mais d'autres interfaces (e.g. en ligne de commande) peuvent être acceptées. Dans tous les cas, cette partie est démonstrative, mais ne doit pas vous demander beaucoup de temps comparé au reste du projet.

Vous devez rédiger un rapport et préparer une présentation orale avec démo décrivant le cas d'usage considéré, les spécifications de votre application, votre modélisation, votre graphe de connaissances, la façon dont vous l'avez construit à partir de sources hétérogènes, les fonctionnalités/questions de compétence implémentées.
