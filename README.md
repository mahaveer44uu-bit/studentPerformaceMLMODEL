# 🎓 Student Performance Prediction System

AI-Powered academic performance prediction using Machine Learning.

## 🚀 Features

- **AI Prediction Engine** - Linear Regression model trained on 5000+ student records
- **Smart Target Planner** - Personalized study recommendations with feasibility analysis
- **Performance Analytics** - Grade prediction with detailed insights
- **Input Validation** - Two-layer validation (client + server side)
- **Multi-page Interface** - Clean, professional web application

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **ML:** Scikit-learn, NumPy, Pandas
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Render (Free tier)

## 📊 Model Information

- **Algorithm:** Linear Regression
- **Training Data:** 5000 student records
- **Accuracy:** ~75% R²
- **Features:** Study Hours, Attendance, Previous Marks, Sleep Hours

## 🌐 Live Demo

**Deployed on Render:** [Add your URL here after deployment]

## 💻 Local Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/student-performance-prediction.git

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Open browser
http://localhost:5000
```

## 📁 Project Structure

```
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── models/
│   └── student_model.pkl       # Trained ML model
├── templates/
│   ├── home.html              # Landing page
│   ├── prediction.html        # Prediction page
│   ├── about.html             # Model information
│   └── contact.html           # Contact page
├── dataset.csv                # Training dataset (5000 rows)
└── train_model.py             # Model training script
```

## 🎯 Input Features

1. **Student Name** (2+ characters)
2. **Study Hours** (0.5-15 hrs/day)
3. **Attendance** (45-100%)
4. **Previous Marks** (30-100)
5. **Sleep Hours** (3-10 hrs/day)
6. **Exam Date** (Future date, within 1 year)
7. **Target Marks** (0-100)

## ✅ Validation Rules

- Study + Sleep ≤ 24 hours
- Attendance ≥ 45% (educational threshold)
- Past dates blocked
- All fields required with proper ranges

## 👨‍💻 Developer

**Mahaveer Meghwal**
- Email: mahaveer44uu@gmail.com
- GitHub: [mahaveer44uu-bit](https://github.com/mahaveer44uu-bit)
- LinkedIn: [mahaveer-verma-04303b379](https://www.linkedin.com/in/mahaveer-verma-04303b379)

## 📄 License

This is an academic project for educational purposes.

## 🙏 Acknowledgments

- Scikit-learn for ML algorithms
- Flask for web framework
- Render for free hosting

---

**Built with ❤️ for academic excellence**
