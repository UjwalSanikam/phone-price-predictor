import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO
import os

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="TechResell Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ RESOURCE LOADING ============
@st.cache_resource
def load_resources():
    """Load models, encoders, and datasets"""
    resources = {}
    
    # Try LightGBM model first (scaled version)
    if os.path.exists('price_predictor_lgb.pkl'):
        import lightgbm as lgb
        resources['model'] = lgb.Booster(model_file='price_predictor_lgb.pkl')
        resources['model_type'] = 'lgb'
    else:
        resources['model'] = joblib.load('price_predictor_model.pkl')
        resources['model_type'] = 'sklearn'
    
    # Load encoders
    resources['le_brand'] = joblib.load('le_brand.pkl')
    resources['le_condition'] = joblib.load('le_condition.pkl')
    
    # Try loading additional encoders for scaled model
    if os.path.exists('le_os.pkl'):
        resources['le_os'] = joblib.load('le_os.pkl')
        resources['le_color'] = joblib.load('le_color.pkl')
        resources['le_network'] = joblib.load('le_network.pkl')
    
    # Load phone database
    resources['phone_db'] = joblib.load('phone_mrp_db.pkl')
    
    # Load dataset (prefer scaled version)
    if os.path.exists('phones_scaled.csv'):
        resources['dataset'] = pd.read_csv('phones_scaled.csv', nrows=10000)  # Load sample
    else:
        resources['dataset'] = pd.read_csv('phones.csv')
    
    return resources

resources = load_resources()
model = resources['model']
le_brand = resources['le_brand']
le_condition = resources['le_condition']
phone_db = resources['phone_db']
dataset = resources['dataset']

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000;
        font-weight: bold;
        border: none;
        height: 50px;
        font-size: 16px;
        border-radius: 10px;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button:hover { transform: scale(1.02); }
    .metric-box {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #92FE9D;
    }
    .header-text {
        color: #00C9FF;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============ SIDEBAR CONFIG ============
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("---")

# ============ MAIN CONTENT ============
st.markdown("<h1 style='text-align: center; color: #00C9FF;'>📱 TechResell Pro v3.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>AI-Powered Phone Resale Pricing & Analytics</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Valuation", "📊 Analytics", "🔄 Comparison", "📈 Trends", "📦 Bulk Import"])

# ============ TAB 1: VALUATION ============
with tab1:
    st.header("💰 Individual Phone Valuation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("📌 Brand", sorted(le_brand.classes_))
        storage = st.selectbox("💾 Storage (GB)", [64, 128, 256, 512])
    
    with col2:
        condition = st.selectbox("⭐ Condition", sorted(le_condition.classes_))
        age = st.slider("📅 Age (months)", 0, 60, 12)
    
    col3, col4 = st.columns(2)
    with col3:
        battery = st.slider("🔋 Battery Health (%)", 20, 100, 85)
        screen_size = st.slider("📺 Screen Size (inches)", 5.0, 6.9, 6.1)
    
    with col4:
        camera_count = st.select_slider("📷 Camera Count", [1, 2, 3, 4, 5], value=3)
        seller_rating = st.slider("⭐ Seller Rating", 1.0, 5.0, 4.5)
    
    trade_in = st.number_input("💵 Trade-in Value (₹)", 0, 100000, 10000, step=1000)
    
    if st.button("🔍 Predict Price", use_container_width=True, key="predict_single"):
        try:
            # Prepare features - must match training order: 16 features
            # brand_encoded, storage_gb, condition_encoded, age_months, 
            # battery_health, os_encoded, camera_count, screen_size, 
            # color_encoded, network_encoded, seller_rating, trade_in_value,
            # model_age_factor, storage_category, screen_size_category, overall_condition_score
            
            brand_enc = le_brand.transform([brand])[0]
            condition_enc = le_condition.transform([condition])[0]
            os_enc = resources.get('le_os', le_brand).transform(['Android 12'])[0] if 'le_os' in resources else 10
            color_enc = resources.get('le_color', le_brand).transform(['Black'])[0] if 'le_color' in resources else 0
            network_enc = resources.get('le_network', le_brand).transform(['5G'])[0] if 'le_network' in resources else 1
            
            storage_cat = min((storage - 64) // 64, 3)
            screen_cat = min(int((screen_size - 5.0) / 0.7), 2)
            model_age = age / 12
            overall_score = battery * 0.4 + condition_enc * 25 + seller_rating * 20
            
            features = np.array([[
                brand_enc, storage, condition_enc, age, 
                battery, os_enc, camera_count, screen_size, 
                color_enc, network_enc, seller_rating, trade_in,
                model_age, storage_cat, screen_cat, overall_score
            ]])
            
            prediction = model.predict(features)[0]
            st.success(f"## 💰 Estimated Price: ₹{int(prediction):,}")
            
            # Additional insights
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Base Trade-in", f"₹{trade_in:,}")
            with col2:
                st.metric("Premium Factor", f"{(prediction / trade_in if trade_in > 0 else 1):.2f}x")
            with col3:
                st.metric("Depreciation", f"{((1 - (age / 60)) * 100):.0f}%")
        except Exception as e:
            st.error(f"❌ Error in prediction: {str(e)}\n\nPlease ensure the model is trained. Run: `python train_model_scaled.py`")

# ============ TAB 2: ANALYTICS ============
with tab2:
    st.header("📊 Dataset Analytics")
    
    if len(dataset) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Phones", f"{len(dataset):,}")
        with col2:
            st.metric("Avg Price", f"₹{dataset['price'].mean():,.0f}")
        with col3:
            st.metric("Price Range", f"₹{dataset['price'].min():,} - {dataset['price'].max():,}")
        with col4:
            st.metric("Unique Brands", len(dataset['brand'].unique()))
        
        # Price distribution by condition
        if 'condition' in dataset.columns:
            fig_cond = px.box(dataset, y='price', x='condition', title="Price by Condition",
                            points="outliers", color='condition')
            st.plotly_chart(fig_cond, use_container_width=True)
        
        # Price by brand
        if 'brand' in dataset.columns:
            brand_stats = dataset.groupby('brand')['price'].agg(['count', 'mean']).sort_values('mean', ascending=False).head(10)
            fig_brand = px.bar(brand_stats, y=brand_stats.index, x='mean', orientation='h', 
                             title="Top 10 Brands by Avg Price", labels={'mean': 'Avg Price (₹)', 'index': 'Brand'})
            st.plotly_chart(fig_brand, use_container_width=True)

# ============ TAB 3: COMPARISON ============
with tab3:
    st.header("🔄 Phone Comparison")
    
    num_phones = st.slider("📱 Compare how many phones?", 2, 5, 3)
    
    comparison_data = []
    for i in range(num_phones):
        st.subheader(f"Phone {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            brand = st.selectbox(f"Brand {i+1}", sorted(le_brand.classes_), key=f"comp_brand_{i}")
            storage = st.selectbox(f"Storage {i+1} (GB)", [64, 128, 256, 512], key=f"comp_storage_{i}")
        with col2:
            condition = st.selectbox(f"Condition {i+1}", sorted(le_condition.classes_), key=f"comp_cond_{i}")
            age = st.slider(f"Age {i+1} (months)", 0, 60, 12, key=f"comp_age_{i}")
        
        comparison_data.append({
            'Phone': f"Phone {i+1}",
            'Brand': brand,
            'Storage': f"{storage}GB",
            'Condition': condition,
            'Age': f"{age}m"
        })
    
    if st.button("📊 Compare Phones", use_container_width=True, key="compare_btn"):
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

# ============ TAB 4: TRENDS ============
with tab4:
    st.header("📈 Market Trends")
    
    if 'age_months' in dataset.columns and 'price' in dataset.columns:
        age_price = dataset.groupby('age_months')['price'].mean().sort_index()
        fig_trend = px.line(x=age_price.index, y=age_price.values, 
                           title="Price Depreciation Over Time",
                           labels={'x': 'Age (months)', 'y': 'Avg Price (₹)'})
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.info("💡 Market trends updated based on latest dataset")

# ============ TAB 5: BULK IMPORT ============
with tab5:
    st.header("📦 Bulk Phone Valuation")
    st.markdown("Upload a CSV with phone details for batch pricing predictions")
    
    # Template info
    st.info("""
    📋 **Required CSV Columns:**
    - `brand`: Phone brand
    - `model`: Phone model
    - `storage_gb`: Storage capacity
    - `condition`: Fair/Good/Excellent/Like New
    - `age_months`: Phone age in months
    - `battery_health`: Battery health % (20-100)
    - `camera_count`: Number of cameras
    - `screen_size`: Screen size in inches
    - `seller_rating`: Seller rating (1-5)
    - `trade_in_value`: Trade-in value (₹)
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="bulk_upload")
    
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.write(f"📊 Loaded {len(df_upload)} records")
        st.dataframe(df_upload.head())
        
        if st.button("💰 Valuate All Phones", use_container_width=True, key="bulk_predict"):
            try:
                progress_bar = st.progress(0)
                
                # Prepare predictions
                predictions = []
                for idx, row in df_upload.iterrows():
                    try:
                        condition_enc = le_condition.transform([row['condition']])[0]
                        os_enc = resources.get('le_os', le_brand).transform(['Android 12'])[0] if 'le_os' in resources else 10
                        color_enc = resources.get('le_color', le_brand).transform(['Black'])[0] if 'le_color' in resources else 0
                        network_enc = resources.get('le_network', le_brand).transform(['5G'])[0] if 'le_network' in resources else 1
                        
                        storage_cat = min((row['storage_gb'] - 64) // 64, 3)
                        screen_cat = min(int((row['screen_size'] - 5.0) / 0.7), 2)
                        model_age = row['age_months'] / 12
                        overall_score = row['battery_health'] * 0.4 + condition_enc * 25 + row['seller_rating'] * 20
                        
                        features = np.array([[
                            le_brand.transform([row['brand']])[0],
                            row['storage_gb'],
                            condition_enc,
                            row['age_months'],
                            row['battery_health'],
                            os_enc,
                            row['camera_count'],
                            row['screen_size'],
                            color_enc,
                            network_enc,
                            row['seller_rating'],
                            row['trade_in_value'],
                            model_age,
                            storage_cat,
                            screen_cat,
                            overall_score
                        ]])
                        pred = model.predict(features)[0]
                        predictions.append(int(pred))
                    except Exception as row_err:
                        predictions.append(0)
                    
                    progress_bar.progress((idx + 1) / len(df_upload))
                
                df_upload['predicted_price'] = predictions
                
                # Display results
                st.success(f"✅ Valued {len(df_upload)} phones!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Min Price", f"₹{df_upload['predicted_price'].min():,.0f}")
                with col2:
                    st.metric("Avg Price", f"₹{df_upload['predicted_price'].mean():,.0f}")
                with col3:
                    st.metric("Max Price", f"₹{df_upload['predicted_price'].max():,.0f}")
                
                st.dataframe(df_upload, use_container_width=True)
                
                # Export results
                csv_export = df_upload.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv_export,
                    file_name=f"valuated_phones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Error during valuation: {str(e)}")

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #999; font-size: 12px;'>
TechResell Pro v3.0 | Built with Streamlit | Powered by LightGBM | 📱 Phone Valuation Engine
</p>
""", unsafe_allow_html=True)
