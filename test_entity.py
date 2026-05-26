from entity.entity_extractor import extract_entities

text = """
GB/T 4851 持粘性测试仪
适用于医药包装检测
"""

entities = extract_entities(text)

print(entities)