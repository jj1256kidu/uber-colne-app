import streamlit as st
from datetime import datetime
import time

# Import utilities
from utils.auth import check_credentials, show_login
from utils.booking import show_booking_page
from utils.ride import show_active_ride, show_ride_history
from utils.payment import show_payment_page
from assets.styles import load_css

# Page config
st.set_page_config(
    page_title="RideShare Pro",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
load_css()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'current_ride' not in st.session_state:
    st.session_state.current_ride = None
if 'ride_history' not in st.session_state:
    st.session_state.ride_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def main():
    # Show sidebar only if logged in
    if st.session_state.logged_in:
        with st.sidebar:
            show_sidebar()
    
    # Main content
    if not st.session_state.logged_in:
        show_login()
    else:
        show_main_content()

def show_sidebar():
    st.title("🚗 RideShare Pro")
    st.write(f"Welcome, {st.session_state.username}!")
    
    # Navigation
    st.markdown("### 📱 Menu")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()
    if st.button("📜 Ride History", use_container_width=True):
        st.session_state.current_page = 'history'
        st.rerun()
    
    # Settings
    st.markdown("### ⚙️ Settings")
    if st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    
    # Logout
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

def show_main_content():
    if st.session_state.current_page == 'home':
        if st.session_state.current_ride:
            show_active_ride()
        else:
            show_booking_page()
    elif st.session_state.current_page == 'history':
        show_ride_history()

if __name__ == "__main__":
    main() 
