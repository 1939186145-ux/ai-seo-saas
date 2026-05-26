import ssl
import certifi
import os

ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

os.environ["HF_HOME"] = "D:/hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/hf_cache"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from flask import Flask, request, jsonify, render_template

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
from v2.report_generator import generate_report

from query_expander import QueryExpander
from industry_detector import IndustryDetector

app = Flask(__name__)

entity_engine = SEOEntityEngineV3()
industry_detector = IndustryDetector()
query_expander = QueryExpander()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json or {}
        url = data.get("url", "").strip()
        query = data.get("query", "").strip()

        # ===================== 1 清洗 =====================
        clean_text = clean_url(url)
        if not clean_text:
            return jsonify({"success": False, "error": "抓取失败"})

        # ===================== 2 行业 =====================
        industry_result = industry_detector.detect_industry(clean_text)
        industry = industry_result["industry"]
        keywords = industry_result["keywords"]
        industry_scores = industry_result["scores"]

        # ===================== 3 chunk =====================
        chunks = semantic_chunk(clean_text)

        # ===================== 4 embedding =====================
        embeddings = embed_chunks(chunks)
        save_faiss(chunks, embeddings)

        # ===================== 5 retrieval =====================
        expanded_queries = query_expander.expand(query, industry)

        docs = []
        for q in expanded_queries:
            docs.extend(hybrid_search(q))

        if not docs:
            return jsonify({"success": False, "error": "无检索结果"})

        docs = simple_rerank(query, docs)
        best_doc = docs[0]

        # ===================== 6 entity =====================
        entities = entity_engine.extract_entities(best_doc, keywords)

        # ===================== 7 score =====================
        geo_score = geo_score_v3(best_doc, entities)
        citation_score = min(len(set(entities)) * 2, 100)
        ranking_score_val = ranking_score(geo_score, citation_score, entities)

        # ===================== 8 AI rewrite =====================
        rewrite = ai_rewrite(best_doc)

        # ===================== 9 雷达图数据（关键） =====================
        radar = {
            "labels": ["GEO", "Citation", "Ranking", "Entities", "Relevance"],
            "values": [
                geo_score,
                citation_score,
                ranking_score_val,
                min(len(entities) * 2, 100),
                min(len(docs) * 10, 100)
            ]
        }

        # ===================== 10 趋势图（模拟企业版） =====================
        trend = {
            "dates": ["D1", "D2", "D3", "D4", "D5"],
            "geo": [geo_score-10, geo_score-6, geo_score-3, geo_score-1, geo_score],
            "citation": [60, 70, 75, 85, citation_score],
            "ranking": [50, 55, 60, 62, ranking_score_val]
        }

        # ===================== 11 SEO建议 =====================
        suggestions = [
            "增加H2结构",
            "增强FAQ模块",
            "补充行业标准（ISO/ASTM）",
            "提高实体密度",
            "增加结构化Schema",
            "优化AI可引用性"
        ]

        return jsonify({
            "success": True,

            "base": {
                "url": url,
                "query": query,
                "industry": industry
            },

            "scores": {
                "geo_score": geo_score,
                "citation_score": citation_score,
                "ranking_score": ranking_score_val
            },

            "entities": entities[:80],
            "keywords": keywords[:50],

            "optimization": {
                "rewrite": rewrite,
                "suggestions": suggestions
            },

            "visual": {
                "radar": radar,
                "trend": trend
            },

            "report": generate_report(url, query, {
                "industry": industry,
                "industry_scores": industry_scores,
                "entities": entities,
                "geo_score": geo_score,
                "citation_score": citation_score,
                "ranking_score": ranking_score_val,
                "rewrite": rewrite
            })
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)