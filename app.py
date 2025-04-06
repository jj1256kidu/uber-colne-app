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
from utils.ride import calculate_fare, estimate_time
from data.locations import saved_locations, recent_locations
from data.drivers import available_drivers

# Lottie URLs
LOTTIE_URLS = {
    'loading': "https://lottie.host/f0ec98d5-ec26-4fc5-9fdc-5a497e20928d/Il6pdCzR0P.json",
    'driver': "https://lottie.host/fd37c232-6c9f-4594-8480-f45f563b3f7b/d82GU0V7zv.json",
    'success': "https://lottie.host/3e0b3c5c-1cf2-45a4-a1db-3253cb464aa2/kN0VzYZR4M.json"
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

def show_booking_page():
    """Main booking interface with map and bottom drawer"""
    
    # Full-screen map
    with st.container():
        m = create_map()
        folium_static(m, width=None, height=600)
    
    # Bottom sheet
    st.markdown("""
        <div class="bottom-sheet">
            <h3>Good morning, {}</h3>
            
            <div class="search-box">
                <input type="text" placeholder="Where to?" />
            </div>
            
            <div class="recent-locations">
                <h4>Recent Places</h4>
                {}
            </div>
            
            <div class="mode-toggle">
                <button class="active">🚗 Rides</button>
                <button>🍽️ Eats</button>
            </div>
        </div>
    """.format(
        st.session_state.username,
        "".join([f"""
            <div class="location-card">
                <div class="location-name">{loc['name']}</div>
                <div class="location-address">{loc['address']}</div>
            </div>
        """ for loc in recent_locations])
    ), unsafe_allow_html=True)

def show_booking_confirmation():
    """Show booking confirmation with loading animation"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h2>Finding your ride...</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Show loading animation
        if st.session_state.animations['loading']:
            st_lottie(st.session_state.animations['loading'], height=250)
        
        with st.spinner(""):
            time.sleep(3)  # Simulate search
            st.session_state.page = 'driver_assigned'
            st.rerun()

def show_driver_assignment():
    """Show driver assignment and live tracking"""
    
    # Auto refresh every 2 seconds
    st_autorefresh(interval=2000, key="map_refresh")
    
    # Update driver progress
    st.session_state.driver_progress += 0.02
    if st.session_state.driver_progress >= 1.0:
        st.session_state.driver_progress = 0.0
    
    # Get current driver location
    driver_location = update_driver_location(
        st.session_state.current_ride['pickup'],
        st.session_state.current_ride['dropoff'],
        st.session_state.driver_progress
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show map with current driver position
        m = create_map(
            pickup=st.session_state.current_ride['pickup'],
            dropoff=st.session_state.current_ride['dropoff'],
            driver_location=driver_location
        )
        folium_static(m, width=800, height=500)
        
        # Show progress bar
        remaining_time = int((1 - st.session_state.driver_progress) * st.session_state.current_ride['eta'])
        st.markdown(f"""
            <div style='text-align: center; padding: 10px; background: white; border-radius: 10px; margin: 10px 0;'>
                <h3>Arriving in {remaining_time} minutes</h3>
                <div class="progress-bar">
                    <div class="progress" style="width: {st.session_state.driver_progress * 100}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Driver info
        driver = st.session_state.current_ride['driver']
        st.markdown(f"""
            <div class="driver-card">
                <img src="{driver['photo']}" class="driver-photo">
                <div class="driver-info">
                    <h3>{driver['name']}</h3>
                    <div>{driver['car']} - {driver['plate']}</div>
                    <div class="rating">{'⭐' * int(driver['rating'])}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Cancel ride button
        if st.button("Cancel Ride", key="cancel_ride"):
            st.session_state.current_ride = None
            st.session_state.page = 'booking'
            st.rerun()

def show_ride_completed():
    """Show ride completion with success animation"""
    
    # Show success animation with confetti
    if st.session_state.animations['success']:
        st_lottie(st.session_state.animations['success'], height=300)
    
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🎉 Ride Completed!</h1>
            <p>Thank you for riding with us</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Rating and feedback
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="rating-card">
                <h3>Rate your ride</h3>
                <div class="star-rating">⭐⭐⭐⭐⭐</div>
                <textarea placeholder="Additional feedback (optional)"></textarea>
                <button onclick="submitRating()">Submit Rating</button>
            </div>
        """, unsafe_allow_html=True)

# Add some additional CSS for the new components
st.markdown("""
<style>
/* Status bar */
.status-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
}

.status-bar {
    width: 100%;
    height: 8px;
    background: #f0f0f0;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 10px;
}

.status-progress {
    height: 100%;
    background: #276EF1;
    transition: width 0.3s ease;
}

/* Rating card */
.rating-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.star-rating {
    font-size: 40px;
    margin: 20px 0;
    cursor: pointer;
}

.rating-card textarea {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin: 15px 0;
    resize: vertical;
}

.rating-card button {
    background: black;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 30px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.rating-card button:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'username' not in st.session_state:
    st.session_state.username = "John"
if 'mode' not in st.session_state:
    st.session_state.mode = 'rides'
if 'current_ride' not in st.session_state:
    st.session_state.current_ride = None

# Add to session state initialization
if 'animations' not in st.session_state:
    st.session_state.animations = {
        key: load_lottie_url(url) for key, url in LOTTIE_URLS.items()
    }

if 'driver_progress' not in st.session_state:
    st.session_state.driver_progress = 0.0

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
