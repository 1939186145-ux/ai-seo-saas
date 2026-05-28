import os
from zhipuai import ZhipuAI

# =========================
# API KEY
# =========================
API_KEY = os.getenv("ZHIPU_API_KEY")

# =========================
# CLIENT（稳定版）
# =========================
client = None

if API_KEY:
    try:
        client = ZhipuAI(api_key=API_KEY)
    except Exception as e:
        print("[rewrite] client init failed:", e)
        client = None


# =========================
# MAIN REWRITE
# =========================
def ai_rewrite(text):

    # =========================
    # 防空
    # =========================
    if not text or len(text.strip()) == 0:
        return fallback_rewrite("空内容")

    if not client:
        return fallback_rewrite(text)

    try:

        # =========================
        # prompt压缩（避免公网超时）
        # =========================
        safe_text = text[:2500]

        prompt = f"""
你是顶尖SEO+GEO优化专家。

任务：
- AI Overview友好
- 增强结构（H2/H3）
- 增加FAQ
- 提升可引用性
- 增强实体覆盖

要求：
- 输出Markdown
- 不要编造事实
- 保持专业

内容：
{safe_text}
"""

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )

        content = response.choices[0].message.content

        # =========================
        # 防空返回
        # =========================
        if not content or len(content.strip()) < 20:
            return fallback_rewrite(text)

        return content

    except Exception as e:
        print("[rewrite] AI error:", e)
        return fallback_rewrite(text)


# =========================
# 降级模式（增强版）
# =========================
def fallback_rewrite(text):

    short = text[:1500]

    return f"""
# SEO优化版本（降级模式）

## 原始内容摘要

{short}

---

## SEO优化结构建议

### H2：内容优化方向
- 增加FAQ模块（提升AI可引用性）
- 增加H2/H3层级结构
- 优化段落长度（<80字）

### H2：GEO优化建议
- 使用短句与列表结构
- 增加定义型语句（What is / How / Why）
- 提高机器可读性

### H2：实体增强建议
- 增加行业关键词
- 增加品牌/设备/标准名称
- 提升知识图谱覆盖

### H2：结构化数据建议
- Schema Product
- Schema FAQ
- Schema Article

---

## 注意
当前AI服务不可用，已进入本地降级模式。
"""