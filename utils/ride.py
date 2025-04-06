import streamlit as st
import time
from datetime import datetime
import random
from utils.maps import create_map
from utils.payment import show_payment_page
from geopy.geocoders import Nominatim

def calculate_fare(distance):
    """Calculate ride fare based on distance"""
    base_fare = 5.0
    per_km_rate = 2.0
    return base_fare + (distance * per_km_rate)

def estimate_time(distance):
    """Estimate ride time based on distance"""
    avg_speed = 30  # km/h
    return round((distance / avg_speed) * 60)  # Convert to minutes

def show_active_ride():
    """Display the active ride tracking interface"""
    
    st.markdown("### 🚗 Your Ride")
    
    # Create two columns for map and ride details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show live tracking map
        if st.session_state.current_ride:
            update_driver_location()  # Simulate driver movement
            m = create_map(
                st.session_state.current_ride['pickup'],
                st.session_state.current_ride['dropoff'],
                show_driver=True,
                driver_location=st.session_state.current_ride['driver_location']
            )
            st.components.v1.html(m._repr_html_(), height=400)
    
    with col2:
        show_ride_status()

def show_ride_status():
    """Display ride status and driver details"""
    
    ride = st.session_state.current_ride
    driver = ride['driver']
    
    # Driver details card
    st.markdown(f"""
        <div class="driver-card">
            <img src="{driver['photo']}" style="width:100px;height:100px;border-radius:50%">
            <h3>{driver['name']}</h3>
            <p>⭐ {driver['rating']} ({driver['trips']} trips)</p>
            <p>🚗 {driver['car']}</p>
            <p>📋 {driver['plate']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Ride status
    status = ride['status']
    st.markdown(f"""
        <div class="status-card">
            <h3>Status: {status}</h3>
            <div class="progress-bar">
                <div class="progress" style="width: {get_progress_percentage(status)}%"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Show appropriate buttons based on status
    if status == "Completed":
        show_feedback_form()
    elif status == "Driver En Route":
        simulate_driver_arrival()
    elif status == "Arrived":
        start_ride_button()
    elif status == "In Progress":
        end_ride_button()

def update_driver_location():
    """Simulate driver movement"""
    if 'driver_location' not in st.session_state.current_ride:
        # Initialize driver location at pickup
        geolocator = Nominatim(user_agent="ridesharepro")
        loc = geolocator.geocode(st.session_state.current_ride['pickup'])
        st.session_state.current_ride['driver_location'] = [
            loc.latitude,
            loc.longitude
        ]
    else:
        # Simulate movement towards destination
        current = st.session_state.current_ride['driver_location']
        geolocator = Nominatim(user_agent="ridesharepro")
        dest = geolocator.geocode(st.session_state.current_ride['dropoff'])
        
        # Move slightly towards destination
        st.session_state.current_ride['driver_location'] = [
            current[0] + (dest.latitude - current[0]) * 0.1,
            current[1] + (dest.longitude - current[1]) * 0.1
        ]

def get_progress_percentage(status):
    """Return progress percentage based on ride status"""
    status_map = {
        'Driver En Route': 25,
        'Arrived': 50,
        'In Progress': 75,
        'Completed': 100
    }
    return status_map.get(status, 0)

def show_feedback_form():
    """Display and handle the feedback form"""
    st.markdown("### ⭐ Rate Your Ride")
    
    rating = st.slider("Rating", 1, 5, 5)
    feedback = st.text_area("Additional Feedback")
    
    if st.button("Submit Feedback"):
        # Save feedback
        st.session_state.ride_history.append({
            'date': datetime.now(),
            'driver': st.session_state.current_ride['driver']['name'],
            'rating': rating,
            'feedback': feedback,
            'fare': st.session_state.current_ride['fare'],
            'pickup': st.session_state.current_ride['pickup'],
            'dropoff': st.session_state.current_ride['dropoff']
        })
        
        # Clear current ride
        st.session_state.current_ride = None
        st.success("Thank you for your feedback!")
        st.rerun()

def show_ride_history():
    """Display ride history in a clean format"""
    st.markdown("### 📜 Ride History")
    
    if not st.session_state.ride_history:
        st.info("No rides yet!")
        return
    
    for ride in reversed(st.session_state.ride_history):
        with st.expander(
            f"🚗 {ride['date'].strftime('%B %d, %Y %I:%M %p')}"
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**From:** ", ride['pickup'])
                st.write("**To:** ", ride['dropoff'])
                st.write("**Driver:** ", ride['driver'])
            
            with col2:
                st.write("**Fare:** ", f"${ride['fare']:.2f}")
                st.write("**Rating:** ", "⭐" * ride['rating'])
                if ride['feedback']:
                    st.write("**Feedback:** ", ride['feedback'])

def simulate_driver_arrival():
    """Simulate driver arriving at pickup location"""
    if st.button("Simulate Driver Arrival"):
        st.session_state.current_ride['status'] = 'Arrived'
        st.rerun()

def start_ride_button():
    """Button to start the ride"""
    if st.button("Start Ride"):
        st.session_state.current_ride['status'] = 'In Progress'
        st.rerun()

def end_ride_button():
    """Button to end the ride"""
    if st.button("End Ride"):
        show_payment_page() 
