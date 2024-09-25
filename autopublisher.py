import os
import requests
import base64
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# List to store titles, descriptions, and links for future use
titles = []
descriptions = []
links = []

# Retrieve credentials from environment variables
user = os.getenv('WORDPRESS_USER')
password = os.getenv('WORDPRESS_PASSWORD')
domain = os.getenv('WORDPRESS_DOMAIN')

# Base URL for WordPress REST API
wordpress_url = f"{domain}/wp-json/wp/v2"

# Combine username and password for authorization and encode using base64
credentials = f"{user}:{password}"
encoded_token = base64.b64encode(credentials.encode())

# Header for authentication and user-agent identification
headers = {
    'Authorization': f'Basic {encoded_token.decode("utf-8")}',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}

def fetch_page_content(url):
    """Fetch and parse HTML content from the given URL."""
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def extract_text_from_elements(elements):
    """Extract and clean text from a list of HTML elements."""
    return [element.get_text().strip('\n') for element in elements]

# URL of the article to fetch
article_url = 'https://acdailynews.com/index.php/2024/09/20/shqiptaret-refuzojne-chatgpt-e-perdorin-shume-me-pak-se-rajoni/'

try:
    # Fetch and parse the article page content
    soup = fetch_page_content(article_url)

    # Extract the article title
    article_title = soup.find("h1", class_="s-title").text.strip('\n')

    # Extract paragraphs from the article body
    article_body_elements = soup.find('div', class_="entry-content").find_all('p')
    article_body_text = extract_text_from_elements(article_body_elements)
    article_body = ' '.join(article_body_text)

    # Prepare the payload to create a new post in WordPress
    post_data = {
        'title': article_title,
        'content': article_body,
        'status': 'draft'  # Save as draft
    }

    # Send a POST request to the WordPress API to create a new post
    response = requests.post(f"{wordpress_url}/posts", headers=headers, json=post_data)
    print(response.status_code, response.json())  # Print the response for debugging

except Exception as e:
    print(f"An error occurred: {e}")
    print(f"Failed to process the URL: {article_url}")
