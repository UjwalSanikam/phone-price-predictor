import pandas as pd
import numpy as np
import joblib
from datetime import datetime

"""
Analytics utility for TechResell Pro
Provides market insights, trends, and statistical analysis
"""

def load_dataset():
    """Load the training dataset"""
    return pd.read_csv('phones.csv')

def analyze_brand_depreciation():
    """Analyze depreciation patterns by brand"""
    df = load_dataset()
    phone_db = joblib.load('phone_mrp_db.pkl')
    
    print("=" * 60)
    print("📊 BRAND DEPRECIATION ANALYSIS")
    print("=" * 60)
    
    brand_stats = []
    for brand in df['brand'].unique():
        brand_data = df[df['brand'] == brand]
        original_price = phone_db.get(brand, 0)
        
        if original_price > 0:
            retention_pct = (brand_data['price'].mean() / original_price) * 100
            brand_stats.append({
                'Brand': brand,
                'Avg Used Price': f"₹{brand_data['price'].mean():,.0f}",
                'Original MRP': f"₹{original_price:,}",
                'Retention %': f"{retention_pct:.1f}%",
                'Samples': len(brand_data)
            })
    
    stats_df = pd.DataFrame(brand_stats)
    stats_df = stats_df.sort_values('Retention %', ascending=False)
    print(stats_df.to_string(index=False))
    print()

def analyze_condition_impact():
    """Analyze price impact by device condition"""
    df = load_dataset()
    
    print("=" * 60)
    print("🎨 CONDITION IMPACT ON PRICING")
    print("=" * 60)
    
    condition_stats = []
    for condition in df['condition'].unique():
        condition_data = df[df['condition'] == condition]
        condition_stats.append({
            'Condition': condition,
            'Avg Price': f"₹{condition_data['price'].mean():,.0f}",
            'Price Range': f"₹{condition_data['price'].min():,} - ₹{condition_data['price'].max():,}",
            'Count': len(condition_data)
        })
    
    stats_df = pd.DataFrame(condition_stats)
    print(stats_df.to_string(index=False))
    print()

def analyze_storage_impact():
    """Analyze price impact by storage capacity"""
    df = load_dataset()
    
    print("=" * 60)
    print("💾 STORAGE CAPACITY IMPACT")
    print("=" * 60)
    
    storage_stats = []
    for storage in sorted(df['storage_gb'].unique()):
        storage_data = df[df['storage_gb'] == storage]
        storage_stats.append({
            'Storage (GB)': storage,
            'Avg Price': f"₹{storage_data['price'].mean():,.0f}",
            'Premium vs 64GB': f"₹{storage_data['price'].mean() - df[df['storage_gb'] == 64]['price'].mean():+,.0f}",
            'Count': len(storage_data)
        })
    
    stats_df = pd.DataFrame(storage_stats)
    print(stats_df.to_string(index=False))
    print()

def analyze_age_depreciation():
    """Analyze depreciation over device age"""
    df = load_dataset()
    
    print("=" * 60)
    print("⏳ DEPRECIATION BY DEVICE AGE")
    print("=" * 60)
    
    # Create age groups
    age_bins = [0, 6, 12, 24, 36, 48]
    age_labels = ['0-6mo', '6-12mo', '12-24mo', '24-36mo', '36-48mo']
    df['age_group'] = pd.cut(df['age_months'], bins=age_bins, labels=age_labels)
    
    age_stats = []
    for group in age_labels:
        group_data = df[df['age_group'] == group]
        if len(group_data) > 0:
            age_stats.append({
                'Age Group': group,
                'Avg Price': f"₹{group_data['price'].mean():,.0f}",
                'Depreciation': f"{(group_data['age_months'].mean() / 60) * 40:.1f}%",
                'Count': len(group_data)
            })
    
    stats_df = pd.DataFrame(age_stats)
    print(stats_df.to_string(index=False))
    print()

def analyze_battery_impact():
    """Analyze price impact by battery health"""
    df = load_dataset()
    
    print("=" * 60)
    print("🔋 BATTERY HEALTH IMPACT")
    print("=" * 60)
    
    battery_bins = [0, 70, 80, 90, 100]
    battery_labels = ['60-70%', '70-80%', '80-90%', '90-100%']
    df['battery_group'] = pd.cut(df['battery_health'], bins=battery_bins, labels=battery_labels)
    
    battery_stats = []
    for group in battery_labels:
        group_data = df[df['battery_group'] == group]
        if len(group_data) > 0:
            battery_stats.append({
                'Battery Health': group,
                'Avg Price': f"₹{group_data['price'].mean():,.0f}",
                'Impact': f"{((group_data['price'].mean() / df['price'].mean()) - 1) * 100:+.1f}%",
                'Count': len(group_data)
            })
    
    stats_df = pd.DataFrame(battery_stats)
    print(stats_df.to_string(index=False))
    print()

def market_summary():
    """Display overall market summary"""
    df = load_dataset()
    phone_db = joblib.load('phone_mrp_db.pkl')
    
    print("=" * 60)
    print("📈 MARKET SUMMARY")
    print("=" * 60)
    print(f"Total Brands: {len(phone_db)}")
    print(f"Total Samples: {len(df)}")
    print(f"Price Range: ₹{df['price'].min():,} - ₹{df['price'].max():,}")
    print(f"Average Used Price: ₹{df['price'].mean():,.0f}")
    print(f"Median Used Price: ₹{df['price'].median():,.0f}")
    print(f"Standard Deviation: ₹{df['price'].std():,.0f}")
    print(f"Average Device Age: {df['age_months'].mean():.1f} months")
    print(f"Average Battery Health: {df['battery_health'].mean():.1f}%")
    print()

if __name__ == "__main__":
    print("\n🔍 TechResell Pro Analytics Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    market_summary()
    analyze_brand_depreciation()
    analyze_condition_impact()
    analyze_storage_impact()
    analyze_age_depreciation()
    analyze_battery_impact()
    
    print("=" * 60)
    print("✅ Analysis Complete!")
    print("=" * 60)
