# TechResell Pro - Quick Start Guide

## 🚀 One-Time Setup (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Training Data
```bash
python generate_data.py
```
Creates 2000 realistic phone pricing samples from 29 brands.

**Output:**
- `phones.csv` - Training dataset
- `phone_mrp_db.pkl` - Phone MRP database

### Step 3: Train the ML Model
```bash
python train_model.py
```
Trains Gradient Boosting model on the generated data.

**Output:**
```
✅ Model Performance:
   Training R² Score: 0.9910
   Testing R² Score: 0.8302
   Mean Absolute Error: ₹4,036
   RMSE: ₹5,520
```

**Files created:**
- `price_predictor_model.pkl` - Trained model
- `le_brand.pkl` - Brand label encoder
- `le_condition.pkl` - Condition label encoder

### Step 4: Launch the Web App
```bash
streamlit run app.py
```

Open browser to `http://localhost:8501` 🎉

---

## 📱 Using the App

1. **Select Phone Model** from dropdown (29 brands available)
2. **Choose Storage**: 64GB, 128GB, 256GB, or 512GB
3. **Rate Condition**: Fair → Good → Excellent → Like New
4. **Set Device Age**: 1-48 months using slider
5. **Input Battery Health**: 20-100% capacity
6. **Click "Calculate Value"** button
7. **View Results**:
   - Original retail price
   - Estimated used value
   - Your savings amount
   - Value retention percentage
   - Market insights & recommendations
   - Option to export report as CSV

---

## 🔍 Run Market Analytics

View detailed insights on phone depreciation, condition impact, storage premiums, and more:

```bash
python analytics.py
```

**Reports generated:**
- Brand depreciation rankings
- Condition impact on pricing
- Storage capacity premium analysis
- Age-based depreciation curves
- Battery health correlation

---

## 📊 Model Architecture

```
Input Features (5)
    ↓
[Brand | Storage | Condition | Age | Battery]
    ↓
Gradient Boosting Regressor (200 trees)
    ↓
Price Prediction Output
```

**Performance Metrics:**
- R² Score (Test): 0.8302 (83% variance explained)
- MAE: ₹4,036
- RMSE: ₹5,520

---

## 🛠️ Customization

### Add New Phone Brands

Edit `generate_data.py`:
```python
PHONE_DB = {
    'iPhone 15': 80000,
    'Samsung S24': 80000,
    'Your Brand': 50000,  # Add here
}
```

Then regenerate and retrain:
```bash
python generate_data.py
python train_model.py
```

### Adjust Model Parameters

Edit `train_model.py`:
```python
model = GradientBoostingRegressor(
    n_estimators=200,      # Number of trees
    learning_rate=0.1,     # Learning rate
    max_depth=6,          # Tree depth
    # ... more params
)
```

---

## 📂 Project Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI (main app) |
| `train_model.py` | ML model training |
| `generate_data.py` | Dataset generation |
| `analytics.py` | Market insights analysis |
| `phones.csv` | Training data (generated) |
| `*.pkl` | Serialized models & encoders |

---

## 🐛 Troubleshooting

**Issue**: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

**Issue**: "File not found" (.pkl files)
```bash
python generate_data.py
python train_model.py
```

**Issue**: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

**Issue**: Model predictions seem off
```bash
# Regenerate data with new distribution
python generate_data.py
python train_model.py
```

---

## 📈 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Training R² | 0.9910 |
| Testing R² | 0.8302 |
| MAE | ₹4,036 |
| RMSE | ₹5,520 |
| Brands | 29 |
| Samples | 2000 |
| Avg Price | ₹23,977 |

---

## 🎯 Next Steps

1. ✅ Complete setup (follow steps above)
2. 📊 Run analytics to understand market
3. 🚀 Launch web app
4. 💬 Get valuations for your phones
5. 📥 Export reports for records
6. 🔄 Fine-tune model as needed

---

## 💡 Tips

- Use **Like New** condition sparingly - reserved for barely-used devices
- **Battery health** significantly impacts value after 12+ months
- **Age matters** - factor in 2-3% monthly depreciation
- **Storage** adds ₹2.7K-₹7.6K value depending on tier
- **Compare brands** - premium brands hold value better

---

## 📞 Support

For issues or improvements, check:
- Model accuracy: Run `train_model.py` to see R² score
- Data quality: Run `analytics.py` for market insights
- Feature requests: Enhance in relevant .py files

---

**Version**: 2.0  
**Last Updated**: January 2026  
**Status**: ✅ Production Ready
