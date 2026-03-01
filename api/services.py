def build_analysis_context(request):
    return {
        "types": request.args.get("types", "[]"),
        "superficie": request.args.get("superficie", "[]"),
        "quantites": request.args.get("quantites", "[]"),
        "rendement": request.args.get("rendement", "[]"),
    }


def normalize_coordinates(raw_coordinates):
    if not isinstance(raw_coordinates, list) or not 3 <= len(raw_coordinates) <= 500:
        return None

    normalized = []
    for pair in raw_coordinates:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            return None

        try:
            latitude = float(pair[0])
            longitude = float(pair[1])
        except (TypeError, ValueError):
            return None

        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            return None

        normalized.append([latitude, longitude])

    return normalized
