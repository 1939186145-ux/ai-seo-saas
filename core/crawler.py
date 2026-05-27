import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")

    title = soup.title.text if soup.title else ""
    text = soup.get_text(" ", strip=True)

    return {
        "title": title,
        "content": text[:8000]
    }