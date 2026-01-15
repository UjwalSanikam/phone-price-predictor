import streamlit as st
import joblib
import pandas as pd
import numpy as np
import time

# 1. Load Models AND the new MRP Database
model = joblib.load('price_predictor_model.pkl')
le_brand = joblib.load('le_brand.pkl')
le_condition = joblib.load('le_condition.pkl')
phone_db = joblib.load('phone_mrp_db.pkl') # <--- NEW FILE

st.set_page_config(page_title="TechResell Pro", page_icon="📱", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000;
        font-weight: bold;
        border: none;
        height: 50px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.title("📱 TechResell Pro")
    st.markdown("### Compare Used Price vs. New Price")
with col2:
    st.metric("Database Size", f"{len(phone_db)} Models", "Updated Today")

st.divider()

# --- INPUT SECTION ---
with st.container(border=True):
    st.subheader("🛠️ Device Details")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Selectbox allows typing to search!
        brand = st.selectbox(
            "Search Model (Type to search)", 
            le_brand.classes_, 
            index=None, 
            placeholder="e.g. iPhone 13..."
        )
    with c2:
        storage = st.selectbox("Storage", [64, 128, 256, 512], index=None)
    with c3:
        condition = st.selectbox("Condition", le_condition.classes_, index=None)

    btn = st.button("Calculate Value")

# --- RESULT SECTION ---
if btn:
    if brand and storage and condition:
        # Spinner
        with st.spinner("Analyzing market rates..."):
            time.sleep(1)

        # 1. Predict Used Price
        brand_num = le_brand.transform([brand])[0]
        condition_num = le_condition.transform([condition])[0]
        input_data = pd.DataFrame({'brand': [brand_num], 'storage_gb': [storage], 'condition': [condition_num]})
        
        predicted_price = int(model.predict(input_data)[0])
        
        # 2. Get Original Price (MRP)
        original_mrp = phone_db.get(brand, 0)
        # Adjust MRP for storage (approx logic)
        if storage == 128: original_mrp += 5000
        elif storage == 256: original_mrp += 10000
        elif storage == 512: original_mrp += 18000
        
        # 3. Calculate Stats
        savings = original_mrp - predicted_price
        savings_pct = int((savings / original_mrp) * 100) if original_mrp > 0 else 0

        # 4. Display
        st.subheader(f"Valuation for {brand} ({storage}GB)")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Original Price (New)", f"₹{original_mrp:,}")
        col_b.metric("Estimated Used Value", f"₹{predicted_price:,}", delta_color="normal")
        col_c.metric("Money Saved", f"₹{savings:,}", f"-{savings_pct}% vs New")
        
        st.progress(savings_pct / 100, text=f"This device retains {100-savings_pct}% of its original value")
        
        # Recommendation
        if savings_pct > 50:
            st.success("✅ **Great Deal!** This phone is less than half the price of a new one.")
        else:
            st.info("ℹ️ **High Value:** This phone holds its value very well.")

    else:
        st.warning("Please select all options above.")