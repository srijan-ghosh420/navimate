# 🚦 Intelligent Navigation System (Kolkata)

## 📌 Overview

This project is a **smart, multi-objective navigation system** designed for urban routing in Kolkata.

Unlike traditional shortest-path systems, it integrates:

* Multi-objective optimization (time, cost, safety, comfort, crowd, tourism)
* Natural language query understanding
* Socio-spatial and infrastructure-aware routing
* LLM-based explanation generation (Gemini)

---

## 🎯 Features

* ✅ Natural language queries
  *Example*:
  `Give me the fastest route from Howrah to New Town with at least 3 police stations`

* ✅ Multi-objective Dijkstra algorithm

* ✅ Context-aware routing (traffic, safety, cost, comfort)

* ✅ Area intelligence (police, hospitals, population, tourism)

* ✅ Constraint-based routing (e.g., minimum police stations)

* ✅ LLM-generated human explanations

---

## 🧠 System Architecture

```
User Query (Natural Language)
        ↓
Query Parser (LLM-based)
        ↓
Intent Engine (weights extraction)
        ↓
Routing Engine (Multi-objective Dijkstra)
        ↓
Constraint Filtering
        ↓
Top-K Routes (optional)
        ↓
LLM Explanation Engine
```

---

## 📂 Project Structure

```
.
├── app.py                  # Flask API server
├── intent.py               # Converts preferences → weights
├── query_parser.py         # Extracts structured data from query
├── llm.py                  # Gemini integration
├── generate_context.py     # Generates traffic/safety data
├── generate_area_context.py# Generates infrastructure data
├── load_graph.py           # Graph utility
├── edges_bidirectional.json# Road network dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone repo

```
git clone https://github.com/your-username/navimate.git
cd navimate
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Running the Server

```
python app.py
```

Server runs on:

```
http://127.0.0.1:5000
```

---

## 📡 API Usage

### Endpoint:

```
POST /route
```

### Input:

```json
{
  "query": "Give me the safest and least crowded route from Howrah to New Town with at least 3 police stations"
}
```

---

### Output:

```json
{
  "path": ["Howrah", "Esplanade", "...", "New Town"],
  "cost": 123.4,
  "transport": "car",
  "weights": {...},
  "llm_explanation": "This route prioritizes safety and avoids crowded areas..."
}
```

---

## 🧮 Cost Function

The routing algorithm minimizes:

```
Total Cost =
w_time * adjusted_time +
w_distance * distance +
w_cost * cost +
w_risk * (1 - safety) +
w_comfort * (1 - comfort) +
w_crowd * congestion +
w_tourism * (1 - tourism)
```

---

## 🧪 Future Improvements

* 🔄 Real-time traffic integration
* 🌦 Weather-aware routing
* 📊 Route comparison (Top-K paths)
* 🧠 Learning user preferences
* 🗺 Visualization dashboard

---

## 🏁 Status

✔ Core system complete
✔ Multi-dataset integration
✔ LLM explanation working
🚧 Advanced features in progress

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📜 License

MIT License
