import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["zorqk"]
vehicles = db["vehicles"]

def get_vehicle_by_reg(reg: str):
    return vehicles.find_one({"registration": reg.upper()})

def get_all_vehicles():
    return list(vehicles.find({}))

def search_by_make_model(make: str, model: str):
    return list(vehicles.find({
        "make": make.upper(),
        "model": {"$regex": model, "$options": "i"}
    }))
