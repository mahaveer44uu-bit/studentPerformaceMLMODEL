# 🎓 AI-Based Student Performance Prediction System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

**An intelligent web application that predicts student academic performance using Machine Learning, with AI explainability, risk assessment, and personalized study planning.**

[Features](#-key-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Machine Learning](#-machine-learning)
- [Architecture](#-architecture)
- [Screenshots](#-screenshots)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🌟 Overview

The **AI-Based Student Performance Prediction System** is a comprehensive web application that uses machine learning to predict student academic performance based on multiple factors including study habits, attendance, health, stress levels, and engagement metrics.

### **What Makes This Different?**

- **16 Comprehensive Features** - Not just grades, but holistic student analysis
- **AI Explainability** - Understand *why* a prediction was made
- **Risk Assessment** - Early identification of at-risk students
- **Smart Study Planner** - Personalized daily and weekly study plans
- **Confidence Intervals** - Know how reliable predictions are
- **Production Ready** - Modular architecture, security, logging, API

---

## ✨ Key Features

### **🤖 Intelligent Prediction**
- Predicts final marks with **confidence intervals**
- **Pass probability** calculation
- **Grade classification** (A+ to F)
- **Risk level assessment** (Low/Moderate/High Risk)

### **🎯 AI Explainability**
- Feature importance analysis
- Natural language explanations
- Understanding prediction factors
- Transparent decision-making

### **📚 Smart Study Planning**
- **Daily study plans** with hour-by-hour breakdown
- **Weekly milestones** and targets
- **Subject priority** recommendations
- **Target feasibility** analysis (Achievable/Challenging/Unrealistic)
- Recommended study hours calculation

### **💡 Personalized Insights**
- Context-aware suggestions
- Stress management advice
- Sleep optimization tips
- Time management guidance
- Wellness recommendations
- Motivational feedback

### **🛡️ Security & Robustness**
- Input validation and sanitization
- XSS prevention
- Error handling with logging
- Rate limiting ready
- Environment-based configuration

### **🔌 API Access**
- RESTful API endpoints
- JSON input/output
- Health check endpoint
- Programmatic predictions

---

## 🛠️ Technology Stack

### **Backend**
- **Python 3.8+** - Core language
- **Flask 3.0** - Web framework
- **scikit-learn** - Machine learning
- **pandas & NumPy** - Data processing
- **joblib** - Model persistence

### **Machine Learning**
- Multiple algorithms (Random Forest, Decision Tree, Linear Regression)
- Cross-validation (5-fold)
- Hyperparameter tuning
- Feature engineering
- Model explainability (SHAP)

### **Frontend** (Planned)
- HTML5, CSS3, JavaScript
- Chart.js for visualizations
- Responsive design
- Glassmorphic UI

### **Optional Enhancements**
- **SHAP** - Advanced explainability
- **ReportLab** - PDF report generation
- **OpenPyXL** - Excel exports
- **Gunicorn** - Production WSGI server

---

## 📁 Project Structure

```
Student-Performance-Prediction/
│
├── app.py                          # Original application (preserved)
├── app_new.py                      # NEW: Enhanced application
├── config.py                       # Configuration management
├── requirements.txt                # Dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
│
├── models/                         # Trained ML models
│   ├── student_model.pkl          # Trained model
│   ├── model_metadata.json        # Model metrics & info
│   └── scaler.pkl                 # Feature scaler
│
├── dataset/                        # Datasets
│   └── dataset.csv                # Training data (2000 samples, 16 features)
│
├── training/                       # Model training scripts
│   ├── train_model.py             # Original training script
│   ├── generate_dataset.py        # Original dataset generator
│   ├── generate_enhanced_dataset.py  # NEW: 16-feature generator
│   └── train_enhanced_model.py    # NEW: Advanced training pipeline
│
├── utils/                          # Business logic modules
│   ├── __init__.py                # Package initialization
│   ├── grading.py                 # Grade calculation & risk assessment
│   ├── planner.py                 # Study planning system
│   ├── prediction.py              # ML prediction engine
│   ├── validation.py              # Input validation
│   └── suggestions.py             # Personalized suggestions
│
├── templates/                      # HTML templates
│   └── index.html                 # Main UI
│
├── static/                         # Static assets
│   ├── css/                       # Stylesheets
│   ├── js/                        # JavaScript
│   └── images/                    # Images & icons
│
├── logs/                           # Application logs
├── exports/                        # PDF/Excel exports
│
└── docs/                           # Documentation
    ├── PROJECT_UPGRADE_SUMMARY.md  # Upgrade details
    ├── QUICK_START.md              # Quick start guide
    └── API_DOCUMENTATION.md        # API docs
```

---

## 🚀 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/student-performance-prediction.git
cd student-performance-prediction
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Generate Dataset (Optional)**
```bash
python training/generate_enhanced_dataset.py
```

### **Step 5: Train Model (Optional)**
```bash
python training/train_model.py
```

---

## 💻 Usage

### **Option 1: Run Original Application**
```bash
python app.py
```
- 4 features
- Basic functionality
- Visit: `http://localhost:5000`

### **Option 2: Run Enhanced Application**
```bash
python app_new.py
```
- 16 features
- AI explainability
- Risk assessment
- Advanced planning
- Visit: `http://localhost:5000`

### **Using the Application**

1. **Enter Student Information:**
   - Student name
   - Study hours per day
   - Attendance percentage
   - Previous marks
   - Sleep hours
   - (+ 12 more features in enhanced version)

2. **Set Exam Details:**
   - Exam date
   - Target marks

3. **Get Predictions:**
   - Predicted final marks
   - Grade & performance status
   - Pass probability
   - Risk level

4. **View Insights:**
   - AI explanation of prediction
   - Personalized suggestions
   - Daily & weekly study plans
   - Recommended study hours

---

## 🔌 API Documentation

### **Endpoint: `/api/predict`**

**Method:** POST

**Request Body:**
```json
{
  "StudentName": "John Doe",
  "StudyHours": 6.5,
  "Attendance": 85.0,
  "PreviousMarks": 75.0,
  "SleepHours": 7.0,
  "StressLevel": 5,
  "InternetUsage": 4.0,
  "AssignmentCompletion": 80.0,
  "ClassParticipation": 7,
  "PreviousSemesterGPA": 7.5,
  "InternalMarks": 72.0,
  "FamilySupport": 8,
  "HealthScore": 7,
  "ExamPrepDays": 20,
  "DistractionHours": 3.0,
  "MockTestScore": 70.0,
  "ExtracurricularActivity": 5,
  "ExamDate": "2026-09-01",
  "TargetMarks": 85
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 78.5,
  "confidence": 82.3,
  "grade": "B",
  "status": "Good",
  "risk_level": "Low Risk",
  "pass_probability": 92.5
}
```

### **Endpoint: `/health`**

**Method:** GET

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-07-24T12:34:56",
  "model_loaded": true
}
```

---

## 🤖 Machine Learning

### **Features (16 Total)**

| Category | Features |
|----------|----------|
| **Study Habits** | Study Hours, Exam Prep Days, Assignment Completion |
| **Engagement** | Attendance, Class Participation |
| **Academic History** | Previous Marks, Internal Marks, Mock Test Score, Previous Semester GPA |
| **Wellness** | Sleep Hours, Stress Level, Health Score |
| **Environment** | Family Support, Internet Usage, Distraction Hours |
| **Balance** | Extracurricular Activity |

### **Models Compared**
1. **Linear Regression** - Baseline
2. **Decision Tree** - Non-linear patterns
3. **Random Forest** - Ensemble method (usually best)

### **Training Process**
1. Data generation with realistic correlations
2. Train-test split (80-20)
3. Cross-validation (5-fold)
4. Hyperparameter tuning
5. Model comparison
6. Best model selection
7. Metrics calculation (R², MAE, RMSE)

### **Performance Metrics**
- **R² Score**: ~0.82 (82% variance explained)
- **MAE**: ~4.5 marks
- **RMSE**: ~6.2 marks

---

## 🏗️ Architecture

### **Design Principles**
- **Separation of Concerns** - Business logic in utilities
- **Modularity** - Each module has single responsibility
- **Scalability** - Easy to add new features
- **Testability** - Each component can be tested independently
- **Security** - Input validation, sanitization, logging

### **Module Breakdown**

#### **Configuration Layer** (`config.py`)
- Environment-based settings
- Feature definitions
- Validation ranges
- Thresholds

#### **Utility Layer** (`utils/`)
- **Grading** - Grade calculation, risk assessment
- **Planner** - Study planning logic
- **Prediction** - ML model interface
- **Validation** - Input validation
- **Suggestions** - Personalized advice generation

#### **Application Layer** (`app_new.py`)
- Route definitions
- Request handling
- Response formatting
- Error handling

#### **Presentation Layer** (`templates/`)
- HTML templates
- User interface
- Form inputs
- Results display

---

## 📸 Screenshots

*Coming soon - Screenshots will be added after frontend enhancement*

---

## 🌐 Deployment

### **Local Development**
```bash
python app_new.py
```

### **Production (Gunicorn)**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_new:app
```

### **Docker** (Coming soon)
```bash
docker build -t student-prediction .
docker run -p 5000:5000 student-prediction
```

### **Cloud Platforms**

#### **Render.com**
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app_new:app`

#### **Railway.app**
1. Connect GitHub repository
2. Auto-detects Python
3. Auto-deploys on push

#### **PythonAnywhere**
1. Upload project files
2. Create virtual environment
3. Configure WSGI file

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### **Development Guidelines**
- Follow PEP 8 style guide
- Add docstrings to functions
- Write unit tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact

**Project Team** - AI-Based Student Performance Prediction

- **GitHub**: [Your GitHub Profile]
- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn Profile]

---

## 🙏 Acknowledgments

- scikit-learn for ML framework
- Flask for web framework
- Bootstrap for UI components (if used)
- Chart.js for visualizations (planned)
- Open source community

---

## 📊 Project Stats

- **Version**: 2.0
- **Python**: 3.8+
- **Features**: 16
- **Dataset Size**: 2000 samples
- **Model Accuracy**: ~82% R²
- **Files**: 20+ organized modules
- **Lines of Code**: 3000+

---

## 🎓 Use Cases

### **For Educational Institutions**
- Early warning system for at-risk students
- Data-driven intervention strategies
- Academic counseling support
- Progress monitoring

### **For Students**
- Self-assessment tool
- Study planning assistance
- Performance prediction
- Goal setting

### **For Researchers**
- Academic performance analysis
- Feature importance studies
- ML model comparison
- Educational data mining

---

## 🔮 Future Enhancements

- [ ] Interactive data visualizations
- [ ] Student dashboard with history
- [ ] Multi-user system with authentication
- [ ] Comparison with peer performance
- [ ] Mobile app version
- [ ] Real-time notifications
- [ ] Integration with LMS
- [ ] Advanced SHAP visualizations

---

<div align="center">

**Made with ❤️ for better education**

⭐ Star this repo if you find it helpful!

</div>
#   s t u d e n t P e r f o r m a c e M L M O D E L  
 #   s t u d e n t P e r f o r m a c e M L M O D E L  
 