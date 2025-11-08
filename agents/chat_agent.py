from agents.data_agent import DataAgent
from agents.spec_agent import SpecAgent
from agents.mot_agent import MotAgent
from agents.insight_agent import InsightAgent
import re


class ChatAgent:
    """Main orchestrator combining all agents."""

    def __init__(self):
        self.data_agent = DataAgent()
        self.spec_agent = SpecAgent()
        self.mot_agent = MotAgent()
        self.insight_agent = InsightAgent()

    def handle_query(self, query: str):
        query_lower = query.lower()

        # --- Parse price (supports £20k or £20,000)
        price_match = re.search(r"£?(\d+(?:,\d{3})*\.?\d*)(k?)", query_lower)
        max_price = None
        if price_match:
            number = float(price_match.group(1).replace(",", ""))
            if price_match.group(2).lower() == 'k':
                number *= 1000
            max_price = number

        # --- Semantic search
        vehicles = self.data_agent.search_vehicles(query)

        # --- Apply filters
        if max_price is not None:
            vehicles = [v for v in vehicles if v.get("price", 0) <= max_price]

        if "heat pump" in query_lower:
            vehicles = [
                v for v in vehicles if self.spec_agent.has_heat_pump(v)]


        # --- If query mentions electric, filter accordingly
        if "electric" in query_lower:
            all_vehicles = self.data_agent.get_all_vehicles()  # Fetch from MongoDB directly
            evs = [v for v in all_vehicles if self.spec_agent.is_electric(v)]
            if not evs:
                return "No electric vehicles found."
            return self.insight_agent.summarize(query, evs)
            if not vehicles:
                return "No vehicles found matching your criteria."

        # --- MOT info requested
        if "mot" in query_lower:
            results = [f"{v.get('make')} {v.get('model')} MOT status: {self.mot_agent.get_mot_status(v)}"
                       for v in vehicles]
            return "\n".join(results)

        # --- Default: summarize
        return self.insight_agent.summarize(query, vehicles)
