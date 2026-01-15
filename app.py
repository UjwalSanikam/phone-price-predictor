import streamlit as st
import joblib
import pandas as pd

# 1. Load the "Brain" (Model) and "Translators" (Encoders)
model = joblib.load('price_predictor_model.pkl')
le_brand = joblib.load('le_brand.pkl')
le_condition = joblib.load('le_condition.pkl')

# 2. Set up the page
st.set_page_config(page_title="Phone Price Predictor", page_icon="📱")
st.title("📱 Used Phone Price Predictor")
st.write("Enter your phone details to see how much it is worth in the second-hand market.")

# 3. Create the Input Form
col1, col2 = st.columns(2)

with col1:
    # Use the brands we learned during training
    brand = st.selectbox("Brand Model", le_brand.classes_)
    storage = st.selectbox("Storage (GB)", [64, 128, 256])

with col2:
    # Use the conditions we learned during training
    condition = st.selectbox("Condition", le_condition.classes_)

# 4. The Magic Button
if st.button("Predict Price"):
    # Convert user text inputs to numbers (just like we did in training)
    brand_num = le_brand.transform([brand])[0]
    condition_num = le_condition.transform([condition])[0]
    
    # Create a small table of data for the model
    input_data = pd.DataFrame({
        'brand': [brand_num],
        'storage_gb': [storage],
        'condition': [condition_num]
    })
    
    # Ask the model for the answer
    prediction = model.predict(input_data)[0]
    
    # Show the result
    st.success(f"💰 Estimated Value: ₹{int(prediction)}")
    st.info("This price is based on current market trends for used devices.")