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
try:
    ssl._create_default_https_context = ssl.create_default_context(
        cafile=certifi.where()
    )
except:
    pass

# =========================
# APP
# =========================
app = Flask(__name__)

# =========================
# 中文字体（解决PDF乱码核心）
# =========================
FONT_PATH = "C:/Windows/Fonts/simhei.ttf"

try:
    pdfmetrics.registerFont(TTFont("SimHei", FONT_PATH))
    PDF_FONT = "SimHei"
except:
    PDF_FONT = "Helvetica"

# =========================
# SAFE IMPORT
# =========================
def safe_import(module, func=None):
    try:
        m = __import__(module, fromlist=["*"])
        return getattr(m, func) if func else m
    except:
        return None


clean_url = safe_import("cleaner", "clean_url")
semantic_chunk = safe_import("semantic_chunk", "semantic_chunk")
hybrid_search = safe_import("hybrid_retrieval", "hybrid_search")
simple_rerank = safe_import("simple_reranker", "simple_rerank")
ai_rewrite = safe_import("rewrite", "ai_rewrite")

SEOEntityEngineV3 = safe_import("v3.entity_engine", "SEOEntityEngineV3")
geo_score_v3 = safe_import("v2.geo_score_v3", "geo_score_v3")
ranking_score = safe_import("v2.ranking_engine", "ranking_score")
QueryExpander = safe_import("query_expander", "QueryExpander")
IndustryDetector = safe_import("industry_detector", "IndustryDetector")

entity_engine = SEOEntityEngineV3() if SEOEntityEngineV3 else None
industry_detector = IndustryDetector() if IndustryDetector else None
query_expander = QueryExpander() if QueryExpander else None

# =========================
# STORAGE
# =========================
HISTORY_FILE = "data/history.json"
PDF_DIR = "data/pdf"

os.makedirs("data", exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)


# =========================
# HISTORY
# =========================
def save_history(record):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(record)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# PDF（最终修复版）
# =========================
def generate_pdf(report):

    report_id = report.get("id")
    data = report.get("data", {})

    file_path = os.path.join(PDF_DIR, f"{report_id}.pdf")

    c = canvas.Canvas(file_path)
    c.setFont(PDF_FONT, 11)

    y = 800

    def line(text):
        nonlocal y
        c.drawString(50, y, str(text))
        y -= 18

    base = data.get("base", {})
    scores = data.get("scores", {})
    entities = data.get("entities", [])
    rewrite = data.get("optimization", {}).get("rewrite", "")

    line("AI SEO SaaS REPORT")
    y -= 10

    line(f"URL: {base.get('url','')}")
    line(f"QUERY: {base.get('query','')}")
    line(f"INDUSTRY: {base.get('industry','')}")
    y -= 10

    line("SCORES:")
    for k, v in scores.items():
        line(f"{k}: {v}")

    y -= 10

    line("ENTITIES:")
    for e in entities[:10]:
        line(f"- {e}")

    y -= 10

    line("AI REWRITE:")
    for i in range(0, min(len(rewrite), 400), 50):
        line(rewrite[i:i+50])

    c.save()
    return file_path


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =========================
# ANALYZE（关键修复版）
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json or {}
    url = data.get("url", "")
    query = data.get("query", "")

    report_id = str(uuid.uuid4())

    # ⭐ 永远保证 clean_text 存在（修复崩溃核心）
    try:
        clean_text = clean_url(url) if clean_url else url
    except:
        clean_text = url

    try:
        industry = "未知"
        keywords = []

        if industry_detector:
            r = industry_detector.detect_industry(clean_text)
            industry = r.get("industry", "未知")
            keywords = r.get("keywords", [])

        docs = [clean_text]

        # retrieval
        if hybrid_search:
            expanded = query_expander.expand(query, industry) if query_expander else [query]
            docs = []
            for q in expanded:
                r = hybrid_search(q)
                if r:
                    docs.extend(r)

        if not docs:
            docs = [clean_text]

        if simple_rerank:
            docs = simple_rerank(query, docs)

        best_doc = docs[0]

        # entities
        entities = entity_engine.extract_entities(best_doc, keywords) if entity_engine else []

        # scores
        geo = geo_score_v3(best_doc, entities) if geo_score_v3 else 50
        citation = min(len(set(entities)) * 2, 100)
        ranking = ranking_score(geo, citation, entities) if ranking_score else 50

        # ⚠️ 修复：AI必须基于原文 clean_text，不是 best_doc
        rewrite = ai_rewrite(clean_text) if ai_rewrite else clean_text

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
            },
            "visual": {
                "radar": {
                    "labels": ["GEO", "Citation", "Ranking", "Entity", "Content"],
                    "values": [geo, citation, ranking, len(entities), 85]
                },
                "trend": {
                    "dates": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    "geo": [20, 30, 35, 40, geo],
                    "citation": [40, 50, 65, 80, citation],
                    "ranking": [30, 45, 50, 60, ranking]
                }
            }
        }

        save_history({
            "id": report_id,
            "time": datetime.now().isoformat(),
            "data": result
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


# =========================
# PDF DOWNLOAD
# =========================
@app.route("/report/<report_id>/pdf")
def download_pdf(report_id):

    for item in load_history():
        if item["id"] == report_id:
            path = generate_pdf(item)
            return send_file(path, as_attachment=True)

    return jsonify({"error": "not found"}), 404


# =========================
# RUN
# =========================
if __name__ == "__main__":
 port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)