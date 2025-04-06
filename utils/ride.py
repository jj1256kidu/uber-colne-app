def calculate_fare(distance):
    """Calculate ride fare based on distance"""
    base_fare = 5.0
    per_km_rate = 2.0
    return base_fare + (distance * per_km_rate)

def get_estimated_time(distance):
    """Calculate estimated ride time based on distance"""
    avg_speed = 30  # km/h
    return round((distance / avg_speed) * 60)  # Convert to minutes 
