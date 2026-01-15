# 📱 TechResell Pro - AI Phone Resale Valuation System

An intelligent web application that predicts fair market prices for used smartphones using machine learning.

## 🎯 Project Overview

TechResell Pro helps buyers and sellers determine accurate resale prices for used phones by analyzing multiple factors including:
- **Device Brand & Model** - Premium brands hold value better
- **Storage Capacity** - More storage = higher value
- **Physical Condition** - Excellent vs. Fair condition impacts price
- **Device Age** - Time degrades value progressively
- **Battery Health** - Critical factor for used phone valuation

## ✨ Key Features

### 🚀 New Improvements (v2.0)
- **Advanced ML Model**: Upgraded from Random Forest to Gradient Boosting Regressor
  - 99.1% training accuracy
  - 83% testing accuracy  
  - Mean Absolute Error: ₹4,036
  
- **Enhanced Data Features**:
  - 2000 training samples (2x previous)
  - 29 phone brands (vs 20 previously)
  - Age-based depreciation modeling
  - Battery health consideration
  - Realistic price ranges: ₹3,000 - ₹87,000

- **Improved UI/UX**:
  - 4-factor input (added age & battery health)
  - Real-time market insights
  - Value retention percentage display
  - Detailed price factor breakdown
  - Export valuation reports as CSV
  - Better recommendations engine

- **Better Error Handling**:
  - Input validation
  - Try-catch exception handling
  - User-friendly error messages

## 📊 Model Performance

```
Training R² Score: 0.9910
Testing R² Score:  0.8302
Mean Absolute Error: ₹4,036
RMSE: ₹5,520
```

The model explains 83% of price variance in unseen data, ensuring reliable predictions.

## 🛠️ Project Structure

```
PhonePricePredictor/
├── app.py                    # Streamlit web interface
├── train_model.py            # ML model training pipeline
├── generate_data.py          # Synthetic dataset generation
├── requirements.txt          # Python dependencies
├── phones.csv               # Generated training data
├── price_predictor_model.pkl # Trained model (serialized)
├── le_brand.pkl             # Brand label encoder
├── le_condition.pkl         # Condition label encoder
└── phone_mrp_db.pkl         # Master phone database with MRPs
```

## 🚀 Getting Started

### Installation

1. Clone/download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate training data:
```bash
python generate_data.py
```

4. Train the model:
```bash
python train_model.py
```

5. Launch the web app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📱 How to Use

1. **Select Phone Model** - Choose from 29+ available brands
2. **Set Storage** - Select 64GB, 128GB, 256GB, or 512GB
3. **Rate Condition** - Fair, Good, Excellent, or Like New
4. **Adjust Age** - Use slider to set device age in months (1-48)
5. **Input Battery Health** - Current battery capacity percentage (20-100%)
6. **Calculate** - Click "Calculate Value" button
7. **Review Results** - See price estimate, savings, and recommendations
8. **Export Report** - Download valuation as CSV file

## 🎨 Features in Detail

### Price Valuation
- Base depreciation: 35-65% of new price
- Age factor: Progressive degradation over 10 years
- Condition multiplier: Fair (-15%), Good (-5%), Excellent (+5%), Like New (+10%)
- Battery factor: Affects 20% of final price
- Storage bonus: +₹50K per 64GB increase

### Market Insights
- Storage capacity impact analysis
- Device age considerations
- Battery health warnings
- Value retention metrics
- Competitive recommendations

### Data Export
- CSV format reports
- One-click download
- Complete valuation breakdown

## 🤖 Machine Learning Details

### Algorithm: Gradient Boosting Regressor
- **n_estimators**: 200
- **learning_rate**: 0.1
- **max_depth**: 6
- **Purpose**: Superior performance on structured financial data

### Features Used
- Brand (encoded categorical)
- Storage capacity (GB)
- Condition (encoded categorical)
- Device age (months)
- Battery health (%)

### Data Split
- Training: 80% (1600 samples)
- Testing: 20% (400 samples)
- Validation: R² score on test set

## 📈 Phone Database (29 Brands)

**Premium**: iPhone 11/12/13/14/15/Pro, Google Pixel 6/7/8/Pro  
**Mid-Range**: Samsung S20/S21/S22/S23/S24/Ultra, OnePlus 9/10/11/12  
**Budget**: Xiaomi, Redmi Note, Realme, Vivo, Motorola

MRP ranges: ₹15,000 - ₹130,000

## 🔧 Configuration

To add new phones, edit `generate_data.py`:

```python
PHONE_DB = {
    'Your Phone': 50000,  # Add as 'Brand Model': MRP
    # ...
}
```

Then regenerate data and retrain model.

## 📊 Example Predictions

| Phone | Storage | Age | Battery | Condition | Predicted Price |
|-------|---------|-----|---------|-----------|-----------------|
| iPhone 15 | 256GB | 6mo | 95% | Like New | ₹68,500 |
| Samsung S23 | 128GB | 12mo | 85% | Excellent | ₹45,200 |
| Redmi Note 13 | 64GB | 24mo | 75% | Good | ₹14,800 |

## 🎯 Future Enhancements

- [ ] Real-time market data integration
- [ ] User authentication & history
- [ ] Bulk valuation API
- [ ] Market trend predictions
- [ ] Comparison with actual listings
- [ ] Trade-in value calculator
- [ ] Mobile app version
- [ ] International market support

## 📝 License

This project is open source and available for educational and commercial use.

## 👨‍💻 Author

Created with ❤️ for the used phone market

---

**Version**: 2.0  
**Last Updated**: January 2026  
**Model Accuracy**: 83% (R² Score)
