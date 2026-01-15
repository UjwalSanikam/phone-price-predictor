"""
Advanced Features for TechResell Pro
Includes bulk valuation, price alerts, and market analytics
"""

import pandas as pd
import numpy as np
import joblib

class PhoneValuationEngine:
    """Advanced phone valuation engine with batch processing"""
    
    def __init__(self):
        self.model = joblib.load('price_predictor_model.pkl')
        self.le_brand = joblib.load('le_brand.pkl')
        self.le_condition = joblib.load('le_condition.pkl')
        self.phone_db = joblib.load('phone_mrp_db.pkl')
        self.dataset = pd.read_csv('phones.csv')
    
    def valuate_phone(self, brand, storage, condition, age_months, battery_health, damage_level='None'):
        """Value a single phone"""
        try:
            damage_adjustment = {'None': 1.0, 'Minor': 0.95, 'Moderate': 0.85, 'Significant': 0.70}
            
            brand_num = self.le_brand.transform([brand])[0]
            condition_num = self.le_condition.transform([condition])[0]
            
            input_data = pd.DataFrame({
                'brand_encoded': [brand_num],
                'storage_gb': [storage],
                'condition_encoded': [condition_num],
                'age_months': [age_months],
                'battery_health': [battery_health]
            })
            
            price = int(self.model.predict(input_data)[0])
            price *= damage_adjustment[damage_level]
            
            return price
        except:
            return None
    
    def batch_valuate(self, phones_list):
        """Valuate multiple phones at once
        
        phones_list: List of dicts with keys:
            brand, storage, condition, age_months, battery_health, damage_level (optional)
        """
        results = []
        for phone in phones_list:
            price = self.valuate_phone(
                phone.get('brand'),
                phone.get('storage'),
                phone.get('condition'),
                phone.get('age_months'),
                phone.get('battery_health'),
                phone.get('damage_level', 'None')
            )
            results.append({**phone, 'estimated_price': price})
        return pd.DataFrame(results)
    
    def get_brand_trend(self, brand):
        """Get price trend for a specific brand"""
        brand_data = self.dataset[self.dataset['brand'] == brand]
        if len(brand_data) == 0:
            return None
        
        return {
            'brand': brand,
            'avg_price': brand_data['price'].mean(),
            'median_price': brand_data['price'].median(),
            'min_price': brand_data['price'].min(),
            'max_price': brand_data['price'].max(),
            'std_dev': brand_data['price'].std(),
            'sample_count': len(brand_data),
            'mrp': self.phone_db.get(brand, 'N/A')
        }
    
    def get_market_report(self):
        """Get comprehensive market report"""
        return {
            'total_brands': len(self.phone_db),
            'total_samples': len(self.dataset),
            'avg_price': self.dataset['price'].mean(),
            'median_price': self.dataset['price'].median(),
            'price_std_dev': self.dataset['price'].std(),
            'avg_age': self.dataset['age_months'].mean(),
            'avg_battery': self.dataset['battery_health'].mean(),
            'conditions': self.dataset['condition'].unique().tolist()
        }
    
    def get_depreciation_schedule(self, brand, storage, condition, battery_health):
        """Get estimated prices for next 48 months"""
        schedule = []
        for age in range(0, 49, 6):
            price = self.valuate_phone(brand, storage, condition, age, battery_health)
            schedule.append({
                'months': age,
                'estimated_price': price,
                'months_label': f"{age}mo"
            })
        return pd.DataFrame(schedule)
    
    def find_similar_phones(self, brand, storage, condition, limit=5):
        """Find similar phones in market"""
        similar = self.dataset[
            (self.dataset['brand'] == brand) &
            (self.dataset['storage_gb'] == storage) &
            (self.dataset['condition'] == condition)
        ]
        return similar.head(limit)
    
    def calculate_price_range(self, estimated_price, confidence=0.85):
        """Calculate price range based on confidence level"""
        margin = estimated_price * (1 - confidence) / 2
        return {
            'low': int(estimated_price - margin),
            'high': int(estimated_price + margin),
            'estimated': estimated_price,
            'confidence': f"{confidence*100:.0f}%"
        }
    
    def get_storage_premium(self, brand):
        """Calculate storage premium for a brand"""
        premium = {}
        for storage in [128, 256, 512]:
            storage_data = self.dataset[
                (self.dataset['brand'] == brand) &
                (self.dataset['storage_gb'] == storage)
            ]
            base_data = self.dataset[
                (self.dataset['brand'] == brand) &
                (self.dataset['storage_gb'] == 64)
            ]
            
            if len(storage_data) > 0 and len(base_data) > 0:
                avg_storage = storage_data['price'].mean()
                avg_base = base_data['price'].mean()
                premium[f"{storage}GB"] = avg_storage - avg_base
        
        return premium


class PriceAlertSystem:
    """Monitor and alert on price changes"""
    
    def __init__(self, engine):
        self.engine = engine
        self.watched_prices = {}
    
    def add_alert(self, brand, storage, condition, target_price):
        """Add price alert"""
        key = f"{brand}_{storage}_{condition}"
        self.watched_prices[key] = {
            'brand': brand,
            'storage': storage,
            'condition': condition,
            'target_price': target_price,
            'created_at': pd.Timestamp.now()
        }
        return f"Alert set for {brand} at ₹{target_price:,}"
    
    def check_alerts(self, age=12, battery=85):
        """Check if any alerts should trigger"""
        triggered = []
        for key, alert in self.watched_prices.items():
            current_price = self.engine.valuate_phone(
                alert['brand'],
                alert['storage'],
                alert['condition'],
                age,
                battery
            )
            
            if current_price and current_price <= alert['target_price']:
                triggered.append({
                    'alert': alert,
                    'current_price': current_price,
                    'target_price': alert['target_price']
                })
        
        return triggered
    
    def remove_alert(self, brand, storage, condition):
        """Remove price alert"""
        key = f"{brand}_{storage}_{condition}"
        if key in self.watched_prices:
            del self.watched_prices[key]
            return f"Alert removed for {brand}"
        return "Alert not found"


if __name__ == "__main__":
    # Example usage
    engine = PhoneValuationEngine()
    
    print("=" * 60)
    print("TechResell Pro Advanced Features Demo")
    print("=" * 60)
    
    # Single valuation
    price = engine.valuate_phone('iPhone 15', 256, 'Excellent', 12, 90)
    print(f"\n✅ iPhone 15 (256GB, Excellent, 12mo): ₹{price:,}")
    
    # Brand trend
    trend = engine.get_brand_trend('iPhone 15')
    print(f"\n📊 iPhone 15 Market Data:")
    for key, value in trend.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:,.0f}")
        else:
            print(f"   {key}: {value}")
    
    # Depreciation schedule
    print(f"\n📈 Depreciation Schedule (iPhone 15, 256GB, Excellent):")
    schedule = engine.get_depreciation_schedule('iPhone 15', 256, 'Excellent', 90)
    for _, row in schedule.iterrows():
        print(f"   {row['months_label']}: ₹{row['estimated_price']:,}")
    
    # Market report
    print(f"\n📊 Market Report:")
    report = engine.get_market_report()
    for key, value in report.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:,.0f}")
        else:
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
