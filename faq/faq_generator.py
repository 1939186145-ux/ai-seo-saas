from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os

load_dotenv()

client = ZhipuAI(
    api_key=os.getenv("ZHIPU_API_KEY")
)

def generate_faq(text):

    prompt = f"""
请基于下面文章：

生成5个SEO FAQ问题。

要求：

1、适合Google FAQ
2、适合AI搜索引用
3、简洁专业
4、输出Markdown

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