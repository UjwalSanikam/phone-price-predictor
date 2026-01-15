import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import numpy as np

print("⏳ Retraining model with expanded dataset and advanced features...")

# 1. Load Data
df = pd.read_csv('phones.csv')

# 2. Preprocessing
le_brand = LabelEncoder()
df['brand_encoded'] = le_brand.fit_transform(df['brand'])

le_condition = LabelEncoder()
df['condition_encoded'] = le_condition.fit_transform(df['condition'])

# 3. Feature Engineering
df['storage_log'] = np.log1p(df['storage_gb'])
df['condition_score'] = (le_condition.transform(df['condition']) + 1) * 20

# 4. Train/Test Split
X = df[['brand_encoded', 'storage_gb', 'condition_encoded', 'age_months', 'battery_health']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train with better model
model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)
model.fit(X_train, y_train)

# 6. Evaluate
train_score = r2_score(y_train, model.predict(X_train))
test_score = r2_score(y_test, model.predict(X_test))
mae = mean_absolute_error(y_test, model.predict(X_test))
rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))

print(f"✅ Model Performance:")
print(f"   Training R² Score: {train_score:.4f}")
print(f"   Testing R² Score: {test_score:.4f}")
print(f"   Mean Absolute Error: ₹{mae:,.0f}")
print(f"   RMSE: ₹{rmse:,.0f}")

# 7. Save
joblib.dump(model, 'price_predictor_model.pkl')
joblib.dump(le_brand, 'le_brand.pkl')
joblib.dump(le_condition, 'le_condition.pkl')

print(f"✅ New Model Trained with {len(le_brand.classes_)} brands and {len(df)} samples!")