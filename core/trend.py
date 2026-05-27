def build_trend(current_geo, current_citation, current_ranking):

    return {
        "dates": ["D1","D2","D3","D4","D5"],
        "geo": [60, 65, 70, 75, current_geo],
        "citation": [55, 60, 68, 75, current_citation],
        "ranking": [50, 58, 66, 72, current_ranking]
    }