import re
from tqdm import tqdm

def parse_and_modify_books(file_path, output_path):
    # Read data from the file with utf-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # Replace whitespace characters with underscore
    data = re.sub(r'%20', '_', data)

    # Parsing the data
    books_by_author = {}
    books_by_publisher = {}
    pattern = re.compile(r"<http://myonto\.org/book/(.*?)>\s+a <http://myonto\.org/myonto_schema/Book>;(.+?)(?=<http://myonto\.org/book/|$)", re.DOTALL)
    properties_pattern = re.compile(r"<http://myonto\.org/myonto_schema/(.*?)>\s+\"(.*?)\";")

    for book, properties_str in tqdm(pattern.findall(data), desc="Parsing books", unit="book"):
        properties = dict(properties_pattern.findall(properties_str))
        author = properties.get("author")
        publisher = properties.get("publisher")
        
        # Track books by author
        if author:
            if author not in books_by_author:
                books_by_author[author] = []
            books_by_author[author].append(book)

        # Track books by publisher
        if publisher:
            if publisher not in books_by_publisher:
                books_by_publisher[publisher] = []
            books_by_publisher[publisher].append(book)

    # Adding the hasSameAuthor and hasSamePublisher property with tqdm for progress tracking
    for entity, books in tqdm({**books_by_author, **books_by_publisher}.items(), desc="Adding properties", unit="entity"):
        if len(books) > 1:
            for book in books:
                if entity in books_by_author:
                    prop = "hasSameAuthor"
                elif entity in books_by_publisher:
                    prop = "hasSamePublisher"
                
                links = ', '.join([f'<http://myonto.org/book/{b}>' for b in books if b != book])
                book_pattern = re.compile(rf"(http://myonto\.org/book/{book}>\n\s+a <http://myonto\.org/myonto_schema/Book>;)")
                data = book_pattern.sub(lambda x: x.group(0) + f"\n  <http://myonto.org/myonto_schema/{prop}> " + links + ";" if prop not in x.group(0) else x.group(0), data)

    # Write modified data to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(data)

# Modify the file paths as necessary
input_file = 'books.ttl'
output_file = 'books_modified.ttl'

parse_and_modify_books(input_file, output_file)
