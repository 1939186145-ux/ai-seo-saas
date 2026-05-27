import requests
from bs4 import BeautifulSoup


# =========================
# CLEAN URL FUNCTION (STABLE)
# =========================
def clean_url(url):

    if not url:
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        # 防止乱码
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "lxml")

        # =========================
        # REMOVE NOISE TAGS
        # =========================
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # =========================
        # EXTRACT TEXT
        # =========================
        text = soup.get_text("\n")

        # =========================
        # CLEAN LINES
        # =========================
        clean_text = "\n".join(
            line.strip()
            for line in text.splitlines()
            if line.strip() and len(line.strip()) > 1
        )

        return clean_text

    except Exception as e:

        # =========================
        # FALLBACK（防崩核心）
        # =========================
        return f"""
[系统降级模式]

无法抓取网页内容

URL: {url}

错误信息: {str(e)}

建议：
- 检查链接是否可访问
- 或使用文本输入模式
"""