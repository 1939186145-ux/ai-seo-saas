# dynamic_entity_extractor.py
import re
import jieba
import jieba.analyse
STOP_WORDS = {    
"我们", "你们", "他们", "这个", "那个", "进行",    
"使用", "可以", "以及", "如果", "需要", "没有",    
"一个", "一种", "为了", "通过", "实现", "相关",    
"点击", "内容", "更多", "企业", "公司", "产品",    
"首页", "文章", "技术", "作者", "来源", "责任编辑",    
"版权", "所有", "联系", "电话", "邮箱", "网址",    
"www", "http", "https", "com", "cn", "html"
}

class DynamicEntityExtractor:
    def clean_text(self, text):
        text = re.sub(r"\\s+", " ", text)        
text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9℃%Nmm/]+", " ", text)
        return text

    def extract(self, text, top_k=50):
        text = self.clean_text(text)
        keywords = jieba.analyse.extract_tags(            
text,            
topK=top_k,            
withWeight=False,            
allowPOS=(                
'n',                
'nz',                
'vn',                
'eng'
            )
        )
        entities = []
        for word in keywords:
            word = word.strip()
            if len(word) < 2:                
continue
            if word.lower() in STOP_WORDS:                
continue
            if word.isdigit():                
continue
            entities.append(word)
        # 去重        
entities = list(dict.fromkeys(entities))
        return entities[:50]