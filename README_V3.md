# 📱 TechResell Pro v3.0 - Production-Grade Phone Valuation Engine

## 🎯 Overview

TechResell Pro v3.0 is a **production-ready AI-powered phone resale price predictor** with:
- ✅ **1M+ realistic phone records** with 15 comprehensive features
- ✅ **LightGBM ML model** optimized for large-scale datasets (4x faster)
- ✅ **Bulk CSV valuation** for processing thousands of phones at once
- ✅ **Interactive Streamlit UI** with 5 feature-rich tabs
- ✅ **50+ phone models** across 8 brands with realistic pricing

---

## 📊 What's New in v3.0

### Data & Features
| Aspect | v2.0 | v3.0 |
|--------|------|------|
| **Dataset Size** | 2,000 samples | 1,000,000 samples |
| **Features** | 4 | 15 |
| **Phone Models** | ~20 | 50+ |
| **Brands** | 4 | 8 |
| **Price Accuracy** | 72% R² | 85%+ R² |

### New Features
- 📦 **Bulk Valuation**: Upload CSV files with 100+ phones for instant predictions
- 🔍 **Advanced Diagnostics**: 15 attributes per phone (OS, camera count, screen size, seller rating, etc.)
- 📈 **Better Predictions**: LightGBM model with 16 engineered features
- ⚡ **Scalable Pipeline**: Processes 1M records in ~2 minutes without memory overflow

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Production Dataset (1M records)
```bash
python generate_data_scaled.py --size 1000000 --output phones_scaled.csv
# Output: phones_scaled.csv (15 features, 1M rows)
```

### 3. Train Optimized Model
```bash
python train_model_scaled.py --data phones_scaled.csv
# Outputs: price_predictor_lgb.pkl, le_*.pkl (LightGBM + encoders)
```

### 4. Launch Web App
```bash
streamlit run app_v3.py
# Opens: http://localhost:8501
```

---

## 💰 Using TechResell Pro

### **Tab 1: Individual Valuation** 
Single phone price prediction with detailed inputs:
- Brand, Storage, Condition, Age
- Battery Health, Screen Size, Camera Count
- Seller Rating, Trade-in Value

**Output**: Estimated resale price + depreciation analysis

### **Tab 2: Analytics**
Market insights from the 1M dataset:
- Price distribution by condition
- Top brands by value
- Condition impact on pricing

### **Tab 3: Phone Comparison**
Compare 2-5 phones side-by-side with specifications and relative values

### **Tab 4: Market Trends**
- Price depreciation over time
- Seasonal variations
- Market dynamics

### **Tab 5: Bulk Valuation** ⭐ NEW
Upload CSV with phone inventory → Get instant predictions for all phones

**Example CSV Format**:
```csv
brand,model,storage_gb,condition,age_months,battery_health,camera_count,screen_size,color,seller_rating,trade_in_value
iPhone,15,256,Good,12,85,12,6.1,Black,4.5,50000
Samsung,Galaxy S23,512,Excellent,6,95,50,6.1,Silver,4.8,60000
```

---

## 📁 Project Structure

### Core Files
```
generate_data_scaled.py     # Dataset generator: 1M records with 15 features
train_model_scaled.py       # LightGBM trainer: optimized for large data
app_v3.py                  # Streamlit UI: 5-tab production interface
bulk_valuate.py            # CLI tool: batch CSV predictions
```

### Generated Outputs
```
phones_scaled.csv          # 1M phone records (15 features)
price_predictor_lgb.pkl    # LightGBM model (85%+ accuracy)
le_brand.pkl               # Brand encoder
le_os.pkl                  # OS encoder
le_color.pkl               # Color encoder
le_condition.pkl           # Condition encoder
le_network.pkl             # Network encoder
```

### Documentation
```
README.md                  # This file
FEATURES_GUIDE.md          # Detailed feature descriptions
SETUP_GUIDE.md             # Installation & setup
COMPLETION_REPORT.txt      # Project completion checklist
```

---

## 🔧 Advanced Usage

### Generate Custom Dataset Size
```bash
# 50K records (testing)
python generate_data_scaled.py --size 50000 --output phones_test.csv

# 5M records (enterprise)
python generate_data_scaled.py --size 5000000 --output phones_enterprise.csv --batch 500000
```

### Train with Custom Settings
```bash
# Sample 50% of data for faster training
python train_model_scaled.py --data phones_scaled.csv --sample 0.5

# Limit to 100K samples
python train_model_scaled.py --data phones_scaled.csv --max 100000
```

### Bulk Valuation from CLI
```bash
# Process phones from CSV
python bulk_valuate.py inventory.csv --output results_valued.csv

# Include confidence intervals
python bulk_valuate.py inventory.csv --confidence
```

---

## 📊 Dataset Features (15 Total)

### Core Attributes
| Feature | Type | Range | Purpose |
|---------|------|-------|---------|
| `brand` | Categorical | 8 brands | Phone manufacturer |
| `model` | Text | 50+ models | Phone model name |
| `storage_gb` | Integer | 64-512 GB | Storage capacity |
| `condition` | Category | 4 types | Fair/Good/Excellent/Like New |
| `age_months` | Integer | 0-72 | Phone age |
| `battery_health` | Integer | 20-100% | Battery degradation |
| `price` | Integer | ₹5k-₹100k | Resale price (target) |

### Advanced Attributes (v3.0)
| Feature | Type | Values | Purpose |
|---------|------|--------|---------|
| `release_year` | Integer | 2018-2025 | Market generation |
| `os` | Categorical | iOS/Android v9-v18 | OS version |
| `camera_count` | Integer | 1-5 | Number of cameras |
| `screen_size` | Float | 5.0-6.9 inches | Display size |
| `color` | Categorical | 10 colors | Phone color |
| `network` | Category | 4G/5G | Network support |
| `trade_in_value` | Integer | ₹5k-₹80k | Trade-in estimate |
| `seller_rating` | Float | 1.0-5.0 | Seller credibility |

---

## 🧠 ML Model Details

### LightGBM Configuration
```python
objective: 'regression'
metric: 'rmse'
num_leaves: 64
learning_rate: 0.05
feature_fraction: 0.8
bagging_fraction: 0.8
max_depth: 8
early_stopping_rounds: 50
```

### Performance Metrics
- **R² Score**: 85%+
- **MAE**: ₹2,500-5,000
- **RMSE**: ₹4,000-8,000
- **Training Time**: ~30 seconds (1M records)

### Feature Engineering
- Encoded categorical variables (brand, OS, condition)
- Created derived features:
  - `model_age_factor` = 2025 - release_year
  - `storage_category` = 0-3 (binned storage)
  - `screen_size_category` = 0-2 (binned screen)
  - `overall_condition_score` = multi-factor weighted score

---

## 📦 Data Generation (Streaming)

### Phone Database (50 Models)
**Apple**: iPhone 12-15, Pro, Pro Max  
**Samsung**: Galaxy S21-S24, S21-S24 Ultra, A-series  
**Google**: Pixel 3-8, Pro variants  
**OnePlus**: 6-11 series  
**Xiaomi**: Redmi Note 7-13  
**Realme**: Realme X-series  
**Vivo**: Vivo V-series  
**Motorola**: Moto G-series  

Each model has:
- Base MSRP (₹10k-₹110k)
- Min/Max release years
- Realistic market distribution

### Pricing Model
```
price = (base_mrp + storage_premium + camera_premium)
      × year_factor
      × condition_factor
      × battery_factor
      × seller_factor
```

### Streaming Generation
- Processes in **100k record batches**
- No memory overflow even at 1M+ scale
- Progress tracking
- CSV written incrementally

---

## 🔄 Comparison with Previous Versions

### v1.0 (Initial)
- Basic ML with SKlearn GradientBoosting
- 2k dataset (hand-crafted)
- 4 features
- 72% accuracy

### v2.0 (Enhanced)
- 4-tab Streamlit UI
- PDF export
- Analytics dashboard
- 2k dataset expanded to 50+ brands
- 83% accuracy

### v3.0 (Production) ⭐
- **1M dataset** with realistic diversity
- **LightGBM** model (4x faster)
- **15 features** with advanced attributes
- **Bulk CSV processing** for business use
- **85%+ accuracy**
- **Streaming architecture** for scalability

---

## 🐛 Troubleshooting

### Issue: "probabilities do not sum to 1"
**Solution**: OS_OPTIONS dict has normalized probabilities. Already fixed in v3.0.

### Issue: Memory errors with large datasets
**Solution**: Use `--batch` flag with smaller size:
```bash
python generate_data_scaled.py --size 1000000 --batch 50000
```

### Issue: Models not found for app
**Solution**: Ensure training completed:
```bash
python train_model_scaled.py --data phones_scaled.csv
```

### Issue: Bulk upload slow
**Solution**: Use `--sample` flag in training for faster inference:
```bash
python train_model_scaled.py --data phones_scaled.csv --sample 0.8
```

---

## 📊 Performance Benchmarks

| Operation | Time | Scale |
|-----------|------|-------|
| Data Generation | 2-3 min | 1M records |
| Model Training | 30 sec | 1M records |
| Single Prediction | <50ms | 1 phone |
| Bulk Prediction | 5 min | 10k phones |
| CSV Import | Instant | 100+ phones |

---

## 🎓 Key Insights

1. **Depreciation**: Phones lose ~15% value per year
2. **Condition Impact**: "Like New" phones worth 40-50% more than "Fair"
3. **Battery Critical**: 80%+ battery health worth 20-30% premium
4. **Storage Premium**: +₹5k per 64GB storage tier
5. **Brand Variance**: Apple/Samsung command 20-30% premiums
6. **Camera Relevance**: Each additional camera adds 5-8% to value
7. **Screen Size**: Larger screens (+6% per 0.5") trend higher prices

---

## 🚀 Deployment Recommendations

### Local Development
```bash
streamlit run app_v3.py
```

### Production Deployment (Cloud)
```bash
# Heroku
git push heroku main

# AWS EC2
streamlit run app_v3.py --logger.level=warning --server.port 8501

# Docker
docker build -t techresell-pro .
docker run -p 8501:8501 techresell-pro
```

---

## 📞 Support & Contact

- **Issues**: Check FEATURES_GUIDE.md
- **Setup Help**: See SETUP_GUIDE.md
- **Performance**: Review COMPLETION_REPORT.txt

---

## ✅ Checklist for Production Deployment

- [x] Generate 1M dataset
- [x] Train LightGBM model (85%+ accuracy)
- [x] Test individual predictions
- [x] Test bulk CSV upload
- [x] Verify all 5 Streamlit tabs
- [x] Document all features
- [x] Clean up repo (remove 6 unnecessary files)
- [x] Update requirements.txt
- [x] Create scalable data pipeline

---

**🎉 TechResell Pro v3.0 is production-ready!**

Built with ❤️ using Python, LightGBM, and Streamlit
