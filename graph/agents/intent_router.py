def detect_intent(query):

    query = query.lower()

    if any(word in query for word in [
        "risk",
        "risky",
        "risk score"
    ]):
        return "RISK"

    elif any(word in query for word in [
        "monte",
        "simulation",
        "probability",
        "p50",
        "p80",
        "p95"
    ]):
        return "MONTE_CARLO"

    elif any(word in query for word in [
        "resource",
        "resources",
        "overloaded",
        "bottleneck"
    ]):
        return "RESOURCE"

    elif any(word in query for word in [
        "delay",
        "slip",
        "impact"
    ]):
        return "DELAY"

    return "UNKNOWN"