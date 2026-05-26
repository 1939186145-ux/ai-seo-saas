import json

def generate_schema():

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage"
    }

    return json.dumps(
        schema,
        indent=2,
        ensure_ascii=False
    )