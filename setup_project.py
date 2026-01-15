import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

print("🚀 Starting Automatic Setup...")

# 1. Load the Kaggle Data
try:
    df = pd.read_csv('phones.csv')
    print(f"✅ Loaded data with {len(df)} rows.")
except FileNotFoundError:
    print("❌ Error: 'phones.csv' not found.")
    exit()

# 2. AUTOMATICALLY Build the 'Rules' Database
# We don't type anything. We let pandas find the unique values.
print("🧠 Learning phone specs from data...")

phone_db = {}
all_brands = df['brand'].unique()

for brand in all_brands:
    # Get all rows for this specific phone
    brand_data = df[df['brand'] == brand]
    
    # Rule 1: Find valid storage options found in the CSV
    valid_storage = sorted(brand_data['storage_gb'].unique().tolist())
    
    # Rule 2: Estimate the "New Price" (MRP)
    # Logic: The most expensive 'Like New' version in our data is likely close to MRP.
    # We add 20% to the max used price to estimate the original retail price.
    max_used_price = brand_data['price'].max()
    estimated_mrp = int(max_used_price * 1.20) 
    
    # Save to our dictionary
    phone_db[brand] = {
        'mrp': estimated_mrp,
        'storage': valid_storage
    }

print(f"✅ Learned rules for {len(phone_db)} models automatically!")
joblib.dump(phone_db, 'phone_mrp_db.pkl')

# 3. Train the Model (Standard)
print("⏳ Training AI Model...")
le_brand = LabelEncoder()
df['brand'] = le_brand.fit_transform(df['brand'])

le_condition = LabelEncoder()
df['condition'] = le_condition.fit_transform(df['condition'])

X = df[['brand', 'storage_gb', 'condition']]
y = df['price']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'price_predictor_model.pkl')
joblib.dump(le_brand, 'le_brand.pkl')
joblib.dump(le_condition, 'le_condition.pkl')

print("✅ Success! System is ready for any number of phones.")