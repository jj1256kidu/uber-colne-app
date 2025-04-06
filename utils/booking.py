import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import time
import random
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from data.locations import popular_locations
from data.drivers import available_drivers
from utils.maps import create_map, generate_route
from utils.ride import calculate_fare, estimate_time

def calculate_distance(pickup, dropoff):
    """Calculate distance between two locations"""
    try:
        geolocator = Nominatim(user_agent="ridesharepro")
        loc1 = geolocator.geocode(pickup)
        loc2 = geolocator.geocode(dropoff)
        return geodesic(
            (loc1.latitude, loc1.longitude),
            (loc2.latitude, loc2.longitude)
        ).kilometers
    except:
        return 5.0  # Default fallback distance

def show_booking_page():
    """Display the main booking interface"""
    
    # Create two columns: Map and Booking Form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📍 Select Location")
        
        # Location inputs with autocomplete
        pickup = st.selectbox(
            "Pickup Location",
            options=popular_locations,
            index=0,
            key="pickup_location"
        )
        
        dropoff = st.selectbox(
            "Drop-off Location",
            options=popular_locations,
            index=1,
            key="dropoff_location"
        )
        
        # Show map
        try:
            m = create_map(pickup, dropoff)
            folium_static(m)
        except Exception as e:
            st.error("Could not load map. Please check your internet connection.")
    
    with col2:
        st.markdown("### 🚗 Ride Details")
        
        # Calculate ride details
        distance = calculate_distance(pickup, dropoff)
        fare = calculate_fare(distance)
        eta = estimate_time(distance)
        
        # Show ride options
        show_ride_options(distance, fare, eta)

    # Additional booking form elements
    # ...

    # ... 

def show_ride_options(distance, fare, eta):
    """Display available ride options"""
    
    # Ride types with multipliers
    ride_types = {
        "UberX": 1.0,
        "Comfort": 1.2,
        "Premium": 1.5
    }
    
    st.markdown("""
        <style>
        .ride-option {
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin: 10px 0;
            cursor: pointer;
        }
        .ride-option:hover {
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)
    
    selected_type = None
    
    for ride_type, multiplier in ride_types.items():
        ride_fare = fare * multiplier
        
        # Create clickable ride option
        if st.button(
            f"""
            ### {ride_type}
            🕒 {eta} min • 💰 ${ride_fare:.2f}
            """,
            key=f"ride_{ride_type}",
            use_container_width=True
        ):
            selected_type = ride_type
            st.session_state.selected_ride = {
                'type': ride_type,
                'fare': ride_fare,
                'distance': distance,
                'eta': eta
            }
    
    if selected_type:
        confirm_booking(selected_type)

def confirm_booking(ride_type):
    """Handle ride confirmation and driver assignment"""
    
    st.markdown("### 🎉 Ready to ride!")
    
    # Show confirmation button
    if st.button("🚀 Confirm Booking", use_container_width=True):
        with st.spinner("Finding your driver..."):
            time.sleep(2)
            # Assign random driver
            driver = random.choice(available_drivers)
            
            # Create ride in session state
            st.session_state.current_ride = {
                'driver': driver,
                'pickup': st.session_state.pickup,
                'dropoff': st.session_state.dropoff,
                'type': ride_type,
                'fare': st.session_state.selected_ride['fare'],
                'status': 'Driver En Route',
                'start_time': datetime.now(),
                'driver_location': None
            }
            
            st.success("Driver found! Redirecting...")
            time.sleep(1)
            st.rerun() 
