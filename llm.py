from google import genai
import os,json, re
from dotenv import load_dotenv

current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, '.env')
load_dotenv(dotenv_path=env_file_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_llm_response(query, path, cost, weights, transport):
    prompt = f"""
You are an intelligent navigation assistant.
DO NOT HALLUCINATE. ONLY RESPOND BASED ON THE GIVEN DATA.

User Query:
{query}

Computed Route:
{path}

Total Cost:
{cost}

Transport Mode:
{transport}

Weights:
{weights}

Explain clearly:
1. Why this route was chosen
2. Key influencing factors (traffic, safety, cost, crowd, tourism)
3. Trade-offs involved

Keep it concise and natural.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text




def parse_query(query):
    prompt = f"""
Extract structured data from this navigation query.

Query:
{query}

Return ONLY valid JSON. No explanation. No text.

Format:
{{
  "start": "...",
  "end": "...",
  "transport": "car",
  "preferences": {{
    "time": float,
    "distance": float,
    "cost": float,
    "risk": float,
    "comfort": float,
    "crowd": float,
    "tourism": float
  }},
  "constraints": {{
    "police_min": int,
    "hospitals_min": int,
    "tourism_min": int,
    "population_max": int
  }}
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # 🔥 Extract JSON using regex
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in LLM response")

    json_text = match.group(0)

    return json.loads(json_text)