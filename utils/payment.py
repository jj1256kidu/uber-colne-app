import streamlit as st
import time

def show_payment_page():
    """Display payment options and handle payment flow"""
    
    st.markdown("### 💳 Payment")
    
    # Show fare details
    fare = st.session_state.current_ride['fare']
    st.markdown(f"""
        <div class="fare-card">
            <h2>Total Fare: ${fare:.2f}</h2>
            <p>Base fare + Distance + Time</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Payment method selection
    payment_method = st.radio(
        "Select Payment Method",
        ["Credit Card", "PayPal", "Cash"],
        horizontal=True
    )
    
    if payment_method == "Credit Card":
        show_card_payment()
    elif payment_method == "PayPal":
        show_paypal_payment()
    else:
        show_cash_payment()

def show_card_payment():
    """Display credit card payment form"""
    
    with st.form("card_payment"):
        st.text_input("Card Number", placeholder="1234 5678 9012 3456")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Expiry Date", placeholder="MM/YY")
        with col2:
            st.text_input("CVV", placeholder="123", type="password")
        
        if st.form_submit_button("Pay Now"):
            process_payment()

def show_paypal_payment():
    """Display PayPal payment option"""
    
    st.markdown("""
        <div style='text-align: center'>
            <img src='https://www.paypalobjects.com/webstatic/en_US/i/buttons/checkout-logo-large.png' 
                 width='200'>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Pay with PayPal"):
        process_payment()

def show_cash_payment():
    """Display cash payment option"""
    
    st.info("Please pay the driver directly in cash.")
    if st.button("Confirm Cash Payment"):
        process_payment()

def process_payment():
    """Simulate payment processing"""
    
    with st.spinner("Processing payment..."):
        time.sleep(2)
        st.success("Payment successful!")
        time.sleep(1)
        
        # Update ride status
        st.session_state.current_ride['status'] = 'Completed'
        st.rerun() 
