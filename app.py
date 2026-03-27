from flask import Flask, request, jsonify
from pymongo import MongoClient
from collections import defaultdict
import heapq
from intent import get_user_preferences
from llm import generate_llm_response, parse_query

TRANSPORT_MULTIPLIERS = {
    "car": 1.0,
    "bike": 0.8,
    "auto": 1.2,
    "bus": 1.5
}

app = Flask(__name__)

# Load data
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["kolkata_navigation"]
collection = db["edges"]

edges = list(collection.find({}, {"_id": 0}))

# Build graph
graph = defaultdict(list)
for edge in edges:
    graph[edge["start"]].append(
        (edge["end"], edge["distance"], edge["time"])
    )

print("Graph loaded:", len(graph), "nodes")

context_collection = db["context"]
context_data = list(context_collection.find({}, {"_id": 0}))

context_map = {
    (item["start"], item["end"]): item
    for item in context_data
}

print("Context loaded:", len(context_map))

area_collection = db["area_context"]
area_data = list(area_collection.find({}, {"_id": 0}))

area_map = {
    (item["start"], item["end"]): item
    for item in area_data
}

print("Area context loaded:", len(area_map))


def compute_cost(dist, time, context, area, weights, transport):
    multiplier = TRANSPORT_MULTIPLIERS.get(transport, 1.0)

    # Existing
    traffic = context.get("traffic", 1.0)
    safety = context.get("safety", 0.5)
    cost_money = context.get("cost", 50)
    comfort = context.get("comfort", 0.5)

    # New variables
    police = area.get("police", 1)
    hospitals = area.get("hospitals", 1)
    govt = area.get("govt", 1)
    population = area.get("population", 50000)
    tourism = area.get("tourism", 1)

    # Derived metrics (MULTIVARIATE ANALYSIS)
    safety_score = (police + hospitals + govt) / 10
    congestion_score = population / 100000
    tourism_score = tourism / 10

    adjusted_time = time * traffic * multiplier

    total_cost = (
        weights["time"] * adjusted_time +
        weights["distance"] * dist +
        weights["cost"] * cost_money +
        weights["risk"] * (1 - safety_score) +
        weights["comfort"] * (1 - comfort) +
        weights["crowd"] * congestion_score +
        weights["tourism"] * tourism_score
    )

    return total_cost

# Dijkstra
import heapq

def dijkstra(graph, start, end, weights, transport,
             context_map, area_map,constraints):

    pq = [(0, start, [])]  # (total_cost, current_node, path)
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        # ✅ Destination reached
        if node == end:
            return path, cost

        for neighbor, dist, time in graph[node]:

            if neighbor in visited:
                continue

            # -------- FETCH DATA --------
            context = context_map.get((node, neighbor), {})
            area = area_map.get((node, neighbor), {})

            police = area.get("police", 0)
            hospitals = area.get("hospitals", 0)
            tourism = area.get("tourism", 0)
            population = area.get("population", 0)

            # ✅ SAFE FILTERING

            if police < constraints["police_min"]:
                continue

            if hospitals < constraints["hospitals_min"]:
                continue

            if tourism < constraints["tourism_min"]:
                continue

            # 🚨 SAFE POPULATION CHECK
            if population > constraints["population_max"]:
                continue

            # 🚨 APPLY MULTIVARIATE CONSTRAINTS

            if police < constraints.get("police_min", 0):
                continue

            if hospitals < constraints.get("hospitals_min", 0):
                continue

            if tourism < constraints.get("tourism_min", 0):
                continue

            if population > constraints.get("population_max", float("inf")):
                continue


            # -------- BASE VALUES --------
            traffic = context.get("traffic", 1.0)
            safety = context.get("safety", 0.5)
            cost_money = context.get("cost", 50)
            comfort = context.get("comfort", 0.5)

            police = area.get("police", 1)
            hospitals = area.get("hospitals", 1)
            govt = area.get("govt", 1)
            population = area.get("population", 50000)
            tourism = area.get("tourism", 1)

            # -------- DERIVED FEATURES (MULTIVARIATE) --------
            safety_score = (police + hospitals + govt) / 10
            congestion_score = population / 100000
            tourism_score = tourism / 10

            # -------- TRANSPORT EFFECT --------
            multiplier = TRANSPORT_MULTIPLIERS.get(transport, 1.0)
            adjusted_time = time * traffic * multiplier

            # -------- FINAL COST FUNCTION --------
            total_edge_cost = (
                weights["time"] * adjusted_time +
                weights["distance"] * dist +
                weights["cost"] * cost_money +
                weights["risk"] * (1 - safety_score) +
                weights["comfort"] * (1 - comfort) +
                weights["crowd"] * congestion_score +
                weights["tourism"] * tourism_score
            )

            # -------- PUSH INTO PQ --------
            heapq.heappush(
                pq,
                (cost + total_edge_cost, neighbor, path)
            )

    return None, float("inf")


@app.route("/")
def home():
    return "Server is running"


@app.route("/route", methods=["POST"])
def get_route():
    try:
        data = request.get_json(force=True)

        query = data["query"]

        parsed = parse_query(query)

        start = parsed["start"]
        end = parsed["end"]
        transport = parsed.get("transport", "car")
        weights = parsed.get("preferences", {})
        constraints = parsed.get("constraints", {})

        # 🔥 Normalize all constraints safely
        constraints["police_min"] = constraints.get("police_min") or 0
        constraints["hospitals_min"] = constraints.get("hospitals_min") or 0
        constraints["tourism_min"] = constraints.get("tourism_min") or 0

        # 🚨 VERY IMPORTANT FIX
        pop_max = constraints.get("population_max")

        if pop_max is None or pop_max == 0:
            constraints["population_max"] = float("inf")
        else:
            constraints["population_max"] = pop_max



        weights, transport = get_user_preferences(query)
        # If no constraints specified → remove them completely
        if not any(constraints.values()):
            constraints = {}

        
        path, cost = dijkstra(
            graph,
            start,
            end,
            weights,
            transport,
            context_map,
            area_map,
            constraints
        )

        llm_explanation = generate_llm_response(
            query,
            path,
            cost,
            weights,
            transport
        )

        if path is None:
            return jsonify({
                "error": "No route satisfies all constraints. Try relaxing them."
            })

        print("PARSED:", parsed)
        print("CLEANED CONSTRAINTS:", constraints)


        return jsonify({
            "path": path,
            "cost": cost,
            "weights": weights,
            "transport": transport,
            "llm_explanation": llm_explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)