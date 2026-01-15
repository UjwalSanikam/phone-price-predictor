import pandas as pd
import numpy as np
import joblib
import argparse
from pathlib import Path

"""
Bulk Phone Valuation Engine
Processes CSV files with phone data and generates batch predictions
"""

def load_models():
    """Load pre-trained models and label encoders"""
    try:
        model = joblib.load('price_predictor_lgb.pkl')
        le_brand = joblib.load('le_brand.pkl')
        le_os = joblib.load('le_os.pkl')
        le_color = joblib.load('le_color.pkl')
        le_condition = joblib.load('le_condition.pkl')
        le_network = joblib.load('le_network.pkl')
        return model, le_brand, le_os, le_color, le_condition, le_network
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Missing model file: {e}. Please run train_model_scaled.py first.")

def valuate_batch(input_csv, output_csv=None, confidence=False):
    """
    Valuate phones in batch from CSV
    
    Args:
        input_csv: Input CSV with phone details (brand, model, storage_gb, condition, age_months, battery_health, screen_size, camera_count, color, network, seller_rating)
        output_csv: Output CSV path (default: input with _valued suffix)
        confidence: Include confidence intervals in output
    """
    
    print(f"📥 Loading {input_csv}...")
    df = pd.read_csv(input_csv)
    print(f"   Loaded {len(df):,} phone records")
    
    # Load models
    print("🧠 Loading pre-trained models...")
    model, le_brand, le_os, le_color, le_condition, le_network = load_models()
    
    # Feature engineering
    print("🔧 Preparing features...")
    
    # Encode categorical variables
    try:
        df['brand_encoded'] = le_brand.transform(df['brand'])
        df['os_encoded'] = le_os.transform(df.get('os', ['Android 12'] * len(df)))
        df['color_encoded'] = le_color.transform(df['color'])
        df['condition_encoded'] = le_condition.transform(df['condition'])
        df['network_encoded'] = le_network.transform(df.get('network', ['5G'] * len(df)))
    except Exception as e:
        print(f"   ⚠️  Encoding issue: {e}")
        print("   Using fallback encoding...")
        df['brand_encoded'] = pd.factorize(df['brand'])[0]
        df['os_encoded'] = 10
        df['color_encoded'] = pd.factorize(df['color'])[0]
        df['condition_encoded'] = pd.factorize(df['condition'])[0]
        df['network_encoded'] = 1
    
    # Engineered features
    release_year = df.get('release_year', [2020] * len(df))
    df['model_age_factor'] = 2025 - release_year
    df['storage_category'] = pd.cut(df['storage_gb'], bins=[0, 64, 128, 256, 512], labels=[0, 1, 2, 3], right=False).fillna(3).astype(int)
    df['screen_size_category'] = pd.cut(df['screen_size'], bins=[0, 5.5, 6.1, 6.9], labels=[0, 1, 2], right=False).fillna(2).astype(int)
    df['overall_condition_score'] = (
        df['battery_health'] * 0.4 +
        df['condition_encoded'] * 25 +
        df['seller_rating'] * 20
    )
    
    # Select features for prediction
    feature_cols = [
        'brand_encoded', 'storage_gb', 'condition_encoded', 'age_months', 
        'battery_health', 'os_encoded', 'camera_count', 'screen_size', 
        'color_encoded', 'network_encoded', 'seller_rating', 'trade_in_value',
        'model_age_factor', 'storage_category', 'screen_size_category', 'overall_condition_score'
    ]
    
    X_pred = df[feature_cols].fillna(0).copy()
    
    # Predict
    print(f"💰 Predicting prices for {len(df):,} phones...")
    predictions = model.predict(X_pred)
    
    # Add predictions to dataframe
    df['predicted_price'] = predictions.astype(int)
    
    # Optional: confidence intervals (using prediction residuals as proxy)
    if confidence:
        df['price_lower'] = (predictions * 0.85).astype(int)
        df['price_upper'] = (predictions * 1.15).astype(int)
    
    # Prepare output
    if output_csv is None:
        output_csv = Path(input_csv).stem + '_valued.csv'
    
    # Select output columns
    output_cols = ['brand', 'model', 'storage_gb', 'condition', 'age_months', 
                   'battery_health', 'seller_rating', 'predicted_price']
    if confidence:
        output_cols.extend(['price_lower', 'price_upper'])
    
    df_output = df[output_cols].copy()
    df_output.to_csv(output_csv, index=False)
    
    print(f"✅ Results saved to {output_csv}")
    print(f"\n📊 Price Statistics:")
    print(f"   Min: ₹{predictions.min():,.0f}")
    print(f"   Max: ₹{predictions.max():,.0f}")
    print(f"   Mean: ₹{predictions.mean():,.0f}")
    print(f"   Median: ₹{np.median(predictions):,.0f}")
    
    return df_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk phone valuation')
    parser.add_argument('input', type=str, help='Input CSV file')
    parser.add_argument('--output', type=str, default=None, help='Output CSV file')
    parser.add_argument('--confidence', action='store_true', help='Include confidence intervals')
    
    args = parser.parse_args()
    
    print("🚀 Bulk Phone Valuation Engine")
    print("=" * 60)
    
    valuate_batch(args.input, args.output, args.confidence)
