import re
import jieba.analyse

def extract_entities(text):

    keywords = jieba.analyse.extract_tags(
        text,
        topK=30
    )

    standards = re.findall(
        r'GB/T\s?\d+',
        text
    )

    entities = list(set(
        keywords + standards
    ))

    return entities