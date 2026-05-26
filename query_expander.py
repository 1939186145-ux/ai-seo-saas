import re

class QueryExpander:

    def expand(self, query, industry):

        expansions = [query]

        industry_map = {

            "仪器": [
                "测试仪",
                "试验机",
                "检测设备",
                "测定仪",
                "分析仪"
            ],

            "医疗": [
                "医用",
                "灭菌",
                "包装",
                "YY/T",
                "GMP"
            ],

            "包装": [
                "薄膜",
                "胶带",
                "复合膜",
                "剥离强度"
            ]
        }

        if industry in industry_map:
            expansions.extend(industry_map[industry])

        return list(set(expansions))