import json
import random

# Load your edges
with open("edges_bidirectional.json") as f:
    edges = json.load(f)

context_data = []

# Define area categories (realistic zoning)
high_traffic_zones = [
    "Esplanade", "Park Street", "Sealdah", "MG Road",
    "Chandni Chowk", "Central"
]

medium_traffic_zones = [
    "Salt Lake", "Ultadanga", "Ballygunge",
    "Rabindra Sadan", "Phoolbagan"
]

low_traffic_zones = [
    "Rajarhat", "New Town", "Barasat",
    "Madhyamgram", "Thakurpukur"
]

for edge in edges:
    start = edge["start"]
    end = edge["end"]
    distance = edge["distance"]
    time = edge["time"]

    # -------- TRAFFIC --------
    if start in high_traffic_zones or end in high_traffic_zones:
        traffic = round(random.uniform(1.4, 2.0), 2)
    elif start in medium_traffic_zones or end in medium_traffic_zones:
        traffic = round(random.uniform(1.1, 1.5), 2)
    else:
        traffic = round(random.uniform(0.8, 1.2), 2)

    # -------- SAFETY --------
    if start in high_traffic_zones:
        safety = round(random.uniform(0.7, 0.9), 2)
    elif start in medium_traffic_zones:
        safety = round(random.uniform(0.5, 0.7), 2)
    else:
        safety = round(random.uniform(0.3, 0.6), 2)

    # -------- COST --------
    cost = round(distance * random.uniform(8, 15), 2)

    # -------- COMFORT --------
    comfort = round(1 / traffic + random.uniform(0, 0.2), 2)
    comfort = min(comfort, 1.0)

    entry = {
    "start": start,
    "end": end,
    "traffic": traffic,
    "safety": safety,
    "cost": cost,
    "comfort": comfort
    }

    reverse_entry = {
        "start": end,
        "end": start,
        "traffic": traffic,
        "safety": safety,
        "cost": cost,
        "comfort": comfort
    }

    context_data.append(entry)
    context_data.append(reverse_entry)

# Save file
with open("context_data.json", "w") as f:
    json.dump(context_data, f, indent=4)

print("Context dataset generated:", len(context_data))