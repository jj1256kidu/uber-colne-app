import folium
from geopy.geocoders import Nominatim

def create_map(pickup, dropoff, show_driver=False, driver_location=None):
    """Create a folium map with pickup and dropoff markers"""
    geolocator = Nominatim(user_agent="ridesharepro")
    
    try:
        pickup_loc = geolocator.geocode(pickup)
        dropoff_loc = geolocator.geocode(dropoff)
        
        # Create map centered between pickup and dropoff
        center_lat = (pickup_loc.latitude + dropoff_loc.latitude) / 2
        center_lon = (pickup_loc.longitude + dropoff_loc.longitude) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        # Add markers
        folium.Marker(
            [pickup_loc.latitude, pickup_loc.longitude],
            popup="Pickup",
            icon=folium.Icon(color='green')
        ).add_to(m)
        
        folium.Marker(
            [dropoff_loc.latitude, dropoff_loc.longitude],
            popup="Dropoff",
            icon=folium.Icon(color='red')
        ).add_to(m)
        
        if show_driver and driver_location:
            folium.Marker(
                driver_location,
                popup="Driver",
                icon=folium.Icon(color='blue')
            ).add_to(m)
        
        # Draw route line
        route_coords = generate_route(
            (pickup_loc.latitude, pickup_loc.longitude),
            (dropoff_loc.latitude, dropoff_loc.longitude)
        )
        folium.PolyLine(
            route_coords,
            weight=2,
            color='blue',
            opacity=0.8
        ).add_to(m)
        
        return m
    
    except:
        # Return default map centered on New York
        return folium.Map(location=[40.7128, -74.0060], zoom_start=12)

def generate_route(start, end):
    """Generate a simple route between two points"""
    # For demo, just return direct line coordinates
    return [start, end] 
