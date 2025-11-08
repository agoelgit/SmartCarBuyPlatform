import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str):
    """
    Get OpenAI embeddings for a given text.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def chat_completion(prompt: str, model: str = "gpt-4o-mini"):
    """
    Generate a conversational response using OpenAI chat models.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are Zorqk's helpful AI assistant that summarizes vehicle data clearly."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
