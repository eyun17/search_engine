import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os

# to look up words in the index
def add_to_index(url, text, index):
    words = text.split()
    for word in words:
        word = word.lower()
        if word not in index:
            index[word] = []
        if url not in index[word]:
            index[word].append(url)

def crawl():
    index = {}
    visited = set()
    # the base URL for the website
    # parse the html and check if there is a link to another page

    while start_url:
        agd = [start_url]
        url = agd.pop()
        idx_page = requests.get(url)
        soup = BeautifulSoup(idx_page.content, 'html.parser')
        soup_list = soup.find_all("a")
        for page in soup_list:
            page = page.get('href')
            current_url = base_url + page
            # the list of acting as a queue of URLs to visit
            agenda = [current_url]
            # the Crawling loop
            url = agenda.pop()
            # Logs the URL being fetched for debugging or informational purposes
            print("Get ", url)
            # Sends an HTTP GET request to the URL
            r = requests.get(url)
            # Prints th HTTP response object r and its character encoding
            # Ensures the request was successful
            visited.add(url)
            if r.status_code == 200:
                # parsing the HTML
                soup = BeautifulSoup(r.content, 'html.parser')
                add_to_index(url, soup.get_text(), index)

        return index

def search(index, words):
    results = []
    for word in words:
        word = word.lower()
        if word in index:
            results.append(index[word])
    return results

# Example usage
if __name__ == "__main__":
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    base_url = "https://vm009.rz.uos.de/crawl/"
    index = crawl()
    user_input = input("Enter a word to search for: ")
    test_results = search(index, user_input.split())
    print(index)
    print(test_results)
