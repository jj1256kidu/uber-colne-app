import streamlit as st
from datetime import datetime
import time
import random
import json

# Handle optional imports
try:
    import folium
    from streamlit_folium import folium_static
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    MAPS_ENABLED = True
except ImportError:
    MAPS_ENABLED = False

# Import custom modules
from utils.auth import check_authentication, login_page
from utils.ride import calculate_fare, get_estimated_time
from data.drivers import available_drivers

# Page configuration
st.set_page_config(
    page_title="RideShare Pro",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check if maps functionality is available
if not MAPS_ENABLED:
    st.warning("Some features are disabled due to missing dependencies. Please install required packages using: pip install -r requirements.txt")

# Load custom CSS
with open('styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_ride' not in st.session_state:
    st.session_state.current_ride = None
if 'ride_history' not in st.session_state:
    st.session_state.ride_history = []

def main():
    # Sidebar for navigation and user info
    with st.sidebar:
        st.title("🚗 RideShare Pro")
        if st.session_state.logged_in:
            st.write(f"Welcome, {st.session_state.username}!")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.experimental_rerun()
        
        # Dark mode toggle
        st.write("---")
        if st.checkbox("Dark Mode"):
            st.markdown("""
                <style>
                    .stApp {
                        background-color: #1a1a1a;
                        color: #ffffff;
                    }
                </style>
                """, unsafe_allow_html=True)

    # Main content
    if not st.session_state.logged_in:
        login_page()
    else:
        show_booking_interface()

def show_booking_interface():
    if st.session_state.current_ride:
        show_active_ride()
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("🎯 Book Your Ride")
            
            # Location inputs
            pickup = st.text_input("Pickup Location", "Times Square, New York")
            dropoff = st.text_input("Drop-off Location", "Central Park, New York")
            
            # Initialize map
            if MAPS_ENABLED:
                m = create_map(pickup, dropoff)
                folium_static(m)
        
        with col2:
            st.header("📋 Ride Details")
            
            # Calculate estimates
            distance = calculate_distance(pickup, dropoff)
            fare = calculate_fare(distance)
            time_estimate = get_estimated_time(distance)
            
            # Display estimates in cards
            st.markdown(f"""
                <div class="metric-card">
                    <h3>Distance</h3>
                    <p>{distance:.1f} km</p>
                </div>
                <div class="metric-card">
                    <h3>Estimated Fare</h3>
                    <p>${fare:.2f}</p>
                </div>
                <div class="metric-card">
                    <h3>Estimated Time</h3>
                    <p>{time_estimate} mins</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Book ride button
            if st.button("🚀 Book Ride", key="book_ride"):
                with st.spinner("Finding your driver..."):
                    time.sleep(2)  # Simulate processing
                    assign_driver()
                st.success("Ride booked successfully!")
                st.experimental_rerun()

def show_active_ride():
    st.header("🚗 Your Active Ride")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show live map with driver location
        if MAPS_ENABLED:
            m = create_map(
                st.session_state.current_ride['pickup'],
                st.session_state.current_ride['dropoff'],
                show_driver=True,
                driver_location=st.session_state.current_ride['driver_location']
            )
            folium_static(m)
    
    with col2:
        # Show driver details
        driver = st.session_state.current_ride['driver']
        st.markdown(f"""
            <div class="driver-card">
                <img src="{driver['photo']}" alt="Driver Photo">
                <h3>{driver['name']}</h3>
                <p>⭐ {driver['rating']} ({driver['trips']} trips)</p>
                <p>🚗 {driver['car']} - {driver['plate']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Ride status
        status = st.session_state.current_ride['status']
        st.markdown(f"""
            <div class="status-card">
                <h3>Status: {status}</h3>
                <div class="progress-bar">
                    <div class="progress" style="width: {get_progress_percentage(status)}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if status == "Completed":
            show_feedback_form()

def calculate_distance(pickup, dropoff):
    """Calculate distance between two locations using Nominatim and geopy"""
    geolocator = Nominatim(user_agent="ridesharepro")
    try:
        loc1 = geolocator.geocode(pickup)
        loc2 = geolocator.geocode(dropoff)
        return geodesic((loc1.latitude, loc1.longitude), 
                       (loc2.latitude, loc2.longitude)).kilometers
    except:
        return 5.0  # Default fallback distance

def assign_driver():
    """Assign a random driver and initialize ride"""
    driver = random.choice(available_drivers)
    st.session_state.current_ride = {
        'driver': driver,
        'pickup': st.session_state.pickup,
        'dropoff': st.session_state.dropoff,
        'status': 'Driver En Route',
        'start_time': datetime.now(),
        'driver_location': None
    }

def get_progress_percentage(status):
    """Return progress percentage based on ride status"""
    status_map = {
        'Driver En Route': 25,
        'Arrived': 50,
        'Ride Started': 75,
        'Completed': 100
    }
    return status_map.get(status, 0)

def show_feedback_form():
    """Display and handle the feedback form"""
    st.subheader("🌟 Rate Your Ride")
    rating = st.slider("Rating", 1, 5, 5)
    feedback = st.text_area("Additional Feedback")
    
    if st.button("Submit Feedback"):
        st.session_state.ride_history.append({
            'driver': st.session_state.current_ride['driver']['name'],
            'rating': rating,
            'feedback': feedback,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.session_state.current_ride = None
        st.success("Thank you for your feedback!")
        st.experimental_rerun()

if __name__ == "__main__":
    main() 
