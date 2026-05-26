# rerank.py

import re

def _score_doc(query, doc):
    """
    轻量级 SEO rerank scoring
    """

    if not doc:
        return 0

    query_words = set(query.lower().split())
    doc_lower = doc.lower()

    score = 0

    # =========================
    # 1. 关键词命中
    # =========================
    for w in query_words:
        if w in doc_lower:
            score += 5

    # =========================
    # 2. 标题权重（SEO核心）
    # =========================
    title_match = re.search(r"#\s*(.+)", doc)
    if title_match:
        title = title_match.group(1).lower()
        for w in query_words:
            if w in title:
                score += 10

    # =========================
    # 3. 标准 / GB 权重
    # =========================
    if "gb" in doc_lower or "iso" in doc_lower:
        score += 3

    # =========================
    # 4. 数值/参数密度（SEO产品页很重要）
    # =========================
    numbers = len(re.findall(r"\d+", doc))
    score += min(numbers * 0.2, 10)

    # =========================
    # 5. 结构化内容奖励（H2 / list）
    # =========================
    if "##" in doc:
        score += 3
    if "-" in doc:
        score += 2

    # =========================
    # 6. 长度惩罚（避免垃圾长文）
    # =========================
    length_penalty = len(doc) / 1000
    score -= length_penalty

    return score


def rerank_docs(query, docs):
    """
    SEO rerank主函数
    """

    if not docs:
        return []

    scored_docs = []

    for doc in docs:
        score = _score_doc(query, doc)
        scored_docs.append((doc, score))

    # 排序
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return [d[0] for d in scored_docs]