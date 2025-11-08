class MotAgent:
    """Interprets MOT and tax data."""

    def get_mot_status(self, vehicle):
        mot_data = vehicle.get("VehicleMotData", [])
        if not mot_data:
            return "No MOT data found."
        latest = mot_data[0]
        return f"MOT valid until {latest.get('expiryDate', 'unknown')}."
