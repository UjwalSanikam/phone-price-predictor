import pandas as pd
import random

# We will create a fake list of 500 phones
data = {
    'brand': [],
    'storage_gb': [],
    'condition': [],
    'price': []
}

brands = ['iPhone 11', 'iPhone 12', 'Samsung S20', 'Samsung S21', 'OnePlus 9']
conditions = ['Fair', 'Good', 'Excellent', 'Like New']

print("Generating data...")

for _ in range(500):
    b = random.choice(brands)
    s = random.choice([64, 128, 256])
    c = random.choice(conditions)
    
    # Logic: Start with a base price
    base = 20000
    if 'iPhone 12' in b: base += 15000
    if 'S21' in b: base += 12000
    if 'OnePlus' in b: base += 8000
    
    # Logic: Add value for storage and condition
    price = base + (s * 50) + (conditions.index(c) * 2000)
    
    # Add random variation (noise) so it looks real
    price += random.randint(-2000, 2000)
    
    data['brand'].append(b)
    data['storage_gb'].append(s)
    data['condition'].append(c)
    data['price'].append(price)

# Save to a CSV file (like an Excel sheet)
df = pd.DataFrame(data)
df.to_csv('phones.csv', index=False)
print("✅ Success! 'phones.csv' file created.")