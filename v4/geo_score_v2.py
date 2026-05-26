def geo_score_v2(text, entities, citations):

    # 标准权重
    standard_score = sum(1 for e in entities if "GB/T" in e) * 20

    # 定义句
    definition_score = len(citations.get("definition", [])) * 25

    # 指标密度
    metric_score = len(citations.get("metric", [])) * 20

    # FAQ能力
    faq_score = 20 if len(citations.get("definition", [])) > 0 else 0

    # 实体密度
    entity_score = min(len(set(entities)) * 2, 100)

    score = (
        standard_score * 0.2 +
        definition_score * 0.25 +
        metric_score * 0.2 +
        faq_score * 0.15 +
        entity_score * 0.2
    )

    return round(score, 2)