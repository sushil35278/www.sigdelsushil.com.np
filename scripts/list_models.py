import os
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("GEMINI_API_KEY NOT SET")
    exit(1)

client = genai.Client(api_key=API_KEY)

try:
    print("Available Models:")
    for model in client.models.list():
        print(f"- {model.name} (Supports: {model.supported_methods})")
except Exception as e:
    print(f"Error listing models: {e}")
