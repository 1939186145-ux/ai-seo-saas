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
# FONT
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
os.makedirs("data", exist_ok=True)
os.makedirs("data/pdf", exist_ok=True)

HISTORY_FILE = "data/history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_history(record):
    data = load_history()
    data.append(record)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =========================
# 🔥 SEO建议生成（关键修复）
# =========================
def generate_seo_suggestions(text, entities):

    base = [
        "增加FAQ模块",
        "优化H2/H3结构",
        "提升AI可引用性",
        "增加Schema结构化数据",
        "增强实体覆盖"
    ]

    if len(text) < 300:
        base.append("内容过短，建议扩展内容深度")

    if len(entities) < 3:
        base.append("增加行业实体词覆盖")

    return base


# =========================
# PDF
# =========================
def generate_pdf(report):

    report_id = report.get("id")
    data = report.get("data", {})

    path = os.path.join("data/pdf", f"{report_id}.pdf")

    c = canvas.Canvas(path)
    c.setFont(PDF_FONT, 11)

    y = 800

    def line(t):
        nonlocal y
        c.drawString(50, y, str(t))
        y -= 18

    base = data.get("base", {})
    scores = data.get("scores", {})
    entities = data.get("entities", [])
    rewrite = data.get("optimization", {}).get("rewrite", "")

    line("AI SEO SaaS V10 REPORT")
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
    for i in range(0, min(len(str(rewrite)), 400), 50):
        line(str(rewrite)[i:i+50])

    c.save()
    return path


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =========================
# ANALYZE V10 FINAL
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json or {}
    url = data.get("url", "")
    query = data.get("query", "")

    report_id = str(uuid.uuid4())

    # =========================
    # CLEAN TEXT（必兜底）
    # =========================
    try:
        clean_text = clean_url(url) if clean_url else url
    except:
        clean_text = url

    if not clean_text:
        clean_text = "empty content"

    # =========================
    # INDUSTRY
    # =========================
    industry = "未知"
    keywords = []

    try:
        if industry_detector:
            r = industry_detector.detect_industry(clean_text)
            industry = r.get("industry", "未知")
            keywords = r.get("keywords", [])
    except:
        pass

    # =========================
    # RETRIEVAL（强兜底）
    # =========================
    docs = [clean_text]

    try:
        if hybrid_search and query:
            expanded = query_expander.expand(query, industry) if query_expander else [query]

            temp = []
            for q in expanded:
                r = hybrid_search(q)
                if r:
                    temp.extend(r)

            if temp:
                docs = temp
    except:
        pass

    # rerank
    try:
        if simple_rerank:
            docs = simple_rerank(query, docs)
    except:
        pass

    best_doc = docs[0] if docs else clean_text

    # =========================
    # ENTITIES（兜底）
    # =========================
    entities = []
    try:
        if entity_engine:
            entities = entity_engine.extract_entities(best_doc, keywords)
    except:
        entities = []

    # =========================
    # SCORES（永远有值）
    # =========================
    try:
        geo = geo_score_v3(best_doc, entities) if geo_score_v3 else 50
    except:
        geo = 50

    try:
        citation = min(len(set(entities)) * 5, 100)
    except:
        citation = 20

    try:
        ranking = ranking_score(geo, citation, entities) if ranking_score else (geo * 0.6 + citation * 0.4)
    except:
        ranking = (geo + citation) / 2

    # =========================
    # SEO建议（关键修复）
    # =========================
    seo_suggestions = generate_seo_suggestions(clean_text, entities)

    # =========================
    # AI REWRITE（强兜底）
    # =========================
    try:
        rewrite = ai_rewrite(clean_text) if ai_rewrite else clean_text
    except:
        rewrite = clean_text

    result = {
        "success": True,
        "report_id": report_id,
        "base": {
            "url": url,
            "query": query,
            "industry": industry
        },
        "scores": {
            "geo_score": float(geo),
            "citation_score": float(citation),
            "ranking_score": float(ranking)
        },
        "entities": entities,
        "seo_suggestions": seo_suggestions,
        "optimization": {
            "rewrite": rewrite
        },
        "visual": {
            "radar": {
                "labels": ["GEO", "Citation", "Ranking", "Entity", "Content"],
                "values": [geo, citation, ranking, len(entities), 80]
            }
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
            path = generate_pdf(item)
            return send_file(path, as_attachment=True)

    return jsonify({"error": "not found"}), 404


# =========================
# RUN（Render兼容）
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)