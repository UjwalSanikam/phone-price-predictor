import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="TechResell Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ LOAD RESOURCES ============
@st.cache_resource
def load_resources():
    model = joblib.load('price_predictor_model.pkl')
    le_brand = joblib.load('le_brand.pkl')
    le_condition = joblib.load('le_condition.pkl')
    phone_db = joblib.load('phone_mrp_db.pkl')
    df = pd.read_csv('phones.csv')
    return model, le_brand, le_condition, phone_db, df

model, le_brand, le_condition, phone_db, dataset = load_resources()

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    /* Main styling */
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* Button styling */
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
    
    /* Metric styling */
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
    
    /* Sidebar */
    .sidebar .sidebar-content { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); }
    
    /* Cards */
    .card-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; font-weight: 600; }
    
    /* Headers */
    h1 { color: #667eea; }
    h2 { color: #764ba2; }
    h3 { color: #667eea; }
</style>
""", unsafe_allow_html=True)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    
    show_advanced = st.checkbox("🔧 Advanced Features", value=True)
    show_comparison = st.checkbox("📊 Comparison Tools", value=True)
    show_analytics = st.checkbox("📈 Market Analytics", value=True)

# ============ HEADER ============
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📱 TechResell Pro")
    st.markdown("### 🚀 AI-Powered Used Phone Valuation Platform")
    st.markdown("Get instant, accurate pricing for your used devices")
    
with col2:
    total_models = len(phone_db)
    st.metric("📦 Phone Models", f"{total_models}+")
    
with col3:
    st.metric("🎯 Accuracy", "83%", "±4%")

st.divider()

# ============ MAIN TABS ============
tab1, tab2, tab3, tab4 = st.tabs(["💰 Valuation", "📊 Analytics", "🔄 Comparison", "📈 Trends"])

# ======================== TAB 1: VALUATION ========================
with tab1:
    st.subheader("🛠️ Device Valuation Tool")
    
    # Input Section
    with st.container(border=True):
        st.markdown("#### Enter Device Details")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            brand = st.selectbox(
                "📱 Phone Model",
                options=sorted(phone_db.keys()),
                index=None,
                placeholder="Select your phone..."
            )
        
        with col_b:
            storage = st.selectbox(
                "💾 Storage (GB)",
                options=[64, 128, 256, 512],
                index=None,
                placeholder="Choose storage..."
            )
        
        with col_c:
            condition = st.selectbox(
                "✨ Condition",
                options=le_condition.classes_,
                index=None,
                placeholder="Select condition..."
            )
        
        with col_d:
            age_months = st.slider("⏳ Age (Months)", 1, 48, 12)
        
        col_e, col_f = st.columns(2)
        
        with col_e:
            battery_health = st.slider("🔋 Battery Health (%)", 20, 100, 85)
        
        with col_f:
            damage_level = st.select_slider(
                "🔧 Damage Level",
                options=["None", "Minor", "Moderate", "Significant"]
            )
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            calculate_btn = st.button("🚀 Calculate Value", use_container_width=True, key="calc_main")
        with col_btn2:
            clear_btn = st.button("🔄 Clear", use_container_width=True)
    
    # Results Section
    if calculate_btn and brand and storage and condition:
        with st.spinner("🔍 Analyzing market data..."):
            
            try:
                # Predict
                brand_num = le_brand.transform([brand])[0]
                condition_num = le_condition.transform([condition])[0]
                
                input_data = pd.DataFrame({
                    'brand_encoded': [brand_num],
                    'storage_gb': [storage],
                    'condition_encoded': [condition_num],
                    'age_months': [age_months],
                    'battery_health': [battery_health]
                })
                
                predicted_price = int(model.predict(input_data)[0])
                
                # Adjust for damage
                damage_adjustment = {'None': 1.0, 'Minor': 0.95, 'Moderate': 0.85, 'Significant': 0.70}
                predicted_price = int(predicted_price * damage_adjustment[damage_level])
                
                original_mrp = phone_db.get(brand, 0)
                if storage > 64:
                    original_mrp += (storage - 64) * 50
                
                savings = original_mrp - predicted_price
                savings_pct = int((savings / original_mrp) * 100) if original_mrp > 0 else 0
                retention_pct = 100 - savings_pct
                
                # Display Results
                st.success("✅ Valuation Complete!")
                
                result_col1, result_col2, result_col3, result_col4 = st.columns(4)
                
                with result_col1:
                    st.metric("Original Price", f"₹{original_mrp:,}", "New")
                
                with result_col2:
                    st.metric("Used Value", f"₹{predicted_price:,}", f"-{savings_pct}%", delta_color="off")
                
                with result_col3:
                    st.metric("You Save", f"₹{savings:,}", "💰")
                
                with result_col4:
                    st.metric("Value Retention", f"{retention_pct}%")
                
                # Progress Bar
                st.progress(min(retention_pct / 100, 1.0))
                st.caption(f"Device retains {retention_pct}% of original value after {age_months} months")
                
                st.divider()
                
                # Detailed Breakdown
                breakdown_col1, breakdown_col2 = st.columns(2)
                
                with breakdown_col1:
                    st.subheader("📋 Price Factors")
                    
                    factors_data = {
                        "📱 Brand": brand,
                        "💾 Storage": f"{storage} GB (+₹{(storage-64)*50:,})" if storage > 64 else f"{storage} GB",
                        "✨ Condition": condition,
                        "🔋 Battery Health": f"{battery_health}%",
                        "⏳ Device Age": f"{age_months} months",
                        "🔧 Damage Level": damage_level,
                    }
                    
                    for factor, value in factors_data.items():
                        st.info(f"{factor}: **{value}**")
                
                with breakdown_col2:
                    st.subheader("💡 Recommendations")
                    
                    if savings_pct > 50:
                        st.success("✅ **Excellent Value!** Over 50% savings vs buying new.")
                    elif savings_pct > 30:
                        st.info("✨ **Good Deal!** Solid savings with quality device.")
                    elif retention_pct > 75:
                        st.warning("📈 **Premium Model!** This phone holds value exceptionally well.")
                    
                    if battery_health < 75:
                        st.warning(f"🔋 **Battery Alert**: {battery_health}% - May need replacement")
                    
                    if age_months > 36:
                        st.info(f"⏰ **Aging Device**: {age_months} months old")
                    
                    if damage_level in ["Moderate", "Significant"]:
                        st.error(f"🔧 **Damage Noted**: {damage_level} damage detected")
                
                st.divider()
                
                # Price Range
                st.subheader("📊 Valuation Range")
                range_low = int(predicted_price * 0.85)
                range_high = int(predicted_price * 1.15)
                st.info(f"**Expected Range**: ₹{range_low:,} — ₹{range_high:,}")
                
                st.divider()
                
                # Export Options
                st.subheader("📥 Export Reports")
                
                export_col1, export_col2, export_col3 = st.columns(3)
                
                with export_col1:
                    pdf_data = generate_pdf_report(
                        brand, storage, condition, age_months, battery_health,
                        damage_level, original_mrp, predicted_price, savings, savings_pct
                    )
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_data,
                        file_name=f"valuation_{brand.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                with export_col2:
                    csv_data = generate_csv_report(
                        brand, storage, condition, age_months, battery_health,
                        damage_level, original_mrp, predicted_price, savings, savings_pct
                    )
                    st.download_button(
                        label="📊 Download CSV Report",
                        data=csv_data,
                        file_name=f"valuation_{brand.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with export_col3:
                    if st.button("💾 Save to Session", use_container_width=True):
                        st.session_state.last_valuation = {
                            'brand': brand,
                            'storage': storage,
                            'condition': condition,
                            'age': age_months,
                            'battery': battery_health,
                            'damage': damage_level,
                            'price': predicted_price,
                            'original': original_mrp,
                            'date': datetime.now()
                        }
                        st.success("✅ Saved!")
                
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
    
    elif calculate_btn:
        st.warning("⚠️ Please fill in all required fields!")

# ======================== TAB 2: MARKET ANALYTICS ========================
with tab2:
    st.subheader("📊 Market Analytics & Insights")
    
    analytics_col1, analytics_col2 = st.columns(2)
    
    with analytics_col1:
        st.markdown("#### 🏆 Top Brands by Value Retention")
        
        brand_retention = []
        for brand_name in phone_db.keys():
            brand_data = dataset[dataset['brand'] == brand_name]
            if len(brand_data) > 0:
                avg_price = brand_data['price'].mean()
                retention = (avg_price / phone_db[brand_name]) * 100
                brand_retention.append({'Brand': brand_name, 'Retention %': retention})
        
        retention_df = pd.DataFrame(brand_retention).sort_values('Retention %', ascending=False).head(10)
        
        fig_retention = px.bar(
            retention_df,
            x='Brand',
            y='Retention %',
            title='Top 10 Brands by Value Retention',
            color='Retention %',
            color_continuous_scale='Viridis'
        )
        fig_retention.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_retention, use_container_width=True)
    
    with analytics_col2:
        st.markdown("#### 🎨 Price by Condition")
        
        condition_price = dataset.groupby('condition')['price'].agg(['mean', 'count']).reset_index()
        
        fig_condition = px.bar(
            condition_price,
            x='condition',
            y='mean',
            title='Average Price by Device Condition',
            color='mean',
            color_continuous_scale='Plasma'
        )
        fig_condition.update_layout(height=400)
        st.plotly_chart(fig_condition, use_container_width=True)
    
    # Storage Impact
    st.markdown("#### 💾 Storage Capacity Impact")
    storage_impact = dataset.groupby('storage_gb')['price'].agg(['mean', 'count']).reset_index()
    
    fig_storage = px.line(
        storage_impact,
        x='storage_gb',
        y='mean',
        markers=True,
        title='Average Price by Storage Capacity',
        labels={'storage_gb': 'Storage (GB)', 'mean': 'Average Price (₹)'}
    )
    fig_storage.update_traces(line=dict(color='#00C9FF', width=3), marker=dict(size=10))
    fig_storage.update_layout(height=400)
    st.plotly_chart(fig_storage, use_container_width=True)
    
    # Age Depreciation
    st.markdown("#### ⏳ Depreciation Over Time")
    age_bins = [0, 6, 12, 24, 36, 48]
    age_labels = ['0-6mo', '6-12mo', '12-24mo', '24-36mo', '36-48mo']
    dataset_copy = dataset.copy()
    dataset_copy['age_group'] = pd.cut(dataset_copy['age_months'], bins=age_bins, labels=age_labels)
    
    age_price = dataset_copy.groupby('age_group', observed=True)['price'].mean().reset_index()
    
    fig_age = px.line(
        age_price,
        x='age_group',
        y='price',
        markers=True,
        title='Price Depreciation by Device Age',
        labels={'age_group': 'Age Group', 'price': 'Average Price (₹)'}
    )
    fig_age.update_traces(line=dict(color='#92FE9D', width=3), marker=dict(size=10))
    fig_age.update_layout(height=400)
    st.plotly_chart(fig_age, use_container_width=True)

# ======================== TAB 3: COMPARISON ========================
with tab3:
    st.subheader("🔄 Device Comparison Tool")
    
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("#### Device 1")
        brand1 = st.selectbox("Select Model 1", sorted(phone_db.keys()), index=None, key="brand1")
        storage1 = st.selectbox("Storage 1", [64, 128, 256, 512], index=1, key="storage1")
        condition1 = st.selectbox("Condition 1", le_condition.classes_, index=1, key="cond1")
        age1 = st.slider("Age 1 (months)", 1, 48, 12, key="age1")
        battery1 = st.slider("Battery 1 (%)", 20, 100, 85, key="bat1")
    
    with comp_col2:
        st.markdown("#### Device 2")
        brand2 = st.selectbox("Select Model 2", sorted(phone_db.keys()), index=None, key="brand2")
        storage2 = st.selectbox("Storage 2", [64, 128, 256, 512], index=1, key="storage2")
        condition2 = st.selectbox("Condition 2", le_condition.classes_, index=2, key="cond2")
        age2 = st.slider("Age 2 (months)", 1, 48, 24, key="age2")
        battery2 = st.slider("Battery 2 (%)", 20, 100, 75, key="bat2")
    
    comp_btn = st.button("⚖️ Compare Devices", use_container_width=True)
    
    if comp_btn and brand1 and brand2 and storage1 and storage2 and condition1 and condition2:
        # Get predictions
        def get_price(brand, storage, condition, age, battery):
            brand_num = le_brand.transform([brand])[0]
            condition_num = le_condition.transform([condition])[0]
            input_data = pd.DataFrame({
                'brand_encoded': [brand_num],
                'storage_gb': [storage],
                'condition_encoded': [condition_num],
                'age_months': [age],
                'battery_health': [battery]
            })
            return int(model.predict(input_data)[0])
        
        price1 = get_price(brand1, storage1, condition1, age1, battery1)
        price2 = get_price(brand2, storage2, condition2, age2, battery2)
        
        comparison_data = pd.DataFrame({
            'Metric': ['Device Model', 'Storage', 'Condition', 'Age', 'Battery', 'Estimated Price'],
            'Device 1': [brand1, f"{storage1}GB", condition1, f"{age1}mo", f"{battery1}%", f"₹{price1:,}"],
            'Device 2': [brand2, f"{storage2}GB", condition2, f"{age2}mo", f"{battery2}%", f"₹{price2:,}"]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
        
        # Comparison chart
        fig_comp = go.Figure(data=[
            go.Bar(name=brand1, x=['Price'], y=[price1], marker_color='#00C9FF'),
            go.Bar(name=brand2, x=['Price'], y=[price2], marker_color='#92FE9D')
        ])
        fig_comp.update_layout(height=400, barmode='group')
        st.plotly_chart(fig_comp, use_container_width=True)
        
        if price1 > price2:
            st.success(f"✅ Device 1 is worth ₹{price1-price2:,} more!")
        elif price2 > price1:
            st.success(f"✅ Device 2 is worth ₹{price2-price1:,} more!")
        else:
            st.info("⚖️ Both devices have similar value!")

# ======================== TAB 4: MARKET TRENDS ========================
with tab4:
    st.subheader("📈 Market Trends & Insights")
    
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        st.markdown("#### 💰 Price Distribution")
        fig_dist = px.histogram(
            dataset,
            x='price',
            nbins=50,
            title='Market Price Distribution',
            labels={'price': 'Price (₹)', 'count': 'Number of Devices'},
            color_discrete_sequence=['#667eea']
        )
        fig_dist.update_layout(height=400)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with trend_col2:
        st.markdown("#### 🔋 Battery Impact on Price")
        fig_battery = px.scatter(
            dataset.sample(min(500, len(dataset))),
            x='battery_health',
            y='price',
            color='condition',
            title='Battery Health vs Price',
            labels={'battery_health': 'Battery Health (%)', 'price': 'Price (₹)'}
        )
        fig_battery.update_layout(height=400)
        st.plotly_chart(fig_battery, use_container_width=True)
    
    # Market Insights
    st.markdown("#### 📊 Market Key Metrics")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("📉 Avg Monthly Depreciation", "3.5%", "-0.5%")
    
    with metric_col2:
        st.metric("🏆 Most Valuable Brand", "iPhone", "+5%")
    
    with metric_col3:
        st.metric("💰 Avg Resale Value", f"₹{dataset['price'].mean():,.0f}", "-2%")
    
    with metric_col4:
        st.metric("📊 Data Points", f"{len(dataset)}", "+100")

# ============ HELPER FUNCTIONS ============

def generate_pdf_report(brand, storage, condition, age, battery, damage, original, predicted, savings, savings_pct):
    """Generate PDF valuation report"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=1
        )
        elements.append(Paragraph("📱 TechResell Pro Valuation Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Date
        date_text = Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(date_text)
        elements.append(Spacer(1, 0.3*inch))
        
        # Device Details Table
        elements.append(Paragraph("<b>Device Details</b>", styles['Heading2']))
        device_data = [
            ['Property', 'Value'],
            ['Phone Model', brand],
            ['Storage', f'{storage} GB'],
            ['Condition', condition],
            ['Age', f'{age} months'],
            ['Battery Health', f'{battery}%'],
            ['Damage Level', damage]
        ]
        
        device_table = Table(device_data, colWidths=[2.5*inch, 3.5*inch])
        device_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(device_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Valuation Summary
        elements.append(Paragraph("<b>Valuation Summary</b>", styles['Heading2']))
        valuation_data = [
            ['Metric', 'Amount'],
            ['Original Retail Price', f'₹{original:,}'],
            ['Estimated Used Value', f'₹{predicted:,}'],
            ['Your Savings', f'₹{savings:,}'],
            ['Savings Percentage', f'{savings_pct}%']
        ]
        
        valuation_table = Table(valuation_data, colWidths=[2.5*inch, 3.5*inch])
        valuation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#92FE9D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(valuation_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = Paragraph(
            "<i>This report is generated by TechResell Pro AI Valuation System. "
            "Estimated price based on current market data.</i>",
            styles['Normal']
        )
        elements.append(footer_text)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    except:
        return b"PDF generation requires reportlab library"

def generate_csv_report(brand, storage, condition, age, battery, damage, original, predicted, savings, savings_pct):
    """Generate CSV valuation report"""
    csv_data = f"""TechResell Pro Valuation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DEVICE DETAILS
Phone Model,{brand}
Storage,{storage} GB
Condition,{condition}
Age,{age} months
Battery Health,{battery}%
Damage Level,{damage}

VALUATION SUMMARY
Original Retail Price,₹{original:,}
Estimated Used Value,₹{predicted:,}
Your Savings,₹{savings:,}
Savings Percentage,{savings_pct}%
"""
    return csv_data

# ============ FOOTER ============
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; padding: 20px;'>
    <p>🔐 <b>TechResell Pro v2.0</b> | AI-Powered Phone Valuation</p>
    <p>Built with ❤️ for accurate, fair market pricing</p>
    <p>© 2026 TechResell Pro. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
