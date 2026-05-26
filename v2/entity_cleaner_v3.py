import re
import jieba

STOPWORDS = set([
    "点击", "进入", "查看", "一家", "有限公司",
    "微信", "电话", "邮箱", "com", "www", "http",
    "copyright", "版权所有", "地址", "官网",
    "产品", "行业", "公司", "专业", "厂家"
])

def clean_entities(text):

    words = jieba.lcut(text)

    entities = []

    for w in words:

        w = w.strip()

        if not w:
            continue

        # 过滤停用词
        if w in STOPWORDS:
            continue

        # 过滤纯数字
        if re.match(r'^\d+$', w):
            continue

        # 过滤URL碎片
        if any(x in w for x in ["http", "www", "com"]):
            continue

        # 过滤太短
        if len(w) < 2:
            continue

        entities.append(w)

    # 强保留：行业核心词（非常关键）
    keywords = [
        "测试仪",
        "持粘性",
        "初粘力",
        "防水卷材",
        "压敏胶",
        "剥离强度"
    ]

    for k in keywords:
        if k in text:
            entities.append(k)

    # 标准识别（权重最高）
    standards = re.findall(r'GB/T\s?\d+', text)

    return list(set(entities + standards))