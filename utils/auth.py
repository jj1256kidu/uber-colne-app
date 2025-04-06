import streamlit as st
import time

def login_page():
    """Display and handle login page"""
    st.header("👋 Welcome to RideShare Pro")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if check_credentials(email, password):
                with st.spinner("Logging in..."):
                    time.sleep(1)
                st.session_state.logged_in = True
                st.session_state.username = email.split('@')[0]
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if new_password == confirm_password:
                with st.spinner("Creating account..."):
                    time.sleep(1)
                st.success("Account created! Please login.")
            else:
                st.error("Passwords don't match")

def check_credentials(email, password):
    """Simulate credential checking"""
    # For demo purposes, accept any non-empty email/password
    return bool(email and password)

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('logged_in', False) 
