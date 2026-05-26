from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    url = data.get("url")
    query = data.get("query")

    result = {
        "success": True,

        "scores": {
            "geo": 78,
            "citation": 92,
            "ranking": 88
        },

        "entities": [
            "SEO",
            "GEO",
            "AI优化",
            "Schema"
        ],

        "rewrite": """
# AI SEO优化标题

## 自动生成内容
这是V5商业版AI SEO系统。
""",

        "trend": {
            "dates": ["Mon","Tue","Wed","Thu","Fri"],
            "geo": [30,40,50,60,78],
            "ranking": [20,35,50,70,88]
        }
    }

    return jsonify(result)