import os
from openai import OpenAI

# =========================
# API KEY
# =========================
API_KEY = os.getenv("ZHIPU_API_KEY")

# =========================
# CLIENT
# =========================
client = None

if API_KEY:
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
    except:
        client = None


# =========================
# AI REWRITE
# =========================
def ai_rewrite(text):

    # 没有API
    if not client:
        return fallback_rewrite(text)

    try:

        prompt = f"""
你是一名SEO/GEO优化专家。

请把下面内容：

1. 改造成 AI Overview 友好
2. 增加 FAQ
3. 增加 H2/H3
4. 增加结构化内容
5. 增强实体覆盖
6. 提升可引用性
7. 输出 markdown

内容：

{text}
"""

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )

        return response.choices[0].message.content

    except Exception as e:

        print("AI Rewrite Error:", e)

        return fallback_rewrite(text)


# =========================
# 降级模式
# =========================
def fallback_rewrite(text):

    short = text[:3000]

    return f"""
# SEO优化版本（降级模式）

## 原始内容摘要

{short}

---

## SEO优化建议

- 增加FAQ模块
- 增加Schema结构化数据
- 提高实体覆盖率
- 增强标题层级
- 提高AI引用友好性

---

## GEO优化建议

- 增加短段落
- 使用列表结构
- 增加定义类句式
- 提高机器可读性
"""