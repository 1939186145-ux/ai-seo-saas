import re

def seo_analysis(text):

    result = {}

    result["h2_count"] = text.count("##")

    result["faq"] = "FAQ" in text

    result["list_count"] = text.count("-")

    result["word_count"] = len(text)

    result["has_schema"] = "FAQPage" in text

    standards = re.findall(
        r'GB/T\s?\d+',
        text
    )

    result["standards"] = standards

    return result