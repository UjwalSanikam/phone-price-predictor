import streamlit as st
import joblib
import pandas as pd

# Load the model
model = joblib.load('price_predictor_model.pkl')
le_brand = joblib.load('le_brand.pkl')
le_condition = joblib.load('le_condition.pkl')

st.set_page_config(page_title="Phone Price Predictor", page_icon="📱")

# --- NEW: Sidebar for user input ---
with st.sidebar:
    st.header("⚙️ Device Config")
    st.write("Select the specs of the phone you want to sell.")
    
    # Inputs moved to sidebar
    brand = st.selectbox("Brand Model", le_brand.classes_)
    storage = st.selectbox("Storage (GB)", [64, 128, 256])
    condition = st.selectbox("Condition", le_condition.classes_)
    
    predict_btn = st.button("Get Estimate", type="primary")

# --- NEW: Main Page Design ---
st.title("📱 Used Phone Value Estimator")
st.markdown("### Stop guessing. Start selling.")
st.markdown("Use our AI-powered tool to check the fair market price for your used device instantly.")

# Visual polish: Add columns for stats
col1, col2, col3 = st.columns(3)
col1.metric("Market Trend", "High Demand", "↑ 12%")
col2.metric("Avg. Resale Time", "4 Days", "fast")
col3.metric("Recycling Impact", "Positive", "🌱")

st.divider()

if predict_btn:
    # Logic remains the same
    brand_num = le_brand.transform([brand])[0]
    condition_num = le_condition.transform([condition])[0]
    
    input_data = pd.DataFrame({
        'brand': [brand_num],
        'storage_gb': [storage],
        'condition': [condition_num]
    })
    
    prediction = model.predict(input_data)[0]
    
    st.success(f"💰 Estimated Value: ₹{int(prediction):,}")
    st.balloons() # <-- NEW: Fun animation