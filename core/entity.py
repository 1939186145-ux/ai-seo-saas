import jieba

def extract_entities(text):
    words = jieba.lcut(text)

    stop = {"的","了","和","是","在","我们","一个","以及","与","等"}

    entities = [
        w for w in words
        if len(w) > 2 and w not in stop
    ]

    return list(set(entities))[:30]