from pymongo import MongoClient

def load_edges():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["kolkata_navigation"]
    collection = db["edges"]

    edges = list(collection.find({}, {"_id": 0}))
    return edges

if __name__ == "__main__":
    data = load_edges()
    print(data[:5])  # preview


from collections import defaultdict

def build_graph(edges):
    graph = defaultdict(list)

    for edge in edges:
        start = edge["start"]
        end = edge["end"]
        distance = edge["distance"]
        time = edge["time"]

        graph[start].append((end, distance, time))

    return graph

edges = load_edges()
graph = build_graph(edges)

print(graph["Howrah"])

import heapq

def dijkstra(graph, start, end, mode="distance"):
    pq = [(0, start, [])]  # (cost, node, path)
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return path, cost

        for neighbor, distance, time in graph[node]:
            if neighbor not in visited:
                weight = distance if mode == "distance" else time
                heapq.heappush(pq, (cost + weight, neighbor, path))

    edges = load_edges()
    graph = build_graph(edges)

    path, cost = dijkstra(graph, "Howrah", "New Town", mode="distance")

    print("Path:", path)
    print("Total Cost:", cost)
    mode="distance"
    mode="time"



    return None, float("inf")

