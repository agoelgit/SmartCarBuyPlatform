# openai_service.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-large"  # 1536-dim

def get_embedding(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

def chat_completion(prompt: str, model: str = "gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are Zorqk's AI assistant that summarizes vehicle data."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
