import ssl
import certifi
import os
import json
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, render_template, send_file
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =========================
# SSL
# =========================
ssl._create_default_https_context = ssl.create_default_context(
    cafile=certifi.where()
)

app = Flask(__name__)

# =========================
# 中文字体
# =========================
FONT_PATH = "C:/Windows/Fonts/simhei.ttf"

try:
    pdfmetrics.registerFont(TTFont("SimHei", FONT_PATH))
    PDF_FONT = "SimHei"
except:
    PDF_FONT = "Helvetica"


# =========================
# IMPORTS
# =========================
def safe_import(module, func=None):
    try:
        m = __import__(module, fromlist=["*"])
        return getattr(m, func) if func else m
    except:
        return None


clean_url = safe_import("cleaner", "clean_url")
hybrid_search = safe_import("hybrid_retrieval", "hybrid_search")
simple_rerank = safe_import("simple_reranker", "simple_rerank")
ai_rewrite = safe_import("rewrite", "ai_rewrite")

SEOEntityEngineV3 = safe_import("v3.entity_engine", "SEOEntityEngineV3")
IndustryDetector = safe_import("industry_detector", "IndustryDetector")

# ⭐ V9评分引擎（关键）
from v9_score_engine import v9_score


entity_engine = SEOEntityEngineV3() if SEOEntityEngineV3 else None
industry_detector = IndustryDetector() if IndustryDetector else None


# =========================
# STORAGE
# =========================
os.makedirs("data", exist_ok=True)
os.makedirs("data/pdf", exist_ok=True)

HISTORY_FILE = "data/history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    return json.load(open(HISTORY_FILE, "r", encoding="utf-8"))


def save_history(record):
    data = load_history()
    data.append(record)
    json.dump(data, open(HISTORY_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =========================
# ANALYZE（V9核心）
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json or {}
    url = data.get("url", "")
    query = data.get("query", "")

    report_id = str(uuid.uuid4())

    # =========================
    # clean
    # =========================
    text = clean_url(url) if clean_url else url

    # =========================
    # industry
    # =========================
    industry = "未知"
    keywords = []

    if industry_detector:
        r = industry_detector.detect_industry(text)
        industry = r.get("industry", "未知")
        keywords = r.get("keywords", [])

    # =========================
    # retrieval（简单稳定）
    # =========================
    docs = [text]

    if hybrid_search and query:
        r = hybrid_search(query)
        if r:
            docs = r

    if simple_rerank:
        docs = simple_rerank(query, docs)

    best_doc = "\n".join(docs[:3])

    # =========================
    # entities
    # =========================
    entities = []

    if entity_engine:
        entities = entity_engine.extract_entities(best_doc, keywords)

    # =========================
    # ⭐ V9 SCORE（唯一入口）
    # =========================
    score = v9_score(text=best_doc, query=query, entities=entities)

    geo = score["geo"]
    citation = score["citation"]
    ranking = score["ranking"]

    # =========================
    # rewrite
    # =========================
    rewrite = ai_rewrite(best_doc) if ai_rewrite else best_doc

    result = {
        "success": True,
        "report_id": report_id,
        "base": {
            "url": url,
            "query": query,
            "industry": industry
        },
        "scores": {
            "geo_score": geo,
            "citation_score": citation,
            "ranking_score": ranking
        },
        "entities": entities,
        "optimization": {
            "rewrite": rewrite
        }
    }

    save_history({
        "id": report_id,
        "time": datetime.now().isoformat(),
        "data": result
    })

    return jsonify(result)


# =========================
# PDF
# =========================
@app.route("/report/<report_id>/pdf")
def download_pdf(report_id):

    for item in load_history():
        if item["id"] == report_id:

            path = f"data/pdf/{report_id}.pdf"

            c = canvas.Canvas(path)
            c.setFont(PDF_FONT, 11)

            y = 800

            def line(t):
                nonlocal y
                c.drawString(50, y, str(t))
                y -= 18

            data = item["data"]

            line("AI SEO SaaS V9 REPORT")
            line(str(data["base"]))
            line(str(data["scores"]))
            line("entities:")
            line(str(data["entities"][:10]))

            c.save()

            return send_file(path, as_attachment=True)

    return jsonify({"error": "not found"}), 404


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)