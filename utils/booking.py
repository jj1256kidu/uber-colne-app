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
