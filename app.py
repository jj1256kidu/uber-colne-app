import streamlit as st
from datetime import datetime
import time
import random
from streamlit_folium import folium_static
import folium
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Import custom modules
from utils.maps import create_map, update_driver_location
from utils.ride import calculate_fare, estimate_time
from data.locations import saved_locations, recent_locations
from data.drivers import available_drivers

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
        border-radius: 30px;
        border: none;
        background: #f8f9fa;
        padding: 15px 20px;
        font-size: 16px;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 30px;
        padding: 10px 25px;
        background: black;
        color: white;
        border: none;
        font-weight: 600;
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'booking'
if 'current_ride' not in st.session_state:
    st.session_state.current_ride = None
if 'username' not in st.session_state:
    st.session_state.username = "John"

def show_booking_page():
    """Main booking interface with map and bottom drawer"""
    
    # Full-screen map
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create map centered on default location
        m = create_map()
        folium_static(m, width=1200, height=800)
    
    # Bottom drawer
    with st.container():
        st.markdown("""
            <div class="bottom-drawer">
                <h3>Good morning, {}</h3>
                <div class="uber-card">
                    <div style="position: relative;">
                        <input type="text" placeholder="Where to?" 
                               style="width: 100%; padding: 15px; border-radius: 30px; border: none; background: #f8f9fa;">
                        <span style="position: absolute; right: 15px; top: 50%; transform: translateY(-50%);">📍</span>
                    </div>
                    
                    <div style="margin-top: 20px;">
                        <h4>Recent Locations</h4>
                        {}
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <div style="display: flex; justify-content: center; gap: 20px;">
                        <button style="flex: 1; padding: 15px; border-radius: 30px; background: black; color: white; border: none;">
                            🚗 Rides
                        </button>
                        <button style="flex: 1; padding: 15px; border-radius: 30px; background: #f8f9fa; color: black; border: none;">
                            🍽️ Eats
                        </button>
                    </div>
                </div>
            </div>
        """.format(
            st.session_state.username,
            "".join([f"""
                <div class="location-item">
                    <span style="margin-right: 10px;">📍</span>
                    <div>
                        <div style="font-weight: 600;">{loc['name']}</div>
                        <div style="color: #666; font-size: 14px;">{loc['address']}</div>
                    </div>
                </div>
            """ for loc in recent_locations])
        ), unsafe_allow_html=True)

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
