import json

# Load original dataset
with open("edges.json") as f:
    edges = json.load(f)

bidirectional_edges = []

# Add forward + reverse edges
for edge in edges:
    bidirectional_edges.append(edge)

    bidirectional_edges.append({
        "start": edge["end"],
        "end": edge["start"],
        "time": edge["time"],
        "distance": edge["distance"]
    })

# Remove duplicates
unique_edges = {}
for edge in bidirectional_edges:
    key = (edge["start"], edge["end"])
    unique_edges[key] = edge

final_edges = list(unique_edges.values())

# Save file
with open("edges_bidirectional.json", "w") as f:
    json.dump(final_edges, f, indent=2)

print(f"Done! Total edges: {len(final_edges)}")