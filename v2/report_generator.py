def generate_report(url, query, data):

    report = f"""
# 🚀 AI SEO SaaS V2 分析报告

## 📌 输入信息
- URL: {url}
- Query: {query}

---

## 📊 核心评分
- GEO Score: {data['geo_score']}
- Citation Score: {data['citation_score']}
- Ranking Score: {data['ranking_score']}

---

## 🧠 实体分析
{data['entities']}

---

## 📈 SEO优化建议

1. 增加H2结构
2. 增加FAQ模块
3. 增强GB/T标准引用
4. 提高实体密度
5. 增加定义句（“是指”结构）

---

## 🚀 AI优化后内容
{data['rewrite']}
"""

    return report