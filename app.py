import streamlit as st
import joblib
import pandas as pd
import time
from report_generator import create_pdf  # Requires report_generator.py to be in the same folder

# 1. Load the Brains (Model) and the Memory (Database)
# We use st.cache_resource to load these only once, making the app faster
@st.cache_resource
def load_resources():
    model = joblib.load('price_predictor_model.pkl')
    le_brand = joblib.load('le_brand.pkl')
    le_condition = joblib.load('le_condition.pkl')
    phone_db = joblib.load('phone_mrp_db.pkl')
    return model, le_brand, le_condition, phone_db

model, le_brand, le_condition, phone_db = load_resources()

# 2. Page Configuration
st.set_page_config(page_title="TechResell Pro", page_icon="📱", layout="wide")

# Custom CSS for Professional Styling
st.markdown("""
<style>
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000;
        font-weight: bold;
        border: none;
        height: 50px;
        font-size: 16px;
        border-radius: 10px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header Section
col1, col2 = st.columns([2, 1])
with col1:
    st.title("📱 TechResell Pro")
    st.markdown("### AI-Powered Used Phone Valuation")
    st.write("Get an instant, fair market price for your device based on real sales data.")

with col2:
    st.metric(label="Database Size", value=f"{len(phone_db)} Models", delta="Auto-Updated")

st.divider()

# 4. Input Section (The "Smart" Form)
with st.container(border=True):
    st.subheader("🛠️ Device Configuration")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Dynamic Brand Search
        # We sort the keys so the list is alphabetical
        brand = st.selectbox(
            "Search Model", 
            options=sorted(phone_db.keys()), 
            index=None, 
            placeholder="Type to search (e.g. iPhone 15)..."
        )
        
    with c2:
        # Dynamic Storage Logic
        valid_storage = [64, 128, 256, 512] # Default fallback
        
        if brand and brand in phone_db:
            # If brand is selected, ONLY show storage options found in the CSV
            valid_storage = phone_db[brand]['storage']
            
        storage = st.selectbox("Storage (GB)", valid_storage, index=None)
        
    with c3:
        condition = st.selectbox("Condition", le_condition.classes_, index=None)

    # Calculate Button
    btn = st.button("🚀 Calculate Value")

# 5. Result Section
if btn:
    if brand and storage and condition:
        # Animation to make it feel "AI"
        with st.spinner("Analyzing current market trends..."):
            time.sleep(1)

        # A. Predict Price
        brand_num = le_brand.transform([brand])[0]
        condition_num = le_condition.transform([condition])[0]
        
        input_data = pd.DataFrame({
            'brand': [brand_num],
            'storage_gb': [storage],
            'condition': [condition_num]
        })
        
        predicted_price = int(model.predict(input_data)[0])
        
        # B. Get Original Price (MRP) from our learned DB
        original_mrp = 0
        if brand in phone_db:
            original_mrp = phone_db[brand]['mrp']
        
        # Adjust MRP slightly for higher storage (Simple heuristic)
        # (This is just for display comparison, doesn't affect the AI price)
        base_storage = min(phone_db[brand]['storage']) if brand in phone_db else 64
        if storage > base_storage:
            original_mrp += (storage - base_storage) * 50 # Add approx value per extra GB
            
        # C. Calculate Savings
        savings = original_mrp - predicted_price
        savings_pct = int((savings / original_mrp) * 100) if original_mrp > 0 else 0

        # D. Display Results
        st.subheader(f"Valuation Report: {brand}")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Original Retail Price", f"₹{original_mrp:,}")
        col_b.metric("Estimated Used Value", f"₹{predicted_price:,}", delta_color="normal")
        col_c.metric("Money Saved", f"₹{savings:,}", f"-{savings_pct}% vs New")
        
        st.progress(savings_pct / 100, text=f"This device retains {100-savings_pct}% of its original value")
        
        if savings_pct > 50:
            st.success("✅ **Great Deal!** Buying this used saves you over 50% compared to new.")
        
        # E. PDF Download Button
        st.divider()
        col_pdf, _ = st.columns([1, 2])
        with col_pdf:
            st.write("Need an official quote?")
            # Generate PDF in memory
            pdf_bytes = create_pdf(brand, storage, condition, predicted_price, original_mrp)
            
            st.download_button(
                label="⬇️ Download Valuation Certificate (PDF)",
                data=pdf_bytes,
                file_name=f"Valuation_{brand}_{storage}GB.pdf",
                mime="application/pdf"
            )

    else:
        st.warning("⚠️ Please select Brand, Storage, and Condition to get a price.")