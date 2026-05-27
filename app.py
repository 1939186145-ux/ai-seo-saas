import ssl
import certifi
import os

# =========================
# SSL
# =========================
ssl._create_default_https_context = ssl.create_default_context(
    cafile=certifi.where()
)

# =========================
# HF Cache
# =========================
os.environ["HF_HOME"] = "D:/hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/hf_cache"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# =========================
# Flask
# =========================
from flask import Flask, request, jsonify, render_template

# =========================
# SEO Core
# =========================
from cleaner import clean_url
from semantic_chunk import semantic_chunk
from embedding import embed_chunks
from vector_store import save_faiss
from hybrid_retrieval import hybrid_search
from simple_reranker import simple_rerank
from rewrite import ai_rewrite

from v3.entity_engine import SEOEntityEngineV3
from v2.geo_score_v3 import geo_score_v3
from v2.ranking_engine import ranking_score

from query_expander import QueryExpander
from industry_detector import IndustryDetector

# =========================
# Flask APP
# =========================
app = Flask(__name__)

# =========================
# Init
# =========================
entity_engine = SEOEntityEngineV3()
industry_detector = IndustryDetector()
query_expander = QueryExpander()

# =========================
# 首页
# =========================
@app.route("/")
def home():
    return render_template("dashboard.html")

# =========================
# Analyze API
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    result = {
        "success": False
    }

    try:

        data = request.json

        url = data.get("url", "")
        query = data.get("query", "")

        # =========================
        # Clean
        # =========================
        clean_text = clean_url(url)

        # =========================
        # Industry
        # =========================
        industry_result = industry_detector.detect_industry(clean_text)

        industry = industry_result.get("industry", "未知")
        keywords = industry_result.get("keywords", [])

        # =========================
        # Chunk
        # =========================
        chunks = semantic_chunk(clean_text)

        # =========================
        # Embedding
        # =========================
        embeddings = embed_chunks(chunks)

        save_faiss(chunks, embeddings)

        # =========================
        # Retrieval
        # =========================
        expanded_queries = query_expander.expand(query, industry)

        docs = []

        for q in expanded_queries:

            r = hybrid_search(q)

            if r:
                docs.extend(r)

        # =========================
        # Rerank
        # =========================
        docs = simple_rerank(query, docs)

        best_doc = docs[0]

        # =========================
        # Entity
        # =========================
        entities = entity_engine.extract_entities(
            best_doc,
            keywords
        )

        # =========================
        # Score
        # =========================
        geo_score = geo_score_v3(best_doc, entities)

        citation_score = min(
            len(set(entities)) * 2,
            100
        )

        ranking_score_value = ranking_score(
            geo_score,
            citation_score,
            entities
        )

        # =========================
        # AI Rewrite
        # =========================
        rewrite = ai_rewrite(best_doc)

        # =========================
        # Radar
        # =========================
        radar = {
            "labels": [
                "GEO",
                "Citation",
                "Ranking",
                "Entity",
                "Content"
            ],
            "values": [
                geo_score,
                citation_score,
                ranking_score_value,
                min(len(entities), 100),
                85
            ]
        }

        # =========================
        # Trend
        # =========================
        trend = {
            "dates": [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri"
            ],
            "geo": [20, 30, 35, 40, geo_score],
            "citation": [40, 50, 65, 80, citation_score],
            "ranking": [30, 45, 50, 60, ranking_score_value]
        }

        # =========================
        # Result
        # =========================
        result = {

            "success": True,

            "base": {
                "url": url,
                "query": query,
                "industry": industry
            },

            "scores": {
                "geo_score": geo_score,
                "citation_score": citation_score,
                "ranking_score": ranking_score_value
            },

            "entities": entities[:80],

            "optimization": {
                "rewrite": rewrite
            },

            "seo_suggestions": [
                "增加FAQ模块",
                "增加Schema结构化数据",
                "提高实体覆盖率",
                "增加行业标准引用",
                "优化标题关键词"
            ],

            "visual": {
                "radar": radar,
                "trend": trend
            }
        }

        return jsonify(result)

    except Exception as e:

        result["error"] = str(e)

        return jsonify(result)

# =========================
# Run
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)