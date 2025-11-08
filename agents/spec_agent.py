class SpecAgent:
    """Analyzes vehicle specifications."""

    def has_heat_pump(self, vehicle):
        extras = str(vehicle.get("extras", "")).lower()
        model_desc = str(vehicle.get("modelDescription", "")).lower()
        return "heat pump" in extras or "heat pump" in model_desc

    def extract_specs(self, vehicle):
        return {
            "make": vehicle.get("make"),
            "model": vehicle.get("modelDescription"),
            "fuel": vehicle.get("fuel"),
            "co2": vehicle.get("co2"),
            "color": vehicle.get("color"),
            "mileage": vehicle.get("mileage"),
        }
    
    def is_electric(self, vehicle):
        fuel = str(vehicle.get("fuel", "")).lower()
        # Match common electric fuel types
        electric_keywords = ["electric", "ev", "battery"]
        return any(keyword in fuel for keyword in electric_keywords)
