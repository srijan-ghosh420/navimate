def get_user_preferences(query):
    query = query.lower()

    # Default weights
    weights = {
        "time": 1.0,
        "distance": 0.5,
        "cost": 0.5,
        "risk": 0.5,
        "comfort": 0.5
    }

    # Transport default
    transport = "car"

    # -------- INTENT --------
    if any(word in query for word in ["fast", "quick", "time"]):
        weights["time"] = 2.0

    if any(word in query for word in ["short", "distance"]):
        weights["distance"] = 2.0

    if any(word in query for word in ["cheap", "low cost", "budget"]):
        weights["cost"] = 2.0

    if any(word in query for word in ["safe", "avoid danger", "secure"]):
        weights["risk"] = 2.0

    if any(word in query for word in ["comfortable", "smooth", "less crowded"]):
        weights["comfort"] = 2.0

    # -------- TRANSPORT --------
    if "bus" in query:
        transport = "bus"
        weights["cost"] = max(weights["cost"], 1.5)

    elif "bike" in query or "motorcycle" in query:
        transport = "bike"
        weights["time"] = max(weights["time"], 1.5)

    elif "auto" in query or "rickshaw" in query:
        transport = "auto"

    elif "car" in query or "drive" in query:
        transport = "car"

    return weights, transport

def get_user_preferences(query):
    query = query.lower()

    weights = {
        "time": 1.0,
        "distance": 0.5,
        "cost": 0.5,
        "risk": 0.5,
        "comfort": 0.5,
        "crowd": 0.5,
        "tourism": 0.5
    }

    if any(word in query for word in ["fast", "quick", "time"]):
        weights["time"] = 2.0

    if any(word in query for word in ["short", "distance"]):
        weights["distance"] = 2.0

    if any(word in query for word in ["cheap", "low cost", "budget"]):
        weights["cost"] = 2.0

    if any(word in query for word in ["safe", "avoid danger", "secure"]):
        weights["risk"] = 2.0

    if any(word in query for word in ["less crowded", "avoid crowd"]):
        weights["crowd"] = 2.0

    if "tourist" in query or "scenic" in query:
        weights["tourism"] = 2.0

    if "comfortable" in query or "smooth" in query:
        weights["comfort"] = 2.0

    transport = "car"

    if "bus" in query:
        transport = "bus"
    elif "bike" in query:
        transport = "bike"

    return weights, transport


