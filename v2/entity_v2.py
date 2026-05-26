# geo_score_v3.py


def geo_score_v3(text, entities):

    score = 0

    # 实体数量
    score += min(len(entities), 40)

    # FAQ
    if "FAQ" in text:
        score += 15

    # 标准引用
    standards = [
        "GB",
        "ISO",
        "ASTM",
        "DIN"
    ]

    for s in standards:
        if s in text:
            score += 10

    # Schema
    if "@type" in text:
        score += 15

    return min(score, 100)