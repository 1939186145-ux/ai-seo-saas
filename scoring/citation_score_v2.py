import re

def citation_score_v2(text):

    score = 0

    # 标准号
    standards = re.findall(
        r'GB/T\s?\d+',
        text
    )

    if standards:
        score += 20

    # FAQ
    if "FAQ" in text:
        score += 20

    # 列表
    if "-" in text or "1." in text:
        score += 20

    # 数据
    if re.search(r'\d+', text):
        score += 20

    # 定义型句子
    if "是指" in text:
        score += 20

    return score