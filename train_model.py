import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib  # This library saves our model to a file

print("⏳ Training the model...")

# 1. Load the textbook (Data)
df = pd.read_csv('phones.csv')

# 2. Convert words to numbers (Preprocessing)
# Computers can't understand "iPhone" or "Good". We assign them numbers.
le_brand = LabelEncoder()
df['brand'] = le_brand.fit_transform(df['brand'])

le_condition = LabelEncoder()
df['condition'] = le_condition.fit_transform(df['condition'])

# 3. Separate the "Questions" (X) from the "Answers" (y)
X = df[['brand', 'storage_gb', 'condition']]
y = df['price']

# 4. Train the Brain!
# We use a Random Forest (a group of decision trees)
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# 5. Save the Brain so we can use it later
joblib.dump(model, 'price_predictor_model.pkl')
joblib.dump(le_brand, 'le_brand.pkl')
joblib.dump(le_condition, 'le_condition.pkl')

print("✅ Success! Model trained and saved as 'price_predictor_model.pkl'")