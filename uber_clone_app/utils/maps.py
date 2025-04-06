import folium
import random
import numpy as np

def create_map(pickup=None, dropoff=None, driver_location=None):
    """Create a map with markers and route"""
    # Default center (New York City)
    center = [40.7128, -74.0060]
    zoom = 12
    
    # Create map
    m = folium.Map(location=center, zoom_start=zoom, tiles="cartodbpositron")
    
    # Add random cars
    if not driver_location:
        for _ in range(5):
            car_loc = [
                center[0] + random.uniform(-0.02, 0.02),
                center[1] + random.uniform(-0.02, 0.02)
            ]
            folium.Marker(
                car_loc,
                popup="Available",
                icon=folium.Icon(icon='car', prefix='fa')
            ).add_to(m)
    
    # Add markers if locations provided
    if pickup:
        folium.Marker(
            pickup,
            popup="Pickup",
            icon=folium.Icon(color='green')
        ).add_to(m)
    
    if dropoff:
        folium.Marker(
            dropoff,
            popup="Dropoff",
            icon=folium.Icon(color='red')
        ).add_to(m)
    
    if driver_location:
        folium.Marker(
            driver_location,
            popup="Driver",
            icon=folium.Icon(color='blue', icon='car', prefix='fa')
        ).add_to(m)
        
        # Draw route if we have both pickup and dropoff
        if pickup and dropoff:
            route = [pickup, driver_location, dropoff]
            folium.PolyLine(
                route,
                weight=2,
                color='blue',
                opacity=0.8
            ).add_to(m)
    
    return m

def update_driver_location(pickup, dropoff, progress):
    """Calculate driver's current location based on progress"""
    if not pickup or not dropoff:
        return None
        
    # Simple linear interpolation
    return [
        pickup[0] + (dropoff[0] - pickup[0]) * progress,
        pickup[1] + (dropoff[1] - pickup[1]) * progress
    ] 
