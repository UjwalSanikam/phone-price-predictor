import pandas as pd
import random
import joblib

# 1. Define the Master List of Phones with their "New" Price (MRP)
PHONE_DB = {
    # Apple
    'iPhone 11': 40000, 'iPhone 12': 50000, 'iPhone 13': 60000, 
    'iPhone 14': 70000, 'iPhone 15': 80000, 'iPhone 15 Pro': 130000,
    # Samsung
    'Samsung S20': 30000, 'Samsung S21': 40000, 'Samsung S22': 55000, 
    'Samsung S23': 75000, 'Samsung S24 Ultra': 130000,
    # OnePlus
    'OnePlus 9': 35000, 'OnePlus 10 Pro': 45000, 'OnePlus 11': 55000, 'OnePlus 12': 65000,
    # Google
    'Pixel 6': 30000, 'Pixel 7': 45000, 'Pixel 8': 70000,
    # Budget Kings
    'Redmi Note 12': 15000, 'Redmi Note 13 Pro': 25000, 'Realme GT': 28000
}

data = {
    'brand': [],
    'storage_gb': [],
    'condition': [],
    'price': []
}

conditions = ['Fair', 'Good', 'Excellent', 'Like New']

print("Generating data for 1000 phones...")

for _ in range(1000):
    brand_name = random.choice(list(PHONE_DB.keys()))
    new_price = PHONE_DB[brand_name]
    
    s = random.choice([64, 128, 256, 512])
    c = random.choice(conditions)
    
    # LOGIC: How much value does it lose?
    # Base used price is roughly 50-70% of new price
    depreciation = random.uniform(0.4, 0.6) 
    
    # Adjust based on condition
    if c == 'Fair': depreciation -= 0.15
    if c == 'Good': depreciation -= 0.05
    if c == 'Excellent': depreciation += 0.05
    if c == 'Like New': depreciation += 0.10
    
    # Storage bonus
    if s == 128: new_price += 5000
    if s == 256: new_price += 10000
    if s == 512: new_price += 18000
    
    final_used_price = new_price * depreciation
    
    data['brand'].append(brand_name)
    data['storage_gb'].append(s)
    data['condition'].append(c)
    data['price'].append(int(final_used_price))

# Save the dataset
df = pd.DataFrame(data)
df.to_csv('phones.csv', index=False)

# CRITICAL: Save the Master DB so the App knows the "New" prices later!
joblib.dump(PHONE_DB, 'phone_mrp_db.pkl')

print("✅ Data generated & MRP Database saved as 'phone_mrp_db.pkl'")