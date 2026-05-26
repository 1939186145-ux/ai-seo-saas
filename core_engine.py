from cleaner import clean_url
from semantic_chunk import semantic_chunk
from embedding import embed_chunks
from vector_store import save_faiss
from hybrid_retrieval import hybrid_search

from entity.entity_extractor import extract_entities
from scoring.citation_score_v2 import citation_score_v2
from geo.geo_score_v2 import geo_score_v2
from analysis.seo_analyzer import seo_analysis
from faq.faq_generator import generate_faq
from schema.schema_generator import generate_schema
from rewrite import ai_rewrite


def run_pipeline(url, query):

    # 1. 清洗
    text = clean_url(url)

    # 2. 切块
    chunks = semantic_chunk(text)

    # 3. 向量
    embeddings = embed_chunks(chunks)

    # 4. FAISS
    save_faiss(chunks, embeddings)

    # 5. 检索
    docs = hybrid_search(query)
    best_doc = docs[0]

    # 6. GEO分析
    entities = extract_entities(best_doc)
    citation = citation_score_v2(best_doc)
    geo = geo_score_v2(best_doc)
    seo = seo_analysis(best_doc)
    faq = generate_faq(best_doc)
    schema = generate_schema()

    # 7. AI优化
    rewrite = ai_rewrite(best_doc)

    return {
        "entities": entities,
        "citation_score": citation,
        "geo_score": geo,
        "seo_analysis": seo,
        "faq": faq,
        "schema": schema,
        "rewrite": rewrite
    }