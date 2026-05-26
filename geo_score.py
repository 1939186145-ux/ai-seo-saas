def geo_score(text):

    score = 0

    if "总结" in text:
        score += 20

    if "步骤" in text:
        score += 20

    if "优点" in text:
        score += 20

    if "缺点" in text:
        score += 20

    if "FAQ" in text:
        score += 20

    return score