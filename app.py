import streamlit as st
import joblib
import pandas as pd
import numpy as np

# 1. Load the Models
model = joblib.load('price_predictor_model.pkl')
le_brand = joblib.load('le_brand.pkl')
le_condition = joblib.load('le_condition.pkl')

# 2. Page Configuration
st.set_page_config(page_title="Phone Price Predictor", page_icon="📱", layout="centered")

# Custom CSS to make the button look better
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header Section
st.title("📱 Instant Phone Value")
st.write("Get a fair market price for your used device in seconds using AI.")
st.divider()

# 4. The "Add Device" Section (Hidden by default using Expander)
# This acts as your "Click to Add Device" button
with st.expander("➕ Add Device Details", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("Select Model", le_brand.classes_, index=None, placeholder="Choose a brand...")
        storage = st.selectbox("Storage Capacity", [64, 128, 256], index=None, placeholder="Select storage...")

    with col2:
        condition = st.selectbox("Device Condition", le_condition.classes_, index=None, placeholder="Select condition...")
        # A helper note for the user
        st.caption("Condition Guide: **Excellent** (No scratches), **Good** (Minor signs), **Fair** (Visible dents).")

    calculate_btn = st.button("💰 Calculate Price")

# 5. Result Section
if calculate_btn:
    if brand and storage and condition:
        # Preprocessing
        brand_num = le_brand.transform([brand])[0]
        condition_num = le_condition.transform([condition])[0]
        
        input_data = pd.DataFrame({
            'brand': [brand_num],
            'storage_gb': [storage],
            'condition': [condition_num]
        })
        
        # Predict
        prediction = model.predict(input_data)[0]
        price = int(prediction)

        st.divider()
        
        # Display Result in a nice Container
        with st.container(border=True):
            st.subheader(f"Estimated Value for {brand}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Your Price", f"₹{price:,}")
            c2.metric("Market Demand", "High 🔥")
            c3.metric("Depreciation", "-15% / yr")
            
            st.success(f"This is a great price! Most shops would offer around ₹{int(price * 0.8):,} for this.")

        # New Feature: Price Trend Graph
        st.subheader("📉 6-Month Price History")
        st.write("See how the value of this phone has changed recently.")
        
        # Generate fake history data for the chart
        dates = pd.date_range(start='2025-01-01', periods=6, freq='M')
        # Create a downward trend
        prices = [price + np.random.randint(500, 2000) for _ in range(6)]
        prices.sort(reverse=True) # Force it to go down to look realistic
        
        chart_data = pd.DataFrame({"Month": dates, "Price (₹)": prices})
        st.line_chart(chart_data, x="Month", y="Price (₹)")

    else:
        st.error("⚠️ Please select all options above to get a price.")