def ranking_score(geo_score, citation_score, entities):

    score = 0

    # GEO权重（最重要）
    score += geo_score * 0.5

    # citation权重
    score += citation_score * 0.3

    # 实体质量
    score += min(len(entities), 20) * 1.0

    return round(score, 2)