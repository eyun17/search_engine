import requests
from bs4 import BeautifulSoup

def find_all_pages(base_url):
    """Find all pages on the website."""
    visited = set() 
    agenda = [base_url] 
    all_pages = [] 

    while agenda:
        url = agenda.pop(0) 
        
        if url in visited: 
            continue
        
        visited.add(url) 
        print(f'Finding pages: {url}')
        
        try:
            response = requests.get(url)
            response.raise_for_status() 
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            continue
        
        # Add this URL to the list of all discovered pages
        all_pages.append(url)

        # Parse the page to find links
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            # We consider only valid pages, including relative URLs
            if href.startswith('/') or href.startswith('page'):
                # If the href starts with '/', it's a relative link to the base URL
                full_url = base_url + href if href.startswith('/') else base_url + href
                if full_url not in visited:
                    agenda.append(full_url)

    return all_pages

def get_page_content(url):
    """Get the title and content of a page."""
    try:
        response = requests.get(url)
        # to check if the request was successful
        response.raise_for_status()
        # Parse the page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Get the title and content
        title = soup.title.string if soup.title else "No Title"
        # Get the text content of the page
        content = soup.get_text()
        return title, content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None

