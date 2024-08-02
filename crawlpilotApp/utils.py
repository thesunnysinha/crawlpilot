import requests
from bs4 import BeautifulSoup
from transformers import pipeline

summarizer = pipeline("summarization")

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').text if soup.find('h1') else 'No title found'
    text = ' '.join(p.text for p in soup.find_all('p'))
    summary = summarizer(text, max_length=round(len(text) * 0.3), min_length=50)[0]['summary_text']
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return title, summary, links
