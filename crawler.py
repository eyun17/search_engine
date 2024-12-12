import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os

def crawl(start_url, base_url):
    visited = set()
    index = {}

    def is_same_server(url):
        return url.startswith(base_url)

    def add_to_index(url, text):
        words = text.split()
        for word in words:
            word = word.lower()
            if word not in index:
                index[word] = []
            if url not in index[word]:
                index[word].append(url)

    def crawl_page(url):
        try:
            response = requests.get(url)
            if "text/html" in response.headers["Content-Type"]:
                soup = BeautifulSoup(response.text, "html.parser")
                add_to_index(url, soup.get_text())
                for link in soup.find_all("a", href=True):
                    full_url = link["href"]
                    if is_same_server(full_url) and full_url not in visited:
                        visited.add(full_url)
                        crawl_page(full_url)
        except Exception as e:
            print(f"Error Processing {url}: {e}")

    visited.add(start_url)
    crawl_page(start_url)
    return index

# to look up words in the index
def search(index, words):
    results = []
    for word in words:
        word = word.lower()
        if word in index:
            if results is None:
                results = results.append(index)

# Example usage
if __name__ == "__main__":
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    base_url = "https://vm009.rz.uos.de/crawl/"
    index = crawl(start_url, base_url)
    print(index)
