def citation_score(text):

    score = 0

    if "研究" in text:
        score += 20

    if "数据" in text:
        score += 20

    if "来源" in text:
        score += 20

    if len(text) > 300:
        score += 20

    if "：" in text:
        score += 20

    return score