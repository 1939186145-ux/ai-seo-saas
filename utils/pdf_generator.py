from jinja2 import Template
from weasyprint import HTML
import os

PDF_DIR = "data/pdf"

def generate_pdf(report):

    os.makedirs(PDF_DIR, exist_ok=True)

    file_path = os.path.join(PDF_DIR, f"{report['id']}.pdf")

    data = report.get("data", {})
    base = data.get("base", {})
    scores = data.get("scores", {})
    entities = data.get("entities", [])
    rewrite = data.get("optimization", {}).get("rewrite", "")

    html = Template("""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; padding: 30px; }
            h1 { color: #2563eb; }
            .box { margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            td,th { border: 1px solid #ddd; padding: 8px; }
        </style>
    </head>

    <body>

    <h1>AI SEO SaaS 专业报告</h1>

    <div class="box">
        <b>URL:</b> {{ base.url }}<br>
        <b>关键词:</b> {{ base.query }}<br>
        <b>行业:</b> {{ base.industry }}
    </div>

    <div class="box">
        <h2>评分表</h2>
        <table>
            <tr><th>指标</th><th>分数</th></tr>
            {% for k,v in scores.items() %}
            <tr><td>{{k}}</td><td>{{v}}</td></tr>
            {% endfor %}
        </table>
    </div>

    <div class="box">
        <h2>实体</h2>
        {% for e in entities %}
            <div>{{e}}</div>
        {% endfor %}
    </div>

    <div class="box">
        <h2>AI优化内容</h2>
        <pre>{{ rewrite }}</pre>
    </div>

    </body>
    </html>
    """)

    html_out = html.render(
        base=base,
        scores=scores,
        entities=entities,
        rewrite=rewrite
    )

    HTML(string=html_out).write_pdf(file_path)

    return file_path