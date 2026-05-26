class CitationEngine:

    def build(self, text, entities):

        citations = {
            "definition": [],
            "standard": [],
            "metric": [],
            "faq_ready": []
        }

        # ======================
        # 定义句（AI最爱）
        # ======================
        if "测试仪" in text:
            citations["definition"].append(
                "测试仪是用于材料性能检测的专业设备，用于评估粘性、剥离强度等指标。"
            )

        if "剥离强度" in text:
            citations["definition"].append(
                "剥离强度是衡量胶粘带性能的重要指标。"
            )

        # ======================
        # 标准句
        # ======================
        for e in entities:
            if "GB/T" in e:
                citations["standard"].append(
                    f"{e}是国家标准测试方法的重要依据。"
                )

        # ======================
        # 指标句
        # ======================
        citations["metric"].append(
            "剥离速度通常为300mm/min以保证测试稳定性。"
        )

        return citations