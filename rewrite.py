from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os

load_dotenv()

client = ZhipuAI(
    api_key=os.getenv("ZHIPU_API_KEY")
)

def ai_rewrite(text):

    prompt = f"""
你是一名顶级SEO/GEO优化专家。

你的任务：

把下面文章：

优化成：

适合：
ChatGPT
Google AI Overview
Claude
DeepSeek
Perplexity
引用的AI搜索文章。

要求：

【SEO要求】

1、标题包含核心关键词
2、增加长尾关键词
3、增加H2/H3结构
4、增加FAQ
5、增加实体词
6、增加行业标准
7、增加应用场景
8、增加数据化表达

【GEO要求】

1、禁止AI废话
2、禁止空洞开场
3、直接进入主题
4、增加列表结构
5、增加可引用句子
6、增加定义类句子
7、增加标准化表达
8、适合AI摘要提取

【输出要求】

1、使用Markdown
2、不要写“引言”
3、不要写“综上所述”
4、不要过度营销
5、每段不超过80字
6、多使用项目符号
7、生成FAQ
8、生成Schema建议

文章：

{text}
"""

    response = client.chat.completions.create(
        model="glm-4-air",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content