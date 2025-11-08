import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from services import mongo_service

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize persistent Chroma client
client = chromadb.PersistentClient(path="./data/chroma_db")

# Use existing collection if it exists, otherwise create with embedding
try:
    collection = client.get_collection("vehicles")  # <-- just load existing
except ValueError:
    # Collection doesn't exist yet, create it with OpenAI embeddings
    collection = client.create_collection(
        name="vehicles",
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name="text-embedding-3-small"
        )
    )

def sync_mongo_to_chroma():
    """
    Loads MongoDB vehicles into ChromaDB for semantic search.
    """
    vehicles = mongo_service.get_all_vehicles()
    print(f"Syncing {len(vehicles)} vehicles from MongoDB to ChromaDB...")

    for v in vehicles:
        try:
            vid = v.get("registration")
            if not vid:
                continue
            doc = f"{v.get('make')} {v.get('model')} {v.get('year')} {v.get('fuel')} {v.get('mot')}"
            collection.add(ids=[vid], documents=[doc])
        except Exception as e:
            print(f"Failed to sync {v.get('registration')}: {e}")

def search_vehicle(query: str, n: int = 3):
    """
    Semantic search for vehicles matching a free-text query.
    """
    try:
        results = collection.query(query_texts=[query], n_results=n)
        ids = results.get("ids", [[]])[0]
        if not ids:
            return []
        return [mongo_service.get_vehicle_by_reg(reg) for reg in ids]
    except Exception as e:
        print("Chroma search error:", e)
        return []
