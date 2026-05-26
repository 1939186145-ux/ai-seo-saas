def geo_score_v3(text, entities):

    score = 0

    # 结构评分
    if "##" in text:
        score += 15

    # FAQ结构
    if "FAQ" in text:
        score += 15

    # 标准权重（核心SEO信号）
    if "GB/T" in text:
        score += 25

    # 实体质量评分（过滤后）
    real_entities = [
        e for e in entities
        if len(e) > 2
        and e not in ["测试", "产品", "行业"]
    ]

    if len(real_entities) > 10:
        score += 25
    elif len(real_entities) > 5:
        score += 15

    # 列表结构
    if "1." in text or "-" in text:
        score += 10

    return min(score, 100)