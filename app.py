from flask import Flask, render_template, request
import joblib
from datetime import datetime
import os

app = Flask(__name__)

# Load model from new location
model_path = os.path.join("models", "student_model.pkl")
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(f"✓ Model loaded from: {model_path}")
else:
    # Try old location as fallback
    if os.path.exists("student_model.pkl"):
        model = joblib.load("student_model.pkl")
        print("✓ Model loaded from: student_model.pkl")
    else:
        print("✗ Model not found!")
        model = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Check if model is loaded
        if model is None:
            return render_template(
                "index.html",
                error="Model not found. Please check if model file exists."
            )

        # ===========================
        # INPUTS
        # ===========================

        name = request.form.get("StudentName", "").strip()
        
        # Validate name
        if not name or len(name) < 2:
            return render_template(
                "index.html",
                error="❌ Please enter a valid student name (minimum 2 characters)."
            )
        
        # Get numeric values
        try:
            study = float(request.form.get("StudyHours", 0))
            attendance = float(request.form.get("Attendance", 0))
            previous = float(request.form.get("PreviousMarks", 0))
            sleep = float(request.form.get("SleepHours", 0))
            target_marks = float(request.form.get("TargetMarks", 0))
        except ValueError:
            return render_template(
                "index.html",
                error="❌ Please enter valid numbers for all fields."
            )
        
        # Validate ranges
        errors = []
        
        if study < 0 or study > 24:
            errors.append("📚 Study Hours must be between 0 and 24")
        
        if attendance < 0 or attendance > 100:
            errors.append("📊 Attendance must be between 0% and 100%")
        
        if previous < 0 or previous > 100:
            errors.append("📝 Previous Marks must be between 0 and 100")
        
        if sleep < 0 or sleep > 24:
            errors.append("😴 Sleep Hours must be between 0 and 24")
        
        if target_marks < 0 or target_marks > 100:
            errors.append("🎯 Target Marks must be between 0 and 100")
        
        # Additional logical validations
        if study + sleep > 24:
            errors.append("⚠️ Study Hours + Sleep Hours cannot exceed 24 hours in a day!")
        
        if errors:
            return render_template(
                "index.html",
                error="<br>".join(errors)
            )

        exam_date = request.form.get("ExamDate", "")

        today = datetime.today().date()
        
        try:
            exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
            days_remaining = (exam - today).days
        except:
            days_remaining = 0

        if days_remaining < 0:
            days_remaining = 0

        # ===========================
        # MODEL PREDICTION
        # ===========================

        prediction = model.predict(
            [[study, attendance, previous, sleep]]
        )[0]

        prediction = round(float(prediction), 2)
        prediction = max(0, min(100, prediction))

        # ===========================
        # GRADE
        # ===========================

        if prediction >= 90:
            grade = "A+"
            status = "Excellent Performance 🌟"
        elif prediction >= 80:
            grade = "A"
            status = "Very Good 👍"
        elif prediction >= 70:
            grade = "B"
            status = "Good 🙂"
        elif prediction >= 60:
            grade = "C"
            status = "Average"
        elif prediction >= 40:
            grade = "D"
            status = "Needs Improvement"
        else:
            grade = "F"
            status = "Fail"

        # ===========================
        # SMART TARGET PLANNER
        # ===========================

        gap = round(target_marks - prediction, 2)

        if gap <= 5:
            target_status = "🟢 Achievable"
            recommended_study = max(study, 5)
            planner_message = (
                "Your target is realistic. "
                "Stay consistent with your preparation."
            )
        elif gap <= 15 and days_remaining >= 20:
            target_status = "🟡 Challenging"
            recommended_study = max(study + 1.5, 6)
            planner_message = (
                "Your target is possible with extra effort "
                "and regular revision."
            )
        else:
            target_status = "🔴 Unrealistic"
            recommended_study = max(study + 2, 7)
            planner_message = (
                "Your target is difficult with the remaining time. "
                "Focus on improving your score step by step."
            )

        recommended_study = round(recommended_study, 1)

        # ===========================
        # PROGRESS BAR
        # ===========================

        if target_marks > 0:
            progress = min(100, round((prediction / target_marks) * 100))
        else:
            progress = 0

        # ===========================
        # SUGGESTIONS
        # ===========================

        suggestions = []

        if attendance < 75:
            suggestions.append("Improve your attendance above 75%.")

        if study < 5:
            suggestions.append("Increase your daily study hours.")

        if sleep < 6:
            suggestions.append("Sleep at least 6–8 hours for better concentration.")

        if previous < 60:
            suggestions.append("Focus on improving your fundamentals.")

        if prediction >= 90:
            suggestions.append("Excellent! Maintain your current performance.")
        elif prediction >= 80:
            suggestions.append("You are close to 90+. Keep practicing consistently.")
        elif prediction >= 70:
            suggestions.append("A little more effort can help you achieve an A grade.")
        else:
            suggestions.append("Regular study and better attendance can significantly improve your marks.")

        # ===========================
        # RENDER TEMPLATE
        # ===========================

        return render_template(
            "index.html",
            name=name,
            prediction=prediction,
            grade=grade,
            status=status,
            suggestions=suggestions,
            study=study,
            attendance=attendance,
            previous=previous,
            sleep=sleep,
            exam_date=exam_date,
            target_marks=target_marks,
            days_remaining=days_remaining,
            target_status=target_status,
            recommended_study=recommended_study,
            planner_message=planner_message,
            gap=gap,
            progress=progress
        )

    except Exception as e:
        print(f"Error in prediction: {e}")
        import traceback
        traceback.print_exc()
        return render_template(
            "index.html",
            error=f"An error occurred: {str(e)}"
        )


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Student Performance Prediction System - Original")
    print("="*60)
    if model is not None:
        print("✓ Model loaded successfully!")
    else:
        print("✗ Warning: Model not loaded!")
    print("Starting server at: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True)
