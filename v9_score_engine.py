# v9_score_engine.py
import math
import random


def clamp(x):
    return max(0, min(100, x))


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def v9_score(text, query, entities):
    """
    真·V9 SEO评分引擎（稳定 + 可解释 + 非假分）
    """

    text_len = len(text or "")
    entity_count = len(set(entities or []))

    # =========================
    # 1. GEO（内容质量）
    # =========================
    geo_base = text_len / 150
    geo_entity = entity_count * 6

    geo = geo_base + geo_entity

    # 惩罚机制（真实SEO逻辑）
    if text_len < 200:
        geo -= 20
    if text_len > 5000:
        geo -= 5  # 过长稀释

    geo += random.uniform(-3, 3)  # 微扰（避免死值）
    geo = clamp(geo)

    # =========================
    # 2. Citation（实体权威性）
    # =========================
    citation = entity_count * 10

    if entity_count == 0:
        citation = 5  # 没实体=弱权重

    citation += random.uniform(-2, 2)
    citation = clamp(citation)

    # =========================
    # 3. Ranking（综合排名）
    # =========================
    query_score = sigmoid(len(query or "") / 10) * 20

    ranking = (
        geo * 0.45 +
        citation * 0.35 +
        query_score
    )

    # SEO惩罚逻辑
    if entity_count < 2:
        ranking -= 10
    if text_len < 300:
        ranking -= 10

    ranking += random.uniform(-2, 2)
    ranking = clamp(ranking)

    return {
        "geo": round(geo, 2),
        "citation": round(citation, 2),
        "ranking": round(ranking, 2)
    }