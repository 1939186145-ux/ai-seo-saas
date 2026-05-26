import re
import jieba
import jieba.analyse


class SEOEntityEngineV3:

    def __init__(self):

        # =========================================
        # 核心SEO实体词
        # =========================================
        self.seo_keywords = set([

            # 仪器行业
            "测试仪",
            "试验机",
            "检测仪",
            "分析仪",

            # 胶粘行业
            "持粘性",
            "初粘力",
            "剥离强度",
            "压敏胶",
            "胶粘带",
            "防水卷材",
            "不干胶",
            "离型纸",

            # 医疗行业
            "医药包装",
            "无菌",
            "灭菌",
            "注射器",
            "药典",

            # 包装行业
            "薄膜",
            "标签",
            "包装材料",

            # SEO/GEO
            "FAQ",
            "Schema",
            "SEO",
            "GEO",

            # 标准
            "GB/T 4851",
            "GB/T 4852",
            "GB/T 23260",
            "ASTM",
            "ISO"
        ])

        # =========================================
        # 垃圾停用词
        # =========================================
        self.stopwords = set([

            # 网站垃圾词
            "点击",
            "进入",
            "查看",
            "上一篇",
            "下一篇",
            "返回",
            "更多",
            "官网",
            "首页",
            "版权所有",

            # 公司垃圾词
            "有限公司",
            "有限责任公司",
            "公司",
            "厂家",

            # 联系方式
            "电话",
            "邮箱",
            "地址",
            "微信",
            "QQ",
            "qq",

            # URL碎片
            "com",
            "cn",
            "www",
            "http",
            "https",

            # 无意义词
            "进行",
            "采用",
            "使用",
            "满足",
            "一种",
            "一般",
            "可以",
            "具有",
            "实现",
            "通过",
            "相关",
            "以及",
            "如果",
            "因此",
            "这个",
            "那个",
            "以下",
            "以上",
            "其中",
            "需要",
            "根据",
            "不同",
            "主要",
            "用于",
            "支持",
            "提供",

            # SEO垃圾词
            "推荐",
            "方法",
            "实验",
            "试验",
            "介绍",
            "应用",
            "作用",
            "功能",
            "特点",

            # 时间词
            "今天",
            "昨日",
            "目前",
            "现在",

            # 常见低质量词
            "友好",
            "稳定",
            "高效",
            "专业",
            "品质",
            "性能",
            "优势",
            "技术",
            "参数",
            "数据",
            "结果"
        ])

        # =========================================
        # 行业正则
        # =========================================
        self.patterns = [

            # GB/T标准
            r'GB/T\s?\d+(?:-\d+)?',

            # ISO标准
            r'ISO\s?\d+',

            # ASTM标准
            r'ASTM\s?[A-Z]?\d+',

            # 型号
            r'[A-Z]{2,}-\d+[A-Z]?',

            # 医疗标准
            r'USP\s?<\d+>',

            # FDA
            r'FDA\s?\d+',

            # 温度
            r'\d+℃',

            # 精度
            r'±\d+\.?\d*%',

            # 力值
            r'\d+N',

            # 尺寸
            r'\d+mm'
        ]

    # =====================================================
    # 清洗词
    # =====================================================
    def clean_word(self, word):

        word = word.strip()

        if not word:
            return None

        # 小写
        lower = word.lower()

        # URL
        if any(x in lower for x in [
            "http",
            "www",
            ".com",
            ".cn"
        ]):
            return None

        # 纯数字
        if re.match(r'^\d+$', word):
            return None

        # 长度
        if len(word) < 2:
            return None

        # 停用词
        if word in self.stopwords:
            return None

        # 中文符号
        if re.match(r'^[\W_]+$', word):
            return None

        return word

    # =====================================================
    # TF-IDF关键词
    # =====================================================
    def tfidf_keywords(self, text):

        try:

            keywords = jieba.analyse.extract_tags(
                text,
                topK=80,
                withWeight=False
            )

            return keywords

        except:
            return []

    # =====================================================
    # 实体抽取
    # =====================================================
    def extract_entities(
            self,
            text,
            dynamic_keywords=[]
    ):

        entities = set()

        # =================================================
        # 1. jieba分词
        # =================================================
        words = jieba.lcut(text)

        for w in words:

            cleaned = self.clean_word(w)

            if cleaned:
                entities.add(cleaned)

        # =================================================
        # 2. TF-IDF关键词
        # =================================================
        tfidf_words = self.tfidf_keywords(text)

        for kw in tfidf_words:

            cleaned = self.clean_word(kw)

            if cleaned:
                entities.add(cleaned)

        # =================================================
        # 3. 动态行业词
        # =================================================
        for kw in dynamic_keywords:

            cleaned = self.clean_word(kw)

            if cleaned:
                entities.add(cleaned)

        # =================================================
        # 4. 强制SEO实体
        # =================================================
        for keyword in self.seo_keywords:

            if keyword in text:
                entities.add(keyword)

        # =================================================
        # 5. 正则抽取
        # =================================================
        for pattern in self.patterns:

            matches = re.findall(pattern, text)

            for m in matches:

                cleaned = self.clean_word(m)

                if cleaned:
                    entities.add(cleaned)

        # =================================================
        # 6. 二次过滤
        # =================================================
        final_entities = []

        for e in entities:

            # 超短词过滤
            if len(e) <= 1:
                continue

            # 数字开头垃圾词
            if re.match(r'^\d+$', e):
                continue

            # 无意义中文词
            if e in self.stopwords:
                continue

            # 英文碎片
            if len(e) <= 3 and re.match(r'^[a-zA-Z]+$', e):
                continue

            final_entities.append(e)

        # =================================================
        # 7. 按长度排序（SEO更稳定）
        # =================================================
        final_entities = sorted(
            list(set(final_entities)),
            key=lambda x: len(x),
            reverse=True
        )

        # =================================================
        # 8. 限制数量（避免AI污染）
        # =================================================
        final_entities = final_entities[:120]

        return final_entities