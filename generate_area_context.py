import json
import random

with open("edges_bidirectional.json") as f:
    edges = json.load(f)

# Define realistic urban categories
high_density = ["Esplanade", "Park Street", "Sealdah", "MG Road"]
medium_density = ["Salt Lake", "Ballygunge", "Ultadanga"]
low_density = ["Rajarhat", "Barasat", "Thakurpukur"]

tourist_hubs = ["Victoria Memorial", "Park Street", "Esplanade"]

area_context = []

for edge in edges:
    start = edge["start"]
    end = edge["end"]

    # -------- POPULATION --------
    if start in high_density:
        population = random.randint(150000, 300000)
    elif start in medium_density:
        population = random.randint(80000, 150000)
    else:
        population = random.randint(30000, 80000)

    # -------- POLICE --------
    police = int(population / random.randint(20000, 40000))

    # -------- HOSPITALS --------
    hospitals = int(population / random.randint(25000, 50000))

    # -------- GOVERNMENT --------
    govt = random.randint(1, 6) if start in high_density else random.randint(0, 3)

    # -------- TOURISM --------
    tourism = random.randint(5, 10) if start in tourist_hubs else random.randint(0, 4)

    entry = {
        "start": start,
        "end": end,
        "police": police,
        "hospitals": hospitals,
        "govt": govt,
        "population": population,
        "tourism": tourism
    }

    reverse_entry = {
        "start": end,
        "end": start,
        "police": police,
        "hospitals": hospitals,
        "govt": govt,
        "population": population,
        "tourism": tourism
    }

    area_context.append(entry)
    area_context.append(reverse_entry)

with open("area_context.json", "w") as f:
    json.dump(area_context, f, indent=4)

print("Area dataset generated:", len(area_context))