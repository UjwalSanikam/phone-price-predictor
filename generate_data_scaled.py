import pandas as pd
import numpy as np
import random
import joblib
import argparse
from datetime import datetime, timedelta

"""
Scalable Phone Dataset Generator
Generates realistic phone pricing data with millions of samples
Supports configurable size, features, and realistic distributions
"""

# Extended Phone Database with Years and Variants
PHONE_DB_EXTENDED = {
    # Apple iPhone (2018-2025)
    'iPhone XS': {'base_mrp': 100000, 'min_year': 2018, 'max_year': 2020},
    'iPhone XR': {'base_mrp': 80000, 'min_year': 2018, 'max_year': 2020},
    'iPhone 11': {'base_mrp': 50000, 'min_year': 2019, 'max_year': 2021},
    'iPhone 12': {'base_mrp': 60000, 'min_year': 2020, 'max_year': 2022},
    'iPhone 13': {'base_mrp': 70000, 'min_year': 2021, 'max_year': 2023},
    'iPhone 14': {'base_mrp': 80000, 'min_year': 2022, 'max_year': 2024},
    'iPhone 15': {'base_mrp': 90000, 'min_year': 2023, 'max_year': 2025},
    'iPhone 12 Pro': {'base_mrp': 120000, 'min_year': 2020, 'max_year': 2022},
    'iPhone 13 Pro': {'base_mrp': 130000, 'min_year': 2021, 'max_year': 2023},
    'iPhone 14 Pro': {'base_mrp': 140000, 'min_year': 2022, 'max_year': 2024},
    'iPhone 15 Pro': {'base_mrp': 150000, 'min_year': 2023, 'max_year': 2025},
    
    # Samsung Galaxy S (2018-2025)
    'Samsung S9': {'base_mrp': 80000, 'min_year': 2018, 'max_year': 2020},
    'Samsung S10': {'base_mrp': 90000, 'min_year': 2019, 'max_year': 2021},
    'Samsung S20': {'base_mrp': 80000, 'min_year': 2020, 'max_year': 2022},
    'Samsung S21': {'base_mrp': 90000, 'min_year': 2021, 'max_year': 2023},
    'Samsung S22': {'base_mrp': 100000, 'min_year': 2022, 'max_year': 2024},
    'Samsung S23': {'base_mrp': 110000, 'min_year': 2023, 'max_year': 2025},
    'Samsung S24': {'base_mrp': 120000, 'min_year': 2024, 'max_year': 2025},
    'Samsung S21 Ultra': {'base_mrp': 120000, 'min_year': 2021, 'max_year': 2023},
    'Samsung S23 Ultra': {'base_mrp': 130000, 'min_year': 2023, 'max_year': 2025},
    'Samsung S24 Ultra': {'base_mrp': 140000, 'min_year': 2024, 'max_year': 2025},
    
    # Samsung Galaxy A (Budget)
    'Samsung A10': {'base_mrp': 10000, 'min_year': 2019, 'max_year': 2021},
    'Samsung A20': {'base_mrp': 12000, 'min_year': 2019, 'max_year': 2021},
    'Samsung A30': {'base_mrp': 15000, 'min_year': 2019, 'max_year': 2021},
    'Samsung A50': {'base_mrp': 25000, 'min_year': 2019, 'max_year': 2021},
    'Samsung A51': {'base_mrp': 25000, 'min_year': 2020, 'max_year': 2022},
    'Samsung A52': {'base_mrp': 30000, 'min_year': 2021, 'max_year': 2023},
    'Samsung A53': {'base_mrp': 35000, 'min_year': 2022, 'max_year': 2024},
    'Samsung A54': {'base_mrp': 40000, 'min_year': 2023, 'max_year': 2025},
    
    # Google Pixel
    'Pixel 3': {'base_mrp': 70000, 'min_year': 2018, 'max_year': 2020},
    'Pixel 4': {'base_mrp': 80000, 'min_year': 2019, 'max_year': 2021},
    'Pixel 5': {'base_mrp': 50000, 'min_year': 2020, 'max_year': 2022},
    'Pixel 6': {'base_mrp': 60000, 'min_year': 2021, 'max_year': 2023},
    'Pixel 7': {'base_mrp': 70000, 'min_year': 2022, 'max_year': 2024},
    'Pixel 8': {'base_mrp': 80000, 'min_year': 2023, 'max_year': 2025},
    'Pixel 6 Pro': {'base_mrp': 90000, 'min_year': 2021, 'max_year': 2023},
    'Pixel 7 Pro': {'base_mrp': 100000, 'min_year': 2022, 'max_year': 2024},
    'Pixel 8 Pro': {'base_mrp': 110000, 'min_year': 2023, 'max_year': 2025},
    
    # OnePlus
    'OnePlus 6': {'base_mrp': 35000, 'min_year': 2018, 'max_year': 2020},
    'OnePlus 7': {'base_mrp': 40000, 'min_year': 2019, 'max_year': 2021},
    'OnePlus 8': {'base_mrp': 45000, 'min_year': 2020, 'max_year': 2022},
    'OnePlus 9': {'base_mrp': 50000, 'min_year': 2021, 'max_year': 2023},
    'OnePlus 10': {'base_mrp': 55000, 'min_year': 2022, 'max_year': 2024},
    'OnePlus 11': {'base_mrp': 60000, 'min_year': 2023, 'max_year': 2025},
    'OnePlus 9 Pro': {'base_mrp': 65000, 'min_year': 2021, 'max_year': 2023},
    
    # Xiaomi Redmi
    'Redmi Note 7': {'base_mrp': 10000, 'min_year': 2019, 'max_year': 2021},
    'Redmi Note 8': {'base_mrp': 12000, 'min_year': 2019, 'max_year': 2021},
    'Redmi Note 9': {'base_mrp': 13000, 'min_year': 2020, 'max_year': 2022},
    'Redmi Note 10': {'base_mrp': 15000, 'min_year': 2021, 'max_year': 2023},
    'Redmi Note 11': {'base_mrp': 18000, 'min_year': 2022, 'max_year': 2024},
    'Redmi Note 12': {'base_mrp': 20000, 'min_year': 2023, 'max_year': 2025},
    'Redmi Note 13': {'base_mrp': 22000, 'min_year': 2024, 'max_year': 2025},
    
    # Realme
    'Realme 5': {'base_mrp': 10000, 'min_year': 2019, 'max_year': 2021},
    'Realme 6': {'base_mrp': 12000, 'min_year': 2020, 'max_year': 2022},
    'Realme 7': {'base_mrp': 15000, 'min_year': 2020, 'max_year': 2022},
    'Realme 8': {'base_mrp': 16000, 'min_year': 2021, 'max_year': 2023},
    'Realme 9': {'base_mrp': 18000, 'min_year': 2022, 'max_year': 2024},
    'Realme GT': {'base_mrp': 35000, 'min_year': 2021, 'max_year': 2023},
    
    # Vivo
    'Vivo V15': {'base_mrp': 28000, 'min_year': 2019, 'max_year': 2021},
    'Vivo V17': {'base_mrp': 30000, 'min_year': 2019, 'max_year': 2021},
    'Vivo V19': {'base_mrp': 35000, 'min_year': 2020, 'max_year': 2022},
    'Vivo X50': {'base_mrp': 45000, 'min_year': 2020, 'max_year': 2022},
    'Vivo X60': {'base_mrp': 50000, 'min_year': 2021, 'max_year': 2023},
    'Vivo X80': {'base_mrp': 55000, 'min_year': 2022, 'max_year': 2024},
    
    # Motorola
    'Motorola G7': {'base_mrp': 15000, 'min_year': 2019, 'max_year': 2021},
    'Motorola G8': {'base_mrp': 16000, 'min_year': 2020, 'max_year': 2022},
    'Motorola G9': {'base_mrp': 18000, 'min_year': 2020, 'max_year': 2022},
    'Motorola G30': {'base_mrp': 16000, 'min_year': 2021, 'max_year': 2023},
    'Motorola G50': {'base_mrp': 12000, 'min_year': 2021, 'max_year': 2023},
    'Motorola Edge': {'base_mrp': 25000, 'min_year': 2020, 'max_year': 2022},
    'Motorola Edge 40': {'base_mrp': 30000, 'min_year': 2023, 'max_year': 2025},
}

# Operating Systems
OS_OPTIONS = {
    'iOS 14': 0.03,
    'iOS 15': 0.06,
    'iOS 16': 0.12,
    'iOS 17': 0.18,
    'iOS 18': 0.15,
    'Android 9': 0.01,
    'Android 10': 0.02,
    'Android 11': 0.06,
    'Android 12': 0.09,
    'Android 13': 0.15,
    'Android 14': 0.12,
    'Android 15': 0.01,
}

# Color Options
COLOR_OPTIONS = ['Space Black', 'Silver', 'Gold', 'Blue', 'Red', 'Green', 'White', 'Black', 'Purple', 'Midnight']

# Network Support
NETWORK_OPTIONS = ['4G', '5G']

CONDITIONS = ['Fair', 'Good', 'Excellent', 'Like New']

def generate_scalable_dataset(num_samples=1000000, output_file='phones_scaled.csv', batch_size=100000):
    """
    Generate large-scale phone dataset with streaming to avoid memory overload
    """
    print(f"📊 Generating {num_samples:,} phone records...")
    
    # Initialize CSV with headers
    headers = [
        'brand', 'model', 'release_year', 'storage_gb', 'condition', 'age_months',
        'battery_health', 'os', 'camera_count', 'screen_size', 'color', 'network',
        'trade_in_value', 'seller_rating', 'price'
    ]
    
    processed = 0
    file_mode = 'w'
    
    while processed < num_samples:
        batch_actual_size = min(batch_size, num_samples - processed)
        batch_data = {col: [] for col in headers}
        
        for _ in range(batch_actual_size):
            # Select random phone
            model_name = random.choice(list(PHONE_DB_EXTENDED.keys()))
            phone_info = PHONE_DB_EXTENDED[model_name]
            
            # Release year
            release_year = random.randint(phone_info['min_year'], phone_info['max_year'])
            current_year = 2025
            max_purchase_year = min(current_year - 1, release_year + 3)
            purchase_year = random.randint(release_year, max(release_year, max_purchase_year))
            age_months = (current_year - purchase_year) * 12 + random.randint(0, 11)
            
            # Storage
            storage = random.choice([64, 128, 256, 512])
            
            # Condition
            condition = random.choice(CONDITIONS)
            
            # Battery health (degradation over time)
            base_battery = random.randint(80, 100)
            battery_degradation = (age_months / 12) * 5
            battery_health = max(20, base_battery - battery_degradation + random.gauss(0, 3))
            
            # OS (weighted towards newer)
            os = np.random.choice(list(OS_OPTIONS.keys()), p=list(OS_OPTIONS.values()))
            
            # Camera (realistic: 1-5 cameras)
            camera_count = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.20, 0.35, 0.30, 0.10])
            
            # Screen size (realistic: 5.0 to 6.8 inches)
            screen_size = round(random.uniform(5.0, 6.8), 1)
            
            # Color
            color = random.choice(COLOR_OPTIONS)
            
            # Network
            network = random.choice(NETWORK_OPTIONS)
            
            # Seller rating (1-5 stars)
            seller_rating = round(random.uniform(3.0, 5.0), 1)
            
            # Base price calculation
            base_mrp = phone_info['base_mrp']
            
            # Storage premium
            storage_premium = (storage - 64) * 50 if storage > 64 else 0
            
            # Year depreciation
            year_factor = max(0.3, 1.0 - (current_year - purchase_year) * 0.15)
            
            # Condition factor
            condition_factor = {
                'Fair': 0.40,
                'Good': 0.60,
                'Excellent': 0.75,
                'Like New': 0.85
            }[condition]
            
            # Battery factor
            battery_factor = battery_health / 100
            
            # Seller rating factor (better rating = slightly higher price)
            seller_factor = 0.95 + (seller_rating / 5) * 0.10
            
            # Camera premium
            camera_premium = (camera_count - 1) * 2000
            
            # Calculate final price
            used_price = (base_mrp + storage_premium + camera_premium) * year_factor * condition_factor * battery_factor * seller_factor
            trade_in_est = used_price * 0.85
            
            # Add to batch
            batch_data['brand'].append(model_name.split()[0])
            batch_data['model'].append(model_name)
            batch_data['release_year'].append(release_year)
            batch_data['storage_gb'].append(storage)
            batch_data['condition'].append(condition)
            batch_data['age_months'].append(age_months)
            batch_data['battery_health'].append(int(battery_health))
            batch_data['os'].append(os)
            batch_data['camera_count'].append(camera_count)
            batch_data['screen_size'].append(screen_size)
            batch_data['color'].append(color)
            batch_data['network'].append(network)
            batch_data['trade_in_value'].append(int(trade_in_est))
            batch_data['seller_rating'].append(seller_rating)
            batch_data['price'].append(int(used_price))
        
        # Write batch to CSV
        df_batch = pd.DataFrame(batch_data)
        df_batch.to_csv(output_file, mode=file_mode, header=(file_mode == 'w'), index=False)
        
        processed += batch_actual_size
        file_mode = 'a'  # Append mode for subsequent batches
        
        percent = (processed / num_samples) * 100
        print(f"   ✅ {processed:,} / {num_samples:,} records ({percent:.1f}%)")
    
    print(f"✅ Dataset saved to {output_file}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate scalable phone dataset')
    parser.add_argument('--size', type=int, default=1000000, help='Number of samples to generate (default: 1M)')
    parser.add_argument('--output', type=str, default='phones_scaled.csv', help='Output filename')
    parser.add_argument('--batch', type=int, default=100000, help='Batch size (default: 100k)')
    
    args = parser.parse_args()
    
    print("🚀 Scalable Phone Dataset Generator")
    print("=" * 60)
    
    start_time = datetime.now()
    generate_scalable_dataset(num_samples=args.size, output_file=args.output, batch_size=args.batch)
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"⏱️  Generated in {elapsed:.1f} seconds")
    print(f"📊 Features: 15 (brand, model, year, storage, condition, age, battery, OS, camera, screen, color, network, trade-in, rating, price)")
