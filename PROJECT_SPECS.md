# 📊 PROJECT SPECIFICATIONS
## Student Performance Prediction System

**Last Updated:** January 30, 2026

---

## 🎯 PROJECT OVERVIEW

**Project Name:** AI-Based Student Performance Prediction System  
**Type:** Machine Learning Web Application  
**Purpose:** Predict student final exam marks based on academic and lifestyle factors

---

## 🤖 MACHINE LEARNING MODEL

### Current Model (Production)
- **Algorithm:** Gradient Boosting Regressor
- **Library:** scikit-learn 1.4.2
- **Model File:** `models/student_model.pkl`

### Performance Metrics
- **Test R² Score:** 80.82%
- **Train R² Score:** 78.35%
- **Mean Absolute Error (Test):** 3.91 marks
- **Root Mean Square Error (Test):** 4.99 marks
- **Overfitting Gap:** 2.47% (Low overfitting)

### Training Details
- **Dataset Size:** 5000 student records
- **Training Set:** 4000 records (80%)
- **Test Set:** 1000 records (20%)
- **Random State:** 42 (reproducible results)
- **Cross-Validation:** Applied during hyperparameter tuning

---

## 📊 DATASET INFORMATION

### Size
- **Total Records:** 5000 rows
- **File:** `dataset.csv`
- **Format:** CSV (Comma Separated Values)

### Features (4 Input Variables)
1. **StudyHours** - Daily study hours (0-24)
2. **Attendance** - Attendance percentage (0-100%)
3. **PreviousMarks** - Previous exam marks (0-100)
4. **SleepHours** - Daily sleep hours (0-24)

### Target Variable
- **FinalMarks** - Predicted final exam marks (0-100 scale)

### Data Characteristics
- Realistic correlations between features
- Normal distribution patterns
- No missing values
- Balanced representation across performance levels

---

## 💻 TECHNOLOGY STACK

### Backend
- **Python:** 3.x
- **Flask:** 2.2.5 (Web framework)
- **Werkzeug:** 2.2.3 (WSGI utility)
- **Gunicorn:** 20.1.0 (Production server)

### Machine Learning & Data Science
- **scikit-learn:** 1.4.2 (ML algorithms)
- **NumPy:** 1.26.4 (Numerical computing)
- **Pandas:** Latest (Data manipulation)
- **Joblib:** 1.3.2 (Model serialization)

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Glass morphism design)
- **JavaScript** - Interactivity
- **Google Fonts (Inter)** - Typography

### Development Tools
- **Git/GitHub** - Version control
- **VS Code** - Development environment

---

## 🌐 APPLICATION FEATURES

### 1. AI-Powered Prediction
- Real-time performance prediction
- 80.82% accuracy
- Predictions within ±4 marks range

### 2. Smart Target Planner
- Gap analysis between target and predicted marks
- Achievability assessment (Achievable/Challenging/Unrealistic)
- Recommended study hours calculation
- Days remaining tracker

### 3. Input Validation
- Range checking for all inputs
- Logical validation (Study + Sleep ≤ 24 hours)
- Date validation (future dates only, within 1 year)
- Professional error messages

### 4. Personalized Suggestions
- Attendance-based recommendations
- Study hour optimization
- Sleep improvement advice
- Grade-specific guidance

### 5. Grade Classification
- A+ (90-100): Excellent Performance
- A (80-89): Very Good
- B (70-79): Good
- C (60-69): Average
- D (40-59): Needs Improvement
- F (0-39): Fail

---

## 📁 PROJECT STRUCTURE

```
Student-Performance-Prediction/
│
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for deployment
├── Procfile                        # Deployment configuration
│
├── models/
│   ├── student_model.pkl           # Trained Gradient Boosting model
│   ├── model_metadata.json         # Model performance metrics
│   └── model_info.json             # Model information
│
├── templates/
│   ├── home.html                   # Landing page
│   ├── index.html                  # Prediction form & results
│   ├── prediction_new.html         # Alternative prediction page
│   ├── about.html                  # Model information page
│   └── contact.html                # Contact page
│
├── dataset.csv                     # Training dataset (5000 rows)
├── generate_dataset.py             # Dataset generation script
│
├── logs/
│   └── app.log                     # Application logs
│
├── exports/                        # Export directory (empty)
│
└── PPT_COMPLETE_CONTENT.md         # Presentation content
```

---

## ✅ VALIDATION RULES

### Input Constraints
- **Study Hours:** 0-24 hours/day
- **Attendance:** 0-100%
- **Previous Marks:** 0-100
- **Sleep Hours:** 0-24 hours/day
- **Exam Date:** Future date, within 365 days
- **Target Marks:** 0-100

### Logical Validations
- Study Hours + Sleep Hours ≤ 24 (daily constraint)
- Exam date cannot be in the past
- All numeric fields must be within valid ranges
- Student name minimum 2 characters

---

## 🚀 DEPLOYMENT

### Production
- **Platform:** Render / Railway / Heroku
- **Server:** Gunicorn WSGI server
- **Environment:** Production mode (DEBUG=False)

### Local Development
```bash
python app.py
# Access: http://localhost:5000
```

---

## 👥 PROJECT INFORMATION

**Developer:** Mahaveer Meghwal  
**Roll No:** 24ESKCY027  
**Institution:** SKIT, Jaipur  
**Internship:** InternPe (AI/ML Domain)  
**Duration:** 18 May 2026 - 01 July 2026

---

## 📈 MODEL COMPARISON

| Algorithm | R² Score | Status |
|-----------|----------|--------|
| Linear Regression | 75.34% | Old/Replaced |
| **Gradient Boosting** | **80.82%** | **Current/Active** |

**Improvement:** +5.48% accuracy gained by upgrading to Gradient Boosting

---

## 🔄 VERSION HISTORY

### Version 2.0 (Current)
- ✅ Upgraded to Gradient Boosting Regressor
- ✅ Improved accuracy to 80.82%
- ✅ Expanded dataset to 5000 records
- ✅ Enhanced UI/UX with glass morphism
- ✅ Multi-page application structure
- ✅ Comprehensive validation system

### Version 1.0 (Legacy)
- Linear Regression model
- 75.34% accuracy
- 1000 records dataset
- Basic single-page interface

---

## 📝 NOTES

- All accuracy values are based on test set (unseen data)
- Model trained with cross-validation
- Low overfitting ensures good generalization
- Production-ready code with proper error handling
- Responsive design for mobile and desktop

---

**Document Version:** 1.0  
**Last Verified:** January 30, 2026  
**Status:** ✅ Production Ready
