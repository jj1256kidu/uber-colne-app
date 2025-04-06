import streamlit as st
from datetime import datetime
import time
import random
from streamlit_folium import folium_static
import folium
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from streamlit_lottie import st_lottie
import requests
from streamlit_autorefresh import st_autorefresh

# Import custom modules
from utils.maps import create_map, update_driver_location, show_live_tracking
from utils.ride import calculate_fare, estimate_time, get_random_driver, calculate_eta
from data.locations import saved_locations, recent_locations
from data.drivers import available_drivers
from utils.animations import load_lottie_url
from data.mock_data import SAVED_LOCATIONS, LOTTIE_URLS

# Lottie URLs
LOTTIE_URLS = {
    'loading': "https://lottie.host/f0ec98d5-ec26-4fc5-9fdc-5a497e20928d/Il6pdCzR0P.json",
    'driver': "https://lottie.host/fd37c232-6c9f-4594-8480-f45f563b3f7b/d82GU0V7zv.json",
    'success': "https://lottie.host/3e0b3c5c-1cf2-45a4-a1db-3253cb464aa2/kN0VzYZR4M.json",
    'ride_complete': "https://lottie.host/3e0b3c5c-1cf2-45a4-a1db-3253cb464aa2/kN0VzYZR4M.json"
}

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Page config - Set wide mode and remove default margins
st.set_page_config(
    page_title="RideShare",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Uber-like styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0 !important;
    }
    
    /* Bottom drawer styling */
    .bottom-drawer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-radius: 20px 20px 0 0;
        padding: 20px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    /* Input field styling */
    .stTextInput input {
        border-radius: 30px !important;
        border: none !important;
        background: #f8f9fa !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 30px !important;
        padding: 15px !important;
        width: 100% !important;
        font-weight: 600 !important;
    }
    
    .stButton button:first-child {
        background-color: black !important;
        color: white !important;
    }
    
    .stButton button:last-child {
        background-color: #f8f9fa !important;
        color: black !important;
    }
    
    /* Card styling */
    .uber-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Location item styling */
    .location-item {
        display: flex;
        align-items: center;
        padding: 15px;
        border-bottom: 1px solid #f0f0f0;
        cursor: pointer;
    }
    
    .location-item:hover {
        background: #f8f9fa;
    }
    
    /* Driver info styling */
    .driver-info {
        display: flex;
        align-items: center;
        padding: 20px;
        background: white;
        border-radius: 15px;
        margin-top: 10px;
    }
    
    .driver-photo {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin-right: 15px;
    }
    
    /* Rating stars */
    .rating {
        color: #ffd700;
        font-size: 20px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f8f9fa;
        border-radius: 30px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 30px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Recent location styling */
    .recent-location {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        cursor: pointer;
    }
    
    .recent-location:hover {
        background-color: #f8f9fa;
    }
    
    /* Remove padding from main container */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Custom CSS for mobile-style UI
st.markdown("""
<style>
    /* Base styles */
    .stApp {
        max-width: 960px;
        margin: 0 auto;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Mobile container */
    .mobile-container {
        max-width: 414px;
        margin: 0 auto;
        padding: 20px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 15px 20px;
        border: 1px solid #eee;
        background: #f8f9fa;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 25px;
        padding: 10px 25px;
        border: none;
        background: black;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Location cards */
    .location-card {
        padding: 15px;
        background: #f8f9fa;
        border-radius: 15px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .location-card:hover {
        background: #eee;
    }
    
    /* Driver card */
    .driver-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Progress bar */
    .progress-bar {
        height: 4px;
        background: #eee;
        border-radius: 2px;
        overflow: hidden;
    }
    .progress {
        height: 100%;
        background: black;
        transition: width 0.3s ease;
    }
    
    /* Rating stars */
    .rating {
        font-size: 24px;
        color: gold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.update({
        'page': 'booking',
        'current_ride': None,
        'driver_progress': 0.0,
        'username': 'Joost',
        'mode': 'rides'
    })

def show_booking_page():
    """Display the main booking interface"""
    # Greeting based on time of day
    hour = datetime.now().hour
    greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"
    
    st.markdown(f"""
        <div class="mobile-container">
            <h2>🚕 {greeting}, {st.session_state.username}</h2>
            <div class="search-box">
                <input type="text" placeholder="Where to?" style="width: 100%;">
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Saved locations
    for location in SAVED_LOCATIONS:
        if st.button(f"{location['icon']} {location['name']}\n{location['address']}", key=f"loc_{location['name']}"):
            st.session_state.destination = location['address']
            st.session_state.page = 'confirm_ride'
            st.rerun()
    
    # Mode toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚗 Rides", key="rides_btn"):
            st.session_state.mode = 'rides'
    with col2:
        if st.button("🍔 Eats", key="eats_btn"):
            st.session_state.mode = 'eats'
    
    # Map with nearby drivers
    m = create_map()
    folium_static(m)

def show_driver_assignment():
    """Show driver assignment and live tracking"""
    if st.session_state.current_ride is None:
        driver = get_random_driver()
        st.session_state.current_ride = {
            'driver': driver,
            'pickup': st.session_state.pickup,
            'dropoff': st.session_state.destination,
            'eta': calculate_eta()
        }
    
    # Auto refresh for driver movement
    st_autorefresh(interval=3000)
    
    # Update driver progress
    st.session_state.driver_progress += 0.02
    if st.session_state.driver_progress >= 1.0:
        st.session_state.page = 'ride_complete'
        st.rerun()
    
    # Show map with driver location
    driver_location = update_driver_location(
        st.session_state.current_ride['pickup'],
        st.session_state.current_ride['dropoff'],
        st.session_state.driver_progress
    )
    m = create_map(
        pickup=st.session_state.current_ride['pickup'],
        dropoff=st.session_state.current_ride['dropoff'],
        driver_location=driver_location
    )
    folium_static(m)
    
    # Driver info card
    driver = st.session_state.current_ride['driver']
    remaining_time = int((1 - st.session_state.driver_progress) * st.session_state.current_ride['eta'])
    
    st.markdown(f"""
        <div class="driver-card">
            <img src="{driver['photo']}" style="width: 60px; height: 60px; border-radius: 50%;">
            <h3>{driver['name']} is on the way</h3>
            <p>{driver['car']} • {driver['plate']}</p>
            <div class="rating">{'⭐' * int(driver['rating'])}</div>
            <div class="progress-bar">
                <div class="progress" style="width: {st.session_state.driver_progress * 100}%"></div>
            </div>
            <p>Arriving in {remaining_time} minutes</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Message Driver")
    with col2:
        if st.button("Cancel Ride"):
            st.session_state.current_ride = None
            st.session_state.page = 'booking'
            st.rerun()

def show_ride_complete():
    """Show ride completion screen with rating"""
    # Show success animation
    success_animation = load_lottie_url(LOTTIE_URLS['ride_complete'])
    st_lottie(success_animation, height=200)
    
    st.markdown("""
        <div class="mobile-container">
            <h2>🎉 Thanks for riding with us!</h2>
            <h3>How was your trip?</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Rating
    rating = st.select_slider("Rate your ride", options=range(1, 6), value=5)
    st.markdown(f"<div class='rating'>{'⭐' * rating}</div>", unsafe_allow_html=True)
    
    # Feedback
    feedback = st.text_area("Any feedback for your driver?")
    
    if st.button("Submit"):
        st.success("Thanks for your feedback!")
        st.session_state.page = 'booking'
        st.session_state.current_ride = None
        st.session_state.driver_progress = 0.0
        st.rerun()

def main():
    """Main app logic"""
    if st.session_state.page == 'booking':
        show_booking_page()
    elif st.session_state.page == 'driver_assigned':
        show_driver_assignment()
    elif st.session_state.page == 'ride_complete':
        show_ride_complete()

if __name__ == "__main__":
    main() 
