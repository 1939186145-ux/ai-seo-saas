import requests
from bs4 import BeautifulSoup
import re

def clean_url(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = "utf-8"
    except:
        return url

    soup = BeautifulSoup(r.text, "html.parser")

    # 删除无用标签
    for tag in soup(["script", "style", "nav", "footer", "img"]):
        tag.decompose()

    text = soup.get_text("\n")

    # 🚨 核心修复：去掉非法字符 + 乱码
    text = re.sub(r'[^\u4e00-\u9fff\w\s.,;:()（）-]', '', text)

    lines = [
        line.strip()
        for line in text.splitlines()
        if len(line.strip()) > 5
    ]

    clean_text = "\n".join(lines)

    return clean_text