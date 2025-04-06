import streamlit as st
import folium
from folium import plugins
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def create_map(pickup, dropoff, show_driver=False, driver_location=None):
    """Create a folium map with markers and route"""
    try:
        # Initialize geocoder
        geolocator = Nominatim(user_agent="ridesharepro")
        
        # Get coordinates
        pickup_loc = geolocator.geocode(pickup)
        dropoff_loc = geolocator.geocode(dropoff)
        
        if not pickup_loc or not dropoff_loc:
            raise ValueError("Could not geocode locations")
        
        # Calculate center point
        center_lat = (pickup_loc.latitude + dropoff_loc.latitude) / 2
        center_lon = (pickup_loc.longitude + dropoff_loc.longitude) / 2
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles="cartodbpositron"
        )
        
        # Add markers
        folium.Marker(
            [pickup_loc.latitude, pickup_loc.longitude],
            popup="Pickup",
            icon=folium.Icon(color='green', icon='info-sign'),
            tooltip="Pickup Location"
        ).add_to(m)
        
        folium.Marker(
            [dropoff_loc.latitude, dropoff_loc.longitude],
            popup="Dropoff",
            icon=folium.Icon(color='red', icon='info-sign'),
            tooltip="Dropoff Location"
        ).add_to(m)
        
        # Add driver marker if available
        if show_driver and driver_location:
            folium.Marker(
                driver_location,
                popup="Driver",
                icon=folium.Icon(color='blue', icon='car', prefix='fa'),
                tooltip="Driver Location"
            ).add_to(m)
        
        # Draw route
        route = generate_route(
            (pickup_loc.latitude, pickup_loc.longitude),
            (dropoff_loc.latitude, dropoff_loc.longitude)
        )
        
        folium.PolyLine(
            route,
            weight=3,
            color='blue',
            opacity=0.8
        ).add_to(m)
        
        # Add demand heatmap (simulated)
        add_demand_heatmap(m, center_lat, center_lon)
        
        return m
    
    except Exception as e:
        print(f"Error creating map: {e}")
        # Return default map centered on New York
        return folium.Map(
            location=[40.7128, -74.0060],
            zoom_start=12,
            tiles="cartodbpositron"
        )

def generate_route(start, end):
    """Generate a route between two points
    For demo, creates a slightly curved path between points"""
    
    # Create intermediate points for curved path
    num_points = 10
    lat_diff = end[0] - start[0]
    lon_diff = end[1] - start[1]
    
    # Generate curve using sine function
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        lat = start[0] + t * lat_diff
        lon = start[1] + t * lon_diff
        # Add sine curve deviation
        if 0 < t < 1:
            deviation = np.sin(t * np.pi) * 0.01
            lon += deviation
        points.append([lat, lon])
    
    return points

def add_demand_heatmap(m, center_lat, center_lon):
    """Add a simulated demand heatmap to the map"""
    
    # Generate random points around center
    num_points = 100
    radius = 0.05  # Roughly 5km
    
    points = []
    for _ in range(num_points):
        lat = center_lat + np.random.normal(0, radius/2)
        lon = center_lon + np.random.normal(0, radius/2)
        intensity = np.random.random()  # Random intensity
        points.append([lat, lon, intensity])
    
    # Add heatmap layer
    plugins.HeatMap(points).add_to(m) 
