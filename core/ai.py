import os
from openai import OpenAI

client = None

if os.getenv("ZHIPU_API_KEY"):
    client = OpenAI(
        api_key=os.getenv("ZHIPU_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )

def rewrite(text):

    if not client:
        return fallback(text)

    try:
        res = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{
                "role": "user",
                "content": f"优化为SEO/GEO结构化内容：\n{text}"
            }],
            max_tokens=800
        )
        return res.choices[0].message.content

    except:
        return fallback(text)


def fallback(text):
    return f"""# SEO优化版本（V11降级）

{text[:2000]}

---

## SEO建议
- 增强FAQ
- 增强结构化
- 增强实体
"""