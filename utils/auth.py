import streamlit as st
import time
from PIL import Image
import requests
from io import BytesIO

def show_login():
    """Display the login page with Google-like styling"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 40px'>
                <h1>🚗 RideShare Pro</h1>
                <p>Book your ride in seconds</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Login container
        with st.container():
            st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1)'>
                    <h2 style='text-align: center; margin-bottom: 20px'>Welcome Back</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Login form
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Login buttons
            if st.button("Login", use_container_width=True):
                if check_credentials(email, password):
                    with st.spinner("Logging in..."):
                        time.sleep(1)
                    st.session_state.logged_in = True
                    st.session_state.username = email.split('@')[0].capitalize()
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            
            # Google login button
            st.markdown("---")
            if st.button("구 Continue with Google", use_container_width=True):
                with st.spinner("Connecting to Google..."):
                    time.sleep(1)
                st.session_state.logged_in = True
                st.session_state.username = "John Doe"
                st.rerun()

def check_credentials(email, password):
    """Simulate credential checking"""
    return bool(email and password)

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('logged_in', False) 
