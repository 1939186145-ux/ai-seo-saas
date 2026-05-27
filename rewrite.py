import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# SAFE INIT CLIENT
# =========================
def get_client():
    try:
        from zhipuai import ZhipuAI

        api_key = os.getenv("ZHIPU_API_KEY")

        if not api_key:
            return None

        return ZhipuAI(api_key=api_key)

    except Exception:
        return None


# =========================
# CORE FUNCTION
# =========================
def ai_rewrite(text):

    # =========================
    # PROMPT（保留你的原逻辑）
    # =========================
    prompt = f"""
你是一名顶级SEO/GEO优化专家。

你的任务：

把下面文章优化成适合AI搜索引擎引用的内容。

要求：

【SEO】
- 标题关键词优化
- 长尾关键词
- H2/H3结构
- FAQ
- 实体词
- 行业标准
- 应用场景
- 数据化表达

【GEO】
- 禁止废话
- 直接进入主题
- 列表结构
- 可引用句子
- 定义类表达
- 标准化表达

【输出】
- Markdown格式
- 不要“引言”
- 不要“综上所述”
- 每段<80字
- 必须FAQ
- 必须Schema建议

文章：
{text}
"""

    # =========================
    # TRY AI
    # =========================
    client = get_client()

    if client:
        try:
            response = client.chat.completions.create(
                model="glm-4-air",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            # AI失败 fallback
            return fallback_rewrite(text, str(e))

    # =========================
    # NO CLIENT fallback
    # =========================
    return fallback_rewrite(text, "no_api_key_or_client")


# =========================
# FALLBACK（防崩核心）
# =========================
def fallback_rewrite(text, reason=""):

    return f"""
# SEO优化版本（降级模式）

## 原始内容
{text}

---

## SEO优化建议

- 增加关键词结构
- 增加FAQ模块
- 增加Schema结构化数据
- 增加实体词覆盖
- 优化H2/H3标题结构
- 提升可引用性（AI Overview友好）

---

## GEO优化建议

- 使用短段落（<80字）
- 增加列表结构
- 避免空话
- 增加定义类语句
- 提升机器可读性

---

## 系统状态
AI服务当前不可用或网络异常

原因：{reason}
"""