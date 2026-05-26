def geo_score_v2(text):

    score = 0

    # 标题结构
    if "##" in text:
        score += 20

    # FAQ
    if "FAQ" in text:
        score += 20

    # AI摘要结构
    if "-" in text:
        score += 20

    # 定义句
    if "是指" in text:
        score += 20

    # Chunk友好
    paragraphs = text.split("\n\n")

    short_para = sum(
        1 for p in paragraphs
        if len(p) < 150
    )

    if short_para > 5:
        score += 20

    return score