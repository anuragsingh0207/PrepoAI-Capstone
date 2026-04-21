import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print("Fetching available models...")
try:
    models = list(genai.list_models())
    found_embedding_model = False
    for m in models:
        if 'embedContent' in m.supported_generation_methods:
            print(f"✅ Available Embedding Model: {m.name}")
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available Generation Model: {m.name}")


except Exception as e:
    print(f"❌ Error listing models: {e}")
