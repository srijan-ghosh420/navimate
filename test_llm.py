from google import genai
import os
import dotenv

dotenv.load_dotenv()
current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, '.env')
dotenv.load_dotenv(dotenv_path=env_file_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

res = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(res.text)