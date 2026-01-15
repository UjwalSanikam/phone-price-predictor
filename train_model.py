import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

print("⏳ Retraining model with expanded dataset...")

# 1. Load Data
df = pd.read_csv('phones.csv')

# 2. Preprocessing
le_brand = LabelEncoder()
df['brand'] = le_brand.fit_transform(df['brand'])

le_condition = LabelEncoder()
df['condition'] = le_condition.fit_transform(df['condition'])

# 3. Train
X = df[['brand', 'storage_gb', 'condition']]
y = df['price']

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# 4. Save
joblib.dump(model, 'price_predictor_model.pkl')
joblib.dump(le_brand, 'le_brand.pkl')
joblib.dump(le_condition, 'le_condition.pkl')

print("✅ New Model Trained with 20+ brands!")