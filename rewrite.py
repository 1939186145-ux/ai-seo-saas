import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ZHIPU_API_KEY")

def ai_rewrite(text):

    # =========================
    # fallback（保证永不崩）
    # =========================
    if not API_KEY:
        return f"""# AI优化版本（降级模式）

{text}

## SEO优化建议
- 增加关键词密度
- 增加FAQ结构
- 增加实体词
"""

    try:
        # 延迟导入（关键：避免启动直接炸）
        from zhipuai import ZhipuAI

        client = ZhipuAI(api_key=API_KEY)

        prompt = f"""
你是一名顶级SEO/GEO优化专家。

将文章优化为适合AI搜索引擎引用的内容：

要求：
- SEO结构优化
- GEO可引用性增强
- Markdown输出
- FAQ结构
- 实体增强
- 每段≤80字

文章：
{text}
"""

        response = client.chat.completions.create(
            model="glm-4-air",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        # =========================
        # AI失败兜底（关键）
        # =========================
        return f"""# AI优化版本（降级模式）

{text}

## 系统提示
AI服务暂时不可用，已启用本地优化模式。

错误信息：{str(e)}

## SEO建议
- 增加结构化标题
- 增加FAQ
- 增加实体词
"""