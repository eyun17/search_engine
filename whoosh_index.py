from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
from crawler import find_all_pages, get_page_content

def create_whoosh_index(index_dir="indexdir"):
    """
    Create a Whoosh index directory and schema.
    :param index_dir: Directory to store the index.
    :return: Index object.
    """
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    
    # Define the schema
    schema = Schema(url=ID(stored=True, unique=True), content=TEXT(stored=True), title=TEXT(stored=True))
    
    # Create the index
    return create_in(index_dir, schema)

def add_to_whoosh_index(index, url, title, content):
    """
    Add a single document to the Whoosh index.
    :param index: The Whoosh index object.
    :param url: URL of the page.
    :param title: Title of the page.
    :param content: Text content of the page.
    """
    writer = index.writer()
    writer.add_document(url=url, title=title, content=content)
    writer.commit()

def populate_whoosh_index(base_url, pages, index):
    """
    Crawl and add all pages to the Whoosh index.
    :param pages: List of pages (URLs).
    :param index: The Whoosh index object.
    """
    for url in pages:
        print(f"Indexing: {url}")
        title, content = get_page_content(url)
        
        if title and content:
            add_to_whoosh_index(index, url, title, content)

def search_whoosh_index(index_dir, query_string):
    """
    Search the Whoosh index for a given query.
    :param index_dir: Directory where the index is stored.
    :param query_string: Query string entered by the user.
    :return: List of search results as dictionaries.

    """
    index = open_dir(index_dir)
    results_list = []

    with index.searcher() as searcher:
        query = QueryParser("content", index.schema).parse(query_string)
        results = searcher.search(query, limit=10)

        if results:
            for result in results:
                results_list.append({
                    "url": result["url"],
                    "title": result["title"],
                    "counts": len(results)
                })
        else:
            print("No results found.")

    return results_list

if __name__ == "__main__":
    base_url = "https://vm009.rz.uos.de/crawl/"
    index_dir = "indexdir"
    
    # Step 1: Create the index
    windex = create_whoosh_index(index_dir)

    # Step 2: Find all pages
    pages = find_all_pages(base_url)
    print(f"Pages found: {pages}")
    
    # Step 3: Populate the index
    populate_whoosh_index(base_url, pages, windex)
    
    # Step 4: Search the index
    while True:
        user_query = input("Enter your search query (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        print(search_whoosh_index(index_dir, user_query))
