import traceback
from datetime import datetime
from bson import ObjectId
from services.mongo_service import get_all_vehicles
from services.openai_service import get_embedding
import chromadb
import json

# -----------------------
# Initialize Chroma client (new API)
# -----------------------
client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_or_create_collection(name="vehicles")

def vehicle_to_text(vehicle: dict) -> str:
    """
    Convert Mongo vehicle record to a descriptive text string.
    """
    return (
        f"Registration: {vehicle.get('registration')}\n"
        f"Make/Model: {vehicle.get('make', '')} {vehicle.get('modelDescription', '')}\n"
        f"Year: {vehicle.get('regDate')}\n"
        f"Color: {vehicle.get('color')}\n"
        f"Mileage: {vehicle.get('mileage')}\n"
        f"Fuel: {vehicle.get('fuel', '')}\n"
        f"Price: {vehicle.get('price', '')}\n"
        f"Vehicle Type: {vehicle.get('vehicleType', '')}\n"
        f"Warranty: {vehicle.get('warrantyPackage', '')}\n"
    )

def sanitize_metadata(data: dict) -> dict:
    """
    Recursively converts MongoDB document fields into Chroma-safe metadata.
    (Removes or stringifies ObjectId, datetime, lists, dicts, etc.)
    """
    safe_meta = {}
    for k, v in data.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            safe_meta[k] = v
        elif isinstance(v, (datetime, ObjectId)):
            safe_meta[k] = str(v)
        elif isinstance(v, (list, dict)):
            # Convert small nested structures to JSON string; skip very large ones
            try:
                s = json.dumps(v)
                if len(s) < 1000:  # avoid huge blobs
                    safe_meta[k] = s
            except Exception:
                safe_meta[k] = str(v)
        else:
            safe_meta[k] = str(v)
    return safe_meta

def sync_mongo_to_chroma():
    """
    Sync all MongoDB vehicle records into ChromaDB with safe embeddings + metadata.
    """
    vehicles = get_all_vehicles()
    print(f"Found {len(vehicles)} vehicles in MongoDB. Starting sync...")

    success_count = failed_count = 0

    for vehicle in vehicles:
        try:
            reg = vehicle.get("registration")
            if not reg:
                print("Skipping vehicle with missing registration.")
                continue

            text = vehicle_to_text(vehicle)
            embedding = get_embedding(text)
            metadata = sanitize_metadata(vehicle)

            collection.upsert(
                ids=[reg],
                metadatas=[metadata],
                documents=[text],
                embeddings=[embedding]
            )

            print(f"✅ Synced vehicle {reg}")
            success_count += 1

        except Exception:
            print(f"❌ Failed to sync vehicle {vehicle.get('registration', 'UNKNOWN')}")
            traceback.print_exc()
            failed_count += 1

    print(f"\nSync complete. {success_count} succeeded, {failed_count} failed.")

if __name__ == "__main__":
    sync_mongo_to_chroma()
