import ssl
import certifi
import os
import json
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, render_template, send_from_directory

# =========================
# SSL CONFIG
# =========================
try:
    ssl._create_default_https_context = ssl.create_default_context(
        cafile=certifi.where()
    )
except:
    pass

# =========================
# ENV
# =========================
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# =========================
# Flask
# =========================
app = Flask(__name__)

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
embed_chunks = safe_import("embedding", "embed_chunks")
save_faiss = safe_import("vector_store", "save_faiss")
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
# HISTORY
# =========================
HISTORY_FILE = "data/history.json"


def save_history(record):
    os.makedirs("data", exist_ok=True)

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
# HOME
# =========================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =========================
# ANALYZE
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json or {}
    url = data.get("url", "")
    query = data.get("query", "")

    report_id = str(uuid.uuid4())
    url_text = url

    try:

        # clean
        clean_text = clean_url(url) if clean_url else url

        # industry
        if industry_detector:
            industry_result = industry_detector.detect_industry(clean_text)
            industry = industry_result.get("industry", "未知")
            keywords = industry_result.get("keywords", [])
        else:
            industry = "未知"
            keywords = []

        # chunk
        chunks = semantic_chunk(clean_text) if semantic_chunk else [clean_text]

        # embedding
        if embed_chunks:
            embeddings = embed_chunks(chunks)
            if save_faiss:
                save_faiss(chunks, embeddings)

        # retrieval
        expanded = query_expander.expand(query, industry) if query_expander else [query]

        docs = []
        if hybrid_search:
            for q in expanded:
                r = hybrid_search(q)
                if r:
                    docs.extend(r)

        if not docs:
            docs = [clean_text]

        # rerank
        if simple_rerank:
            docs = simple_rerank(query, docs)

        best_doc = docs[0]

        # entity
        entities = entity_engine.extract_entities(best_doc, keywords) if entity_engine else []

        # scores
        geo = geo_score_v3(best_doc, entities) if geo_score_v3 else 50
        citation = min(len(set(entities)) * 2, 100)
        ranking = ranking_score(geo, citation, entities) if ranking_score else 50

        # rewrite
        rewrite = ai_rewrite(best_doc) if ai_rewrite else best_doc

        radar = {
            "labels": ["GEO", "Citation", "Ranking", "Entity", "Content"],
            "values": [geo, citation, ranking, len(entities), 85]
        }

        trend = {
            "dates": ["Mon","Tue","Wed","Thu","Fri"],
            "geo": [20,30,35,40,geo],
            "citation": [40,50,65,80,citation],
            "ranking": [30,45,50,60,ranking]
        }

        result = {
            "success": True,
            "report_id": report_id,
            "base": {"url": url, "query": query, "industry": industry},
            "scores": {
                "geo_score": geo,
                "citation_score": citation,
                "ranking_score": ranking
            },
            "entities": entities[:80],
            "optimization": {"rewrite": rewrite},
            "seo_suggestions": [
                "增加FAQ模块",
                "增加Schema结构化数据",
                "提高实体覆盖率",
                "增加行业标准引用",
                "优化标题关键词"
            ],
            "visual": {"radar": radar, "trend": trend}
        }

        # SAVE HISTORY
        save_history({
            "id": report_id,
            "time": datetime.now().isoformat(),
            "url": url,
            "query": query,
            "data": result
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "report_id": report_id
        })


# =========================
# SHARE API
# =========================
@app.route("/report/<report_id>")
def get_report(report_id):
    data = load_history()
    for item in data:
        if item["id"] == report_id:
            return jsonify(item)
    return jsonify({"error": "not found"}), 404


# =========================
# PDF STATIC
# =========================
@app.route("/data/<path:filename>")
def files(filename):
    return send_from_directory("data", filename)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)