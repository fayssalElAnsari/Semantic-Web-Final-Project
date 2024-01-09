# COLLABORATORS
- Fayssal EL ANSARI.

# TODO
* [x] Choose `SPARQL` API microservice.
    - `Google's books API`
* [x] Create boilerplate code for `GoogleBooks micro-service`
* [x] create a first version `microservice`
    * [x] getBookById
        * [x] modify config.ini
        * [x] modify construct.sparql
        * [x] modify profile.jsonId
    * [x] getBookByName
        * [x] modify config.ini
        * [x] modify construct.sparql
        * [x] modify profile.jsonId
* [ ] create a second version `microservice`
    * [ ] add more entities
    * [ ] add an actual id to every node representing a book in the graph
    * [ ] make the id clickable to download data in the form of `ttl` (just like in provided examples)
    * [ ] demo html page
* [x] Align data to a thrid party ontology (`schema.org`, `DBpedia` or wikidata...)
* [x] Choose `CSV` file.
    - file downloaded from `https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks`
* [x] learn to use `csv2rdf`
    * [x] set up ubuntu wsl on windows
    * [x] run the downlaoded csv2rdf with the provided files
    * [x] validate the produced .ttl filex
* [x] Lift the `CSV` file using a CSVW mapping and a chosen tool.
    - [x] download `csv2rdf` from realeases page
    - [x] make `run.sh` file
    - [x] create a `metadata.json` file
    - [x] save output to `books.ttl`
* [x] Write a `SPARQL` federated query involving both data sources.

To be finished before the **05/01/2024**.

# PROJECT DESCRIPTION
The API we'll be working on is `Google's books API` https://developers.google.com/books/docs/v1/getting_started, a sample of its response is as follows, the first element of the items list:
```JSON
{
    "kind": "books#volume",
    "id": "buc0AAAAMAAJ",
    "etag": "Jb2BwbsTZIA",
    "selfLink": "https://www.googleapis.com/books/v1/volumes/buc0AAAAMAAJ",
    "volumeInfo": {
        "title": "Adventures of Sherlock Holmes",
        "authors": [
            "Sir Arthur Conan Doyle"
        ],
        "publisher": "Harper & Bros.",
        "publishedDate": "1892",
        "description": "Presenting 12 tales starring the legendary British detective Sherlock Holmes, this 1892 book is Arthur Conan Doyle's first short-story collection. The mystery compilation includes some of Holmes's finest cases with his dutiful sidekick, Doctor Watson, most notably \"A Scandal in Bohemia,\" in which Holmes matches wits with the crafty former lover of a European king. Also featured is \"The Adventure of the Red-Headed League,\" a study in misdirection that unfolds to become a much larger scheme. The stories, initially published in the Strand Magazine, are essential reading for Holmes fans.",
        "readingModes": {
            "text": true,
            "image": true
        },
        "pageCount": 307,
        "printedPageCount": 360,
        "dimensions": {
            "height": "20.00 cm"
        },
        "printType": "BOOK",
        "averageRating": 4.5,
        "ratingsCount": 485,
        "maturityRating": "NOT_MATURE",
        "allowAnonLogging": false,
        "contentVersion": "7.5.15.0.full.3",
        "panelizationSummary": {
            "containsEpubBubbles": false,
            "containsImageBubbles": false
        },
        "imageLinks": {
            "smallThumbnail": "http://books.google.com/books/content?id=buc0AAAAMAAJ&printsec=frontcover&img=1&zoom=5&edge=curl&imgtk=AFLRE71AsKhoBnnPtp7CDC6MFaf10pRUkJyfaxq_Zau6wZGcidUMSH1vMr3InAUatC8m8JDiP1OUpYWxA41up8N0VCWJZKiMJ9RgBMZz1ov-G1phK09NXu6tLGp81aYjEr9cNvhNpkvY&source=gbs_api",
            "thumbnail": "http://books.google.com/books/content?id=buc0AAAAMAAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70P15brdAFvkW5BNXFVWCvhyUIQMB5Ft0c0iZ0Mz4uW8Em5A6y0PqTmDVzzUkguOp_dyIUGIrHcflAvqRWeOFHxv8quoxN_8ZsbcoERifE-nrNjjZoQHJSS9aZD6dHBd9EybILO&source=gbs_api",
            "small": "http://books.google.com/books/content?id=buc0AAAAMAAJ&printsec=frontcover&img=1&zoom=2&edge=curl&imgtk=AFLRE715BROhKm0jhKBhgS5WC6-DdujLA5ATUT0pOf1BPxE6K4ECPQfGtnymPeWQI9yNeqi3pE4_CMAtZZVaR5M2R5N-KaMseAWjWhRQR72PSiv22Yb9NvD7VaAtddIivzfI4rPG98rD&source=gbs_api",
            "medium": "http://books.google.com/books/content?id=buc0AAAAMAAJ&printsec=frontcover&img=1&zoom=3&edge=curl&imgtk=AFLRE72ON1WnAm5Fz0YCRJSkXcZDVNvBCsXb7WBLeWwR4ZBAEgsN6FqBOHCRb_gJhNwvdekYTE3ZDwYShrWFci9n4HePArZmeS1hb31aQiOFXsxCJkvC9Zur0Q2vEr3IHy02ezoMf94a&source=gbs_api",
            "large": "http://books.google.com/books/content?id=buc0AAAAMAAJ&printsec=frontcover&img=1&zoom=4&edge=curl&imgtk=AFLRE72b5v-rjKpqJ9dLu203QHLO_mFNS6hOTlD1BQRmawyAqE9sVwS99DUyT7A7FM6sjzy_8qgC3tJkjHz-yNibxkLjxi3ElWJDvvEkf_cUUpn3rIMOEuwDtEYCu4b4Kov0RkJm1953&source=gbs_api",
            "extraLarge": "http://books.google.com/books/content?id=buc0AAAAMAAJ&printsec=frontcover&img=1&zoom=6&edge=curl&imgtk=AFLRE70CVyVAQvWDFwLMKSkFWa4DnhmJoECAi_p47IbRY4jRsQFo2c7WGydQmeAoovhDkQjzPqMmDQb214BPpHMlgGBYrGIxjTuRzJbmsEs7J9ruc92TE8jg2wrxEkoPLwrLSfADg79q&source=gbs_api"
        },
        "language": "en",
        "previewLink": "http://books.google.fr/books?id=buc0AAAAMAAJ&hl=&source=gbs_api",
        "infoLink": "https://play.google.com/store/books/details?id=buc0AAAAMAAJ&source=gbs_api",
        "canonicalVolumeLink": "https://play.google.com/store/books/details?id=buc0AAAAMAAJ"
    },
    "layerInfo": {
        "layers": [
            {
                "layerId": "geo",
                "volumeAnnotationsVersion": "28"
            }
        ]
    },
    "saleInfo": {
        "country": "FR",
        "saleability": "FREE",
        "isEbook": true,
        "buyLink": "https://play.google.com/store/books/details?id=buc0AAAAMAAJ&rdid=book-buc0AAAAMAAJ&rdot=1&source=gbs_api"
    },
    "accessInfo": {
        "country": "FR",
        "viewability": "ALL_PAGES",
        "embeddable": true,
        "publicDomain": true,
        "textToSpeechPermission": "ALLOWED",
        "epub": {
            "isAvailable": true,
            "downloadLink": "http://books.google.fr/books/download/Adventures_of_Sherlock_Holmes.epub?id=buc0AAAAMAAJ&hl=&output=epub&source=gbs_api"
        },
        "pdf": {
            "isAvailable": true,
            "downloadLink": "http://books.google.fr/books/download/Adventures_of_Sherlock_Holmes.pdf?id=buc0AAAAMAAJ&hl=&output=pdf&sig=ACfU3U3UFzY0zsHRr3M-FLDDrmM0rrWf4Q&source=gbs_api"
        },
        "webReaderLink": "http://play.google.com/books/reader?id=buc0AAAAMAAJ&hl=&source=gbs_api",
        "accessViewStatus": "FULL_PUBLIC_DOMAIN",
        "quoteSharingAllowed": false
    }
}
``` 
To align this data to DBPedia we'll take a couple of entities such as:
- https://dbpedia.org/page/Title_(publishing)
- https://dbpedia.org/ontology/author 
- https://dbpedia.org/page/Publishing
- https://dbpedia.org/page/Book
- https://dbpedia.org/ontology/language
- https://dbpedia.org/ontology/country

## CSV
The purpose of the complementary CSV file can be either to add information that was not provided by google's API, or to provide second source of the same information. 
The CSV file was downloaded from `https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks`.

### CSV Details
Check word file.

## References
* https://www.w3.org/TR/csvw-ucr/
  
------
# Provided Questions:
1. Figure out a use case to integrate data from 2 non-RDF sources:  

* Web API that you will query by writing a SPARQL micro-service:
The API must NOT be those given in example during the TD, Deezer and MusicBrainz, unless you chose a different service and target vocabulary.
Align the data generated on a vocabulary that is relevant for your use case, such as Schema.org, DBpedia, Wikidata or any other one you can find on http://lov.linkeddata.es.
If you do not find any existing relevant vocabulary, create one of your own (RDFS or OWL).  

* A CSV file
Lift the file to RDF using a CSVW mapping and the tool of your choice, for example csv2rdf
Align the data generated on a vocabulary that is relevant for your use case, ideally the same as for the SPARQL micro-service
If you do not find a public CSV file that matches your use case, you are allowed to write one. In that case, the grade iwll take into consideration how difficult it is to write the final federated query.

2. Write a SPARQL federated query that involves both data sources: load the RDF file in Corese, and query it together with the SPARQL micro-service.
SPARQL federated queries are written with the SERVICE clause, check the spefication: https://www.w3.org/TR/sparql11-federated-query/
 
3. Upload the result of your work as a Zip file containing:

A PDF file describing succinctly your use case, the API and CSV file you have selected, and the vocabulary(ies) that you have selected or created (which classes and properties you used).
a folder sparql-micro-services with the code of the SPARQL micro-service (config.ini, profile.jsonld, construct.sparql)
a folder csvw with: the csv file, the CSVW mapping, and the result file in Turtle generated with csv2rdf.
a screenshot of Yasgui or Corese GUI where you query individually each source with a simple "construct where {?s ?p ?p}".
a screenshot of Yasgui or Corese GUI where you execute the SPARQL federated query (that can be either a SELECT or CONSTRUCT query).



The grade will take into account:
* The quality of the mapping to the target vocabulary  
* The challenge of reconciling the two sources: if the CSV file and the API represent exactly the same information and you just gather the results, that's not challenging.
