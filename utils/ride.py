import streamlit as st
import time
from datetime import datetime
import random
from utils.maps import create_map
from utils.payment import show_payment_page

def calculate_fare(distance):
    """Calculate ride fare based on distance"""
    base_fare = 5.0
    per_km_rate = 2.0
    return base_fare + (distance * per_km_rate)

def get_estimated_time(distance):
    """Calculate estimated ride time based on distance"""
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
