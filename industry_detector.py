from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import jieba.analyse
import re


class IndustryDetector:

    def __init__(self):
        self.industry_rules = {
            "医疗": [
                "医药", "药品", "医疗", "灭菌",
                "注射器", "药典", "无菌"
            ],

            "仪器": [
                "测试仪", "试验机", "检测仪",
                "剥离", "持粘", "初粘"
            ],

            "化工": [
                "树脂", "涂料", "粘度",
                "化学", "聚合物"
            ],

            "电子": [
                "芯片", "PCB", "半导体",
                "电路", "电子元件"
            ],

            "包装": [
                "包装", "薄膜", "标签",
                "胶带", "纸箱"
            ]
        }

    def extract_keywords(self, text):

        keywords = jieba.analyse.extract_tags(
            text,
            topK=50,
            withWeight=False
        )

        return keywords

    def detect_industry(self, text):

        keywords = self.extract_keywords(text)

        scores = {}

        for industry, words in self.industry_rules.items():

            score = 0

            for w in words:
                if w in keywords:
                    score += 1

            scores[industry] = score

        best = max(scores, key=scores.get)

        return {
            "industry": best,
            "keywords": keywords,
            "scores": scores
        }