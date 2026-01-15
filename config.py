"""
TechResell Pro Configuration File
Centralized settings for easy customization
"""

# ============ MODEL CONFIGURATION ============
MODEL_CONFIG = {
    'algorithm': 'GradientBoostingRegressor',
    'n_estimators': 200,
    'learning_rate': 0.1,
    'max_depth': 6,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42,
    'test_size': 0.2,
}

# ============ DATA GENERATION CONFIG ============
DATA_CONFIG = {
    'num_samples': 2000,
    'storage_options': [64, 128, 256, 512],
    'condition_options': ['Fair', 'Good', 'Excellent', 'Like New'],
    'age_range': (3, 48),  # months
    'battery_range': (60, 100),  # percentage
    'depreciation_range': (0.35, 0.65),  # base depreciation
}

# ============ PHONE DATABASE ============
PHONE_DB = {
    # Apple
    'iPhone 11': 40000,
    'iPhone 12': 50000,
    'iPhone 13': 60000,
    'iPhone 14': 70000,
    'iPhone 15': 80000,
    'iPhone 15 Plus': 95000,
    'iPhone 15 Pro': 130000,
    
    # Samsung
    'Samsung A54': 35000,
    'Samsung A74': 42000,
    'Samsung S20': 30000,
    'Samsung S21': 40000,
    'Samsung S22': 55000,
    'Samsung S23': 75000,
    'Samsung S24': 80000,
    'Samsung S24 Ultra': 130000,
    
    # OnePlus
    'OnePlus 9': 35000,
    'OnePlus 10 Pro': 45000,
    'OnePlus 11': 55000,
    'OnePlus 12': 65000,
    
    # Google
    'Pixel 6': 30000,
    'Pixel 7': 45000,
    'Pixel 8': 70000,
    'Pixel 8 Pro': 100000,
    
    # Xiaomi
    'Xiaomi 13': 50000,
    'Redmi Note 12': 15000,
    'Redmi Note 13 Pro': 25000,
    
    # Other Brands
    'Realme GT': 28000,
    'Vivo X80': 55000,
    'Motorola Edge 40': 30000,
}

# ============ APP CONFIGURATION ============
APP_CONFIG = {
    'page_title': 'TechResell Pro',
    'page_icon': '📱',
    'layout': 'wide',
    'initial_sidebar_state': 'auto',
}

# ============ PRICING FACTORS ============
PRICING_FACTORS = {
    'condition': {
        'Fair': -0.15,
        'Good': -0.05,
        'Excellent': 0.05,
        'Like New': 0.10,
    },
    'storage_bonus': {  # per 64GB increase
        128: 5000,
        256: 10000,
        512: 18000,
    },
    'battery_influence': 0.2,  # 20% of final price
    'age_degradation': 1.0 / 120,  # per month over 10 years
}

# ============ UI/UX SETTINGS ============
UI_CONFIG = {
    'color_gradient_start': '#00C9FF',
    'color_gradient_end': '#92FE9D',
    'metrics_font_size': 24,
    'button_height': 50,
}

# ============ THRESHOLDS FOR RECOMMENDATIONS ============
RECOMMENDATION_THRESHOLDS = {
    'great_deal_savings_pct': 50,  # > 50% savings
    'good_deal_savings_pct': 30,   # 30-50% savings
    'premium_retention_pct': 70,   # > 70% value retention
    'battery_warning_threshold': 80,  # < 80% battery
    'age_warning_months': 24,  # > 24 months old
}

# ============ FILE PATHS ============
FILE_PATHS = {
    'model': 'price_predictor_model.pkl',
    'le_brand': 'le_brand.pkl',
    'le_condition': 'le_condition.pkl',
    'phone_db': 'phone_mrp_db.pkl',
    'data': 'phones.csv',
}

# ============ EXPORT SETTINGS ============
EXPORT_CONFIG = {
    'csv_delimiter': ',',
    'include_timestamp': True,
    'filename_prefix': 'valuation_report',
}

def get_config(section):
    """
    Get configuration section
    
    Args:
        section (str): Configuration section name
    
    Returns:
        dict: Configuration dictionary
    """
    configs = {
        'model': MODEL_CONFIG,
        'data': DATA_CONFIG,
        'phones': PHONE_DB,
        'app': APP_CONFIG,
        'pricing': PRICING_FACTORS,
        'ui': UI_CONFIG,
        'recommendations': RECOMMENDATION_THRESHOLDS,
        'files': FILE_PATHS,
        'export': EXPORT_CONFIG,
    }
    return configs.get(section, {})

def update_phone_db(brand, mrp):
    """Add or update phone in database"""
    PHONE_DB[brand] = mrp
    return f"✅ {brand} added/updated with MRP: ₹{mrp:,}"

def update_model_config(param, value):
    """Update model configuration parameter"""
    if param in MODEL_CONFIG:
        MODEL_CONFIG[param] = value
        return f"✅ {param} updated to {value}"
    return f"❌ Parameter '{param}' not found"

if __name__ == "__main__":
    print("TechResell Pro Configuration")
    print("=" * 50)
    print(f"Total Brands: {len(PHONE_DB)}")
    print(f"Model Algorithm: {MODEL_CONFIG['algorithm']}")
    print(f"Training Samples: {DATA_CONFIG['num_samples']}")
    print(f"Storage Options: {DATA_CONFIG['storage_options']}")
    print("=" * 50)
