# data_agent.py
from services import db_service, mongo_service

class DataAgent:
    """Handles vehicle retrieval and search."""

    def search_vehicles(self, query: str):
        # Semantic search via ChromaDB
        return db_service.search_vehicle(query)

    def filter_by_price(self, max_price: float):
        """Filter vehicles from MongoDB cheaper than max_price"""
        vehicles = mongo_service.get_all_vehicles()
        result = []

        for v in vehicles:
            price = v.get("price", 0)
            try:
                # Convert to float, remove £ and commas if present
                price = float(str(price).replace("£", "").replace(",", ""))
                if price <= max_price:
                    result.append(v)
            except (ValueError, TypeError):
                # Skip vehicles with invalid price
                continue

        return result

    def get_all_vehicles(self):
        """Return all vehicles from MongoDB"""
        return mongo_service.get_all_vehicles()
