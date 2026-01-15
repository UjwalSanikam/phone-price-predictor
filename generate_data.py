import pandas as pd
import random
import joblib
from datetime import datetime, timedelta

# 1. Define the Master List of Phones with their "New" Price (MRP)
PHONE_DB = {
    # Apple
    'iPhone 11': 40000, 'iPhone 12': 50000, 'iPhone 13': 60000, 
    'iPhone 14': 70000, 'iPhone 15': 80000, 'iPhone 15 Pro': 130000,
    'iPhone 15 Plus': 95000,
    # Samsung
    'Samsung S20': 30000, 'Samsung S21': 40000, 'Samsung S22': 55000, 
    'Samsung S23': 75000, 'Samsung S24': 80000, 'Samsung S24 Ultra': 130000,
    'Samsung A54': 35000, 'Samsung A74': 42000,
    # OnePlus
    'OnePlus 9': 35000, 'OnePlus 10 Pro': 45000, 'OnePlus 11': 55000, 'OnePlus 12': 65000,
    # Google
    'Pixel 6': 30000, 'Pixel 7': 45000, 'Pixel 8': 70000, 'Pixel 8 Pro': 100000,
    # Xiaomi
    'Redmi Note 12': 15000, 'Redmi Note 13 Pro': 25000, 'Xiaomi 13': 50000,
    # Other
    'Realme GT': 28000, 'Vivo X80': 55000, 'Motorola Edge 40': 30000
}

data = {
    'brand': [],
    'storage_gb': [],
    'condition': [],
    'age_months': [],
    'battery_health': [],
    'price': []
}

conditions = ['Fair', 'Good', 'Excellent', 'Like New']

print("Generating data for 2000 phones with enhanced features...")

for _ in range(2000):
    brand_name = random.choice(list(PHONE_DB.keys()))
    new_price = PHONE_DB[brand_name]
    
    s = random.choice([64, 128, 256, 512])
    c = random.choice(conditions)
    age = random.randint(3, 48)  # 3 to 48 months old
    battery_health = random.randint(60, 100)
    
    # LOGIC: How much value does it lose?
    # Base used price is roughly 50-70% of new price
    depreciation = random.uniform(0.35, 0.65) 
    
    # Age factor (degrades more over time)
    age_factor = max(0.3, 1 - (age / 120))
    depreciation *= age_factor
    
    # Adjust based on condition
    if c == 'Fair': depreciation -= 0.15
    if c == 'Good': depreciation -= 0.05
    if c == 'Excellent': depreciation += 0.05
    if c == 'Like New': depreciation += 0.10
    
    # Battery health factor
    battery_factor = battery_health / 100
    depreciation *= (0.8 + 0.2 * battery_factor)
    
    # Storage bonus
    if s == 128: new_price += 5000
    if s == 256: new_price += 10000
    if s == 512: new_price += 18000
    
    final_used_price = new_price * max(0.2, depreciation)
    
    data['brand'].append(brand_name)
    data['storage_gb'].append(s)
    data['condition'].append(c)
    data['age_months'].append(age)
    data['battery_health'].append(battery_health)
    data['price'].append(int(final_used_price))

    
# Save the dataset
df = pd.DataFrame(data)
df.to_csv('phones.csv', index=False)

# CRITICAL: Save the Master DB so the App knows the "New" prices later!
joblib.dump(PHONE_DB, 'phone_mrp_db.pkl')

print("✅ Data generated & MRP Database saved as 'phone_mrp_db.pkl'")
print(f"   Total records: {len(df)}")
print(f"   Brands: {len(PHONE_DB)}")
print(f"   Price range: ₹{df['price'].min():,} - ₹{df['price'].max():,}")