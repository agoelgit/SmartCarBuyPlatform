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
        """
        Checks if vehicle is electric.
        Handles nested MongoDB structure: VehicleSmartData.VehicleDetails.Fuel
        """
        try:
            fuel = vehicle.get("VehicleSmartData", {}).get("VehicleDetails", {}).get("Fuel", "")
            if not fuel:
                fuel = vehicle.get("fuel", "")  # fallback
            fuel = str(fuel).lower()
            electric_keywords = ["electric", "ev", "battery"]
            return any(k in fuel for k in electric_keywords)
        except Exception:
            return False
