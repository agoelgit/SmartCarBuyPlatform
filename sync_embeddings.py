from services.mongo_service import get_all_vehicles
from services.openai_service import get_embedding
import chromadb
import json

client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_or_create_collection(name="vehicles")

def vehicle_to_text(vehicle):
    return f"{vehicle.get('make','')} {vehicle.get('modelDescription','')} {vehicle.get('fuel','')} {vehicle.get('regDate','')}"

def sanitize_metadata(data):
    safe_meta = {}
    for k, v in data.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            safe_meta[k] = v
        else:
            safe_meta[k] = str(v)
    return safe_meta

def sync_mongo_to_chroma():
    vehicles = get_all_vehicles()
    print(f"Syncing {len(vehicles)} vehicles...")

    for v in vehicles:
        vid = v.get("registration")
        if not vid:
            continue

        text = vehicle_to_text(v)
        embedding = get_embedding(text)
        metadata = sanitize_metadata(v)

        collection.upsert(
            ids=[vid],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    print("Sync complete.")
