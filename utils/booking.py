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
            index=0
        )

        # Location inputs with autocomplete
        dropoff = st.selectbox(
            "Dropoff Location",
            options
        )

        # Date and time inputs
        date = st.date_input("Date")
        time = st.time_input("Time")

        # Button to confirm booking
        if st.button("Confirm Booking"):
            # Process booking
            pass

    with col2:
        # Map display
        map = create_map(pickup, dropoff)
        folium_static(map)

    # Additional booking form elements
    # ...

    # ... 
