import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import lightgbm as lgb
import joblib
import argparse

"""
Scalable ML Training Pipeline
Optimized for datasets with 1M+ samples
Uses LightGBM for memory efficiency and speed
"""

def train_scalable_model(data_file='phones_scaled.csv', sample_rate=1.0, max_samples=None):
    """
    Train LightGBM model on large-scale phone dataset
    
    Args:
        data_file: Input CSV path
        sample_rate: Fraction of data to use (0.1 = 10% for testing)
        max_samples: Max samples to load (None = all)
    """
    
    print("📊 Loading dataset...")
    df = pd.read_csv(data_file)
    
    # Sample if needed
    if sample_rate < 1.0:
        df = df.sample(frac=sample_rate, random_state=42)
        print(f"   Sampled {sample_rate*100:.1f}% → {len(df):,} rows")
    
    if max_samples and len(df) > max_samples:
        df = df.sample(n=max_samples, random_state=42)
        print(f"   Limited to {max_samples:,} rows")
    
    print(f"   Total: {len(df):,} samples with {len(df.columns)} features")
    
    # Feature Engineering
    print("\n🔧 Engineering features...")
    
    # Encode categorical variables
    le_brand = LabelEncoder()
    df['brand_encoded'] = le_brand.fit_transform(df['brand'])
    
    le_os = LabelEncoder()
    df['os_encoded'] = le_os.fit_transform(df['os'])
    
    le_color = LabelEncoder()
    df['color_encoded'] = le_color.fit_transform(df['color'])
    
    le_condition = LabelEncoder()
    df['condition_encoded'] = le_condition.fit_transform(df['condition'])
    
    le_network = LabelEncoder()
    df['network_encoded'] = le_network.fit_transform(df['network'])
    
    # Additional engineered features
    df['model_age_factor'] = 2025 - df['release_year']  # How old is the model
    df['storage_category'] = pd.cut(df['storage_gb'], bins=[0, 64, 128, 256, 512], labels=[0, 1, 2, 3]).astype(int)
    df['screen_size_category'] = pd.cut(df['screen_size'], bins=[0, 5.5, 6.1, 6.9], labels=[0, 1, 2]).astype(int)
    df['overall_condition_score'] = (
        df['battery_health'] * 0.4 +
        df['condition_encoded'] * 25 +
        df['seller_rating'] * 20
    )
    
    # Select features for model
    feature_cols = [
        'brand_encoded', 'storage_gb', 'condition_encoded', 'age_months', 
        'battery_health', 'os_encoded', 'camera_count', 'screen_size', 
        'color_encoded', 'network_encoded', 'seller_rating', 'trade_in_value',
        'model_age_factor', 'storage_category', 'screen_size_category', 'overall_condition_score'
    ]
    
    X = df[feature_cols].copy()
    y = df['price'].copy()
    
    print(f"   Features: {len(feature_cols)}")
    print(f"   Target range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
    
    # Train/Test Split
    print("\n📂 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"   Train: {len(X_train):,} | Test: {len(X_test):,}")
    
    # Create LightGBM datasets
    train_data = lgb.Dataset(X_train, label=y_train, free_raw_data=False)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data, free_raw_data=False)
    
    # LightGBM Parameters (optimized for large data)
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'num_leaves': 64,
        'learning_rate': 0.05,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1,
        'max_depth': 8,
        'min_child_samples': 20,
    }
    
    # Train
    print("\n🧠 Training LightGBM model...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=500,
        valid_sets=[test_data],
        valid_names=['test'],
        callbacks=[
            lgb.log_evaluation(period=50),
            lgb.early_stopping(stopping_rounds=50),
        ]
    )
    
    # Evaluate
    print("\n📊 Model Evaluation:")
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    mae = mean_absolute_error(y_test, y_test_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    print(f"   Training R² Score:  {train_r2:.4f}")
    print(f"   Testing R² Score:   {test_r2:.4f}")
    print(f"   Mean Absolute Error: ₹{mae:,.0f}")
    print(f"   RMSE:               ₹{rmse:,.0f}")
    
    # Feature Importance
    print("\n🔝 Top 10 Important Features:")
    importance = model.feature_importance(importance_type='gain')
    feature_importance = list(zip(feature_cols, importance))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    for i, (feat, imp) in enumerate(feature_importance[:10], 1):
        print(f"   {i}. {feat}: {imp:,.0f}")
    
    # Save models
    print("\n💾 Saving models...")
    model.save_model('price_predictor_lgb.pkl')
    joblib.dump(le_brand, 'le_brand.pkl')
    joblib.dump(le_os, 'le_os.pkl')
    joblib.dump(le_color, 'le_color.pkl')
    joblib.dump(le_condition, 'le_condition.pkl')
    joblib.dump(le_network, 'le_network.pkl')
    
    print("✅ Models saved!")
    print(f"\n   price_predictor_lgb.pkl")
    print(f"   le_brand.pkl, le_os.pkl, le_color.pkl, le_condition.pkl, le_network.pkl")
    
    # Force garbage collection and flush
    import gc
    gc.collect()
    print("✅ Complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train scalable phone pricing model')
    parser.add_argument('--data', type=str, default='phones_scaled.csv', help='Input data file')
    parser.add_argument('--sample', type=float, default=1.0, help='Sample fraction (0-1)')
    parser.add_argument('--max', type=int, default=None, help='Max samples to use')
    
    args = parser.parse_args()
    
    print("🚀 Scalable Model Training Pipeline")
    print("=" * 60)
    
    train_scalable_model(data_file=args.data, sample_rate=args.sample, max_samples=args.max)
