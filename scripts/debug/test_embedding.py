import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv() # Load your API key

# 1. Setup the Embedding Model
# Changing model to text-embedding-004 as per conversation
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 2. Your Test Text
text = "Anurag is the team lead."

# 3. Turn it into numbers
vector = embeddings.embed_query(text)

# 4. Print the result
print(f"Text: {text}")
print(f"Vector Length: {len(vector)}")
print(f"First 5 numbers: {vector[:5]}")