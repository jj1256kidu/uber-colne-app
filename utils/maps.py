import streamlit as st
import folium
from folium import plugins
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import random

def create_map(pickup=None, dropoff=None, driver_location=None):
    """Create a map with markers and route"""
    
    # Default center (New York City)
    center = [40.7128, -74.0060]
    
    # Create map
    m = folium.Map(
        location=center,
        zoom_start=13,
        tiles="cartodbpositron"
    )
    
    # Add pickup and dropoff markers
    if pickup and dropoff:
        geolocator = Nominatim(user_agent="uber_clone")
        
        # Add pickup marker
        pickup_loc = geolocator.geocode(pickup)
        folium.Marker(
            [pickup_loc.latitude, pickup_loc.longitude],
            popup="Pickup",
            icon=folium.Icon(color='green')
        ).add_to(m)
        
        # Add dropoff marker
        dropoff_loc = geolocator.geocode(dropoff)
        folium.Marker(
            [dropoff_loc.latitude, dropoff_loc.longitude],
            popup="Dropoff",
            icon=folium.Icon(color='red')
        ).add_to(m)
        
        # Draw route
        route_coords = [
            [pickup_loc.latitude, pickup_loc.longitude],
            [dropoff_loc.latitude, dropoff_loc.longitude]
        ]
        folium.PolyLine(
            route_coords,
            weight=3,
            color='blue',
            opacity=0.8
        ).add_to(m)
    
    # Add driver marker
    if driver_location:
        folium.Marker(
            driver_location,
            popup="Driver",
            icon=folium.Icon(color='blue', icon='car', prefix='fa')
        ).add_to(m)
    
    return m

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

def update_driver_location():
    """Simulate driver movement"""
    # Random location near NYC
    return [
        40.7128 + random.uniform(-0.01, 0.01),
        -74.0060 + random.uniform(-0.01, 0.01)
    ]

def show_driver_assignment():
    """Show driver assignment and live tracking"""
    
    # Update driver location
    if 'driver_location' not in st.session_state.current_ride:
        st.session_state.current_ride['driver_location'] = update_driver_location()
    
    # Show map with route and driver
    m = create_map(
        pickup=st.session_state.current_ride['pickup'],
        dropoff=st.session_state.current_ride['dropoff'],
        driver_location=st.session_state.current_ride['driver_location']
    )
    folium_static(m, width=1200, height=800)
    
    # Driver info card
    driver = st.session_state.current_ride['driver']
    st.markdown(f"""
        <div class="driver-info">
            <img src="{driver['photo']}" class="driver-photo">
            <div>
                <h3>{driver['name']}</h3>
                <div>{driver['car']} • {driver['plate']}</div>
                <div class="rating">{'⭐' * int(driver['rating'])}</div>
            </div>
            <div style="margin-left: auto">
                <h2>ETA: {st.session_state.current_ride['eta']} min</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_ride_completed():
    """Show ride completion and rating screen"""
    
    st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <h1>🎉 Ride Completed!</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Rating and feedback
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="uber-card">
                <h3>Rate your ride</h3>
                <div class="rating" style="font-size: 40px; margin: 20px 0;">
                    ⭐⭐⭐⭐⭐
                </div>
                <textarea placeholder="Additional feedback (optional)" 
                          style="width: 100%; padding: 10px; border-radius: 10px; margin: 10px 0;"></textarea>
                <button style="width: 100%; padding: 15px; border-radius: 30px; background: black; color: white; border: none; margin-top: 20px;">
                    Submit Rating
                </button>
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main app logic"""
    
    if st.session_state.page == 'booking':
        show_booking_page()
    elif st.session_state.page == 'driver_assigned':
        show_driver_assignment()
    elif st.session_state.page == 'completed':
        show_ride_completed()

if __name__ == "__main__":
    main() 
