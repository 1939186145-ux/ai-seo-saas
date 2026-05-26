import re
import jieba

class SEOEntityEngineV4:

    def __init__(self):

        # ✅ 行业核心实体（增强版）
        self.seo_keywords = set([
            "测试仪",
            "试验机",
            "持粘性",
            "初粘力",
            "剥离强度",
            "压敏胶",
            "胶粘带",
            "防水卷材",
            "恒温",
            "GB/T 4851",
            "GB/T 4852",
            "GB/T 23260"
        ])

        # ❌ 垃圾词（V4强化版）
        self.stopwords = set([
            "点击","进入","查看","一家","有限公司",
            "公众","微信","电话","邮箱","官网",
            "com","www","http","https",
            "版权所有","地址","推荐","方法",
            "实验","试验","过程","使用","操作",
            "这样","一个","进行","根据","以及"
        ])

    def extract_entities(self, text, dynamic_keywords=None):

        words = jieba.lcut(text)

        entities = []

        for w in words:

            w = w.strip()

            # ❌ 过滤垃圾
            if not w:
                continue

            if w in self.stopwords:
                continue

            if re.match(r'^\d+$', w):
                continue

            if len(w) < 2:
                continue

            if any(x in w.lower() for x in ["http","www","com"]):
                continue

            entities.append(w)

        # ✅ 行业关键词强化
        if dynamic_keywords:
            for k in dynamic_keywords:
                if k and len(k) >= 2:
                    entities.append(k)

        # ✅ SEO核心词强化
        for k in self.seo_keywords:
            if k in text:
                entities.append(k)

        # ✅ 标准提取
        standards = re.findall(r'GB/T\s?\d+', text)

        # 去重
        final = list(set(entities + standards))

        # 二次过滤
        final = [
            e for e in final
            if e not in self.stopwords and len(e) > 1
        ]

        return final