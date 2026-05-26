def simple_rerank(query, docs):
    """
    🚀 轻量rerank（无模型版本）
    """

    scored = []

    query_tokens = set(query.lower().split())

    for d in docs:
        score = 0

        text = d.lower()

        # 1. query完全匹配加分
        if query.lower() in text:
            score += 10

        # 2. 关键词重合度
        text_tokens = set(text.split())
        score += len(query_tokens & text_tokens)

        scored.append((score, d))

    # ✅ 正确排序（这里是你报错的地方）
    scored.sort(key=lambda x: x[0], reverse=True)

    return [d for _, d in scored]