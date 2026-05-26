import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def clean_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)

    soup = BeautifulSoup(response.text, "lxml")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text("\n")

    clean_text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    return clean_text