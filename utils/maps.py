import streamlit as st
import folium
from folium import plugins
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import random
import math
import time
from streamlit_folium import folium_static

def create_map(pickup=None, dropoff=None, driver_progress=0):
    """Create a map with animated driver movement"""
    try:
        # Default center (New York City)
        center = [40.7128, -74.0060]
        
        if pickup and dropoff:
            geolocator = Nominatim(user_agent="uber_clone")
            
            # Get coordinates
            pickup_loc = geolocator.geocode(pickup)
            dropoff_loc = geolocator.geocode(dropoff)
            
            if pickup_loc and dropoff_loc:
                # Update center
                center = [
                    (pickup_loc.latitude + dropoff_loc.latitude) / 2,
                    (pickup_loc.longitude + dropoff_loc.longitude) / 2
                ]
                
                # Create map
                m = folium.Map(
                    location=center,
                    zoom_start=13,
                    tiles="cartodbpositron"
                )
                
                # Add pickup marker
                folium.Marker(
                    [pickup_loc.latitude, pickup_loc.longitude],
                    popup="Pickup",
                    icon=folium.Icon(color='green', icon='info-sign'),
                    tooltip="Pickup Location"
                ).add_to(m)
                
                # Add dropoff marker
                folium.Marker(
                    [dropoff_loc.latitude, dropoff_loc.longitude],
                    popup="Dropoff",
                    icon=folium.Icon(color='red', icon='info-sign'),
                    tooltip="Dropoff Location"
                ).add_to(m)
                
                # Create route points
                route_points = create_route_points(
                    [pickup_loc.latitude, pickup_loc.longitude],
                    [dropoff_loc.latitude, dropoff_loc.longitude]
                )
                
                # Draw route line
                folium.PolyLine(
                    route_points,
                    weight=3,
                    color='blue',
                    opacity=0.8
                ).add_to(m)
                
                # Add driver marker if progress is provided
                if driver_progress > 0:
                    current_point_index = int(driver_progress * (len(route_points) - 1))
                    if current_point_index < len(route_points):
                        driver_position = route_points[current_point_index]
                        folium.Marker(
                            driver_position,
                            icon=create_car_icon(),
                            tooltip="Driver"
                        ).add_to(m)
                
                return m
        
        # Return default map if no valid locations
        return folium.Map(location=center, zoom_start=12, tiles="cartodbpositron")
    
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return folium.Map(location=[40.7128, -74.0060], zoom_start=12)

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
    """Update driver location for simulation"""
    if 'driver_progress' not in st.session_state:
        st.session_state.driver_progress = 0.0
    
    # Increment progress
    st.session_state.driver_progress += 0.02
    if st.session_state.driver_progress >= 1.0:
        st.session_state.driver_progress = 0.0
    
    return st.session_state.driver_progress

def show_driver_assignment():
    """Show driver assignment and live tracking"""
    
    # Update driver location
    if 'driver_location' not in st.session_state.current_ride:
        st.session_state.current_ride['driver_location'] = update_driver_location()
    
    # Show map with route and driver
    m = create_map(
        pickup=st.session_state.current_ride['pickup'],
        dropoff=st.session_state.current_ride['dropoff'],
        driver_progress=st.session_state.current_ride['driver_location']
    )
    folium_static(m, width=1200, height=800)
    
    # Driver info card
    driver = st.session_state.current_ride['driver']
    st.markdown(f"""
        <div class="driver-info">
            <img src="{driver['photo']}" class="driver-photo">
            <div>
                <h3>{driver['name']}</h3>
                <div>{driver['car']} - {driver['plate']}</div>
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

def interpolate_position(start, end, progress):
    """Calculate intermediate position between start and end points"""
    return [
        start[0] + (end[0] - start[0]) * progress,
        start[1] + (end[1] - start[1]) * progress
    ]

def create_route_points(start, end, num_points=20):
    """Create a curved route between two points"""
    points = []
    
    # Create intermediate points
    for i in range(num_points):
        progress = i / (num_points - 1)
        
        # Add some curvature using sine function
        curve = math.sin(progress * math.pi) * 0.0005
        
        point = interpolate_position(start, end, progress)
        point[1] += curve  # Add curve to longitude
        
        points.append(point)
    
    return points

def create_car_icon():
    """Create a custom car icon"""
    return folium.DivIcon(
        html="""
            <div style="font-size: 24px;">🚗</div>
        """,
        icon_size=(30, 30),
        icon_anchor=(15, 15)
    )

def show_live_tracking():
    """Show live tracking with auto-refresh"""
    
    # Initialize progress in session state if not exists
    if 'driver_progress' not in st.session_state:
        st.session_state.driver_progress = 0.0
    
    # Get ride details from session state
    ride = st.session_state.current_ride
    
    # Create map with current progress
    m = create_map(
        pickup=ride['pickup'],
        dropoff=ride['dropoff'],
        driver_progress=st.session_state.driver_progress
    )
    
    # Display map
    folium_static(m, width=800, height=500)
    
    # Update progress for next refresh
    st.session_state.driver_progress += 0.02  # Increment by 2%
    if st.session_state.driver_progress >= 1.0:
        st.session_state.driver_progress = 0.0
    
    # Calculate ETA
    remaining_time = int((1 - st.session_state.driver_progress) * ride['eta'])
    
    # Show status
    status = "Arriving in {} minutes".format(remaining_time)
    st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: white; border-radius: 10px; margin: 10px 0;'>
            <h3>{status}</h3>
            <div class="progress-bar">
                <div class="progress" style="width: {st.session_state.driver_progress * 100}%"></div>
            </div>
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
