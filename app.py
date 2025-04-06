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
    from utils.maps import create_map
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

# Custom CSS
css = """
/* Card styles */
.metric-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.driver-card {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
}

.driver-card img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-bottom: 10px;
}

.status-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
}

/* Progress bar */
.progress-bar {
    width: 100%;
    height: 10px;
    background-color: #e9ecef;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 10px;
}

.progress {
    height: 100%;
    background-color: #007bff;
    transition: width 0.3s ease;
}

/* Dark mode adjustments */
.dark-mode .metric-card,
.dark-mode .driver-card,
.dark-mode .status-card {
    background-color: #2d2d2d;
    color: #ffffff;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.stButton button {
    transition: transform 0.2s ease;
}

.stButton button:hover {
    transform: scale(1.02);
}
"""

# Apply custom CSS
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_ride' not in st.session_state:
    st.session_state.current_ride = None
if 'ride_history' not in st.session_state:
    st.session_state.ride_history = []
if 'pickup' not in st.session_state:
    st.session_state.pickup = "Times Square, New York"
if 'dropoff' not in st.session_state:
    st.session_state.dropoff = "Central Park, New York"

def main():
    # Sidebar for navigation and user info
    with st.sidebar:
        st.title("🚗 RideShare Pro")
        if st.session_state.logged_in:
            st.write(f"Welcome, {st.session_state.username}!")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()
        
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
            
            # Location inputs - store in session state
            st.session_state.pickup = st.text_input("Pickup Location", 
                value=st.session_state.pickup, key="pickup_input")
            st.session_state.dropoff = st.text_input("Drop-off Location", 
                value=st.session_state.dropoff, key="dropoff_input")
            
            # Show map only if dependencies are available
            if MAPS_ENABLED:
                try:
                    m = create_map(st.session_state.pickup, st.session_state.dropoff)
                    folium_static(m)
                except Exception as e:
                    st.error(f"Could not load map. Error: {str(e)}")
                    st.info("You can still book a ride without the map visualization.")
            else:
                st.info("Map view is currently disabled. Install folium and streamlit-folium to enable maps.")
        
        with col2:
            st.header("📋 Ride Details")
            
            # Calculate estimates using session state values
            distance = calculate_distance(st.session_state.pickup, st.session_state.dropoff)
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
                st.rerun()

def show_active_ride():
    st.header("🚗 Your Active Ride")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show live map with driver location
        if MAPS_ENABLED:
            try:
                m = create_map(
                    st.session_state.current_ride['pickup'],
                    st.session_state.current_ride['dropoff'],
                    show_driver=True,
                    driver_location=st.session_state.current_ride.get('driver_location')
                )
                folium_static(m)
            except Exception as e:
                st.error(f"Could not load map. Error: {str(e)}")
    
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
        st.rerun()

if __name__ == "__main__":
    main() 
