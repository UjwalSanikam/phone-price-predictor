import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Define the Master List of "New" Prices (MRP) for the phones in your CSV
# I extracted these brands from your file to ensure they match perfectly.
PHONE_MRP_DB = {
    # Apple
    'iPhone 11': 30000, 'iPhone 12': 40000, 'iPhone 13': 50000, 
    'iPhone 14': 60000, 'iPhone 15': 70000, 'iPhone 15 Pro': 120000,
    
    # Samsung
    'Samsung S20': 25000, 'Samsung S21': 35000, 'Samsung S22': 45000, 
    'Samsung S23': 60000, 'Samsung S24 Ultra': 125000,
    
    # Google Pixel
    'Pixel 6': 30000, 'Pixel 7': 40000, 'Pixel 8': 65000,
    
    # OnePlus
    'OnePlus 9': 30000, 'OnePlus 10 Pro': 40000, 'OnePlus 11': 50000, 'OnePlus 12': 65000,
    
    # Others
    'Redmi Note 12': 15000, 'Redmi Note 13 Pro': 25000, 'Realme GT': 30000
}

print("🚀 Starting Project Setup...")

# 2. Load your Kaggle Dataset
try:
    df = pd.read_csv('phones.csv')
    print(f"✅ Loaded phones.csv with {len(df)} rows.")
except FileNotFoundError:
    print("❌ Error: 'phones.csv' not found. Make sure it is in this folder.")
    exit()

# 3. Save the MRP Database (Critical for the App!)
joblib.dump(PHONE_MRP_DB, 'phone_mrp_db.pkl')
print("✅ Generated 'phone_mrp_db.pkl' (for New Price comparison)")

# 4. Prepare Data for Training
print("⏳ Training AI Model...")
le_brand = LabelEncoder()
df['brand'] = le_brand.fit_transform(df['brand'])

le_condition = LabelEncoder()
df['condition'] = le_condition.fit_transform(df['condition'])

X = df[['brand', 'storage_gb', 'condition']]
y = df['price']

# 5. Train the Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 6. Save the Brains
joblib.dump(model, 'price_predictor_model.pkl')
joblib.dump(le_brand, 'le_brand.pkl')
joblib.dump(le_condition, 'le_condition.pkl')

print("✅ Success! Model trained and saved.")
print("👉 You can now run: streamlit run app.py")