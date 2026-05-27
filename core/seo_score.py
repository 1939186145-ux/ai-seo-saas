def calc_scores(text, entities):

    geo = min(len(text) / 100, 100)

    citation = min(len(set(entities)) * 3, 100)

    ranking = (geo * 0.4 + citation * 0.6)

    return {
        "geo": round(geo, 2),
        "citation": round(citation, 2),
        "ranking": round(ranking, 2)
    }