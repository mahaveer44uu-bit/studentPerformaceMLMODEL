"""
Student Performance Prediction System - Simple Version
=======================================================
Works with the existing 4-feature model while using new utility modules.

This is a bridge version that demonstrates the new architecture
while being compatible with your existing trained model.

Author: AI-Based Student Performance Prediction Team
Version: 2.0-simple
"""

from flask import Flask, render_template, request
import os
import logging

# Import configuration
from config import get_config

# Import utilities
from utils import (
    GradingSystem,
    StudyPlanner,
    PredictionEngine,
    InputValidator,
    SuggestionsGenerator
)

# ============================================================
# APPLICATION INITIALIZATION
# ============================================================

env = os.getenv('FLASK_ENV', 'development')
config_class = get_config(env)

app = Flask(__name__)
app.config.from_object(config_class)

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

os.makedirs(app.config['LOG_DIR'], exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(app.config['LOG_FILE']),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"Simple application started in {env} mode")

# ============================================================
# INITIALIZE UTILITY SYSTEMS
# ============================================================

try:
    grading_system = GradingSystem(
        grade_boundaries=app.config['GRADE_BOUNDARIES'],
        performance_status=app.config['PERFORMANCE_STATUS']
    )
    
    study_planner = StudyPlanner(config=app.config)
    
    prediction_engine = PredictionEngine(
        model_path=app.config['MODEL_PATH'],
        metadata_path=app.config.get('MODEL_METADATA_PATH'),
        scaler_path=app.config.get('SCALER_PATH')
    )
    
    input_validator = InputValidator(
        validation_ranges=app.config['VALIDATION_RANGES']
    )
    
    suggestions_generator = SuggestionsGenerator(config=app.config)
    
    logger.info("All systems initialized successfully!")

except Exception as e:
    logger.error(f"Error initializing systems: {e}")
    raise


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    """Render home page."""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return "Internal Server Error", 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle prediction request.
    
    This version works with 4 features (compatible with existing model):
    - StudyHours
    - Attendance
    - PreviousMarks
    - SleepHours
    """
    
    try:
        logger.info("Processing prediction request")
        
        # ===========================
        # 1. EXTRACT BASIC DATA
        # ===========================
        
        student_name = request.form.get("StudentName", "").strip()
        exam_date = request.form.get("ExamDate", "")
        
        try:
            target_marks = float(request.form.get("TargetMarks", 0))
        except:
            target_marks = 75.0
        
        # ===========================
        # 2. EXTRACT 4 CORE FEATURES
        # ===========================
        
        try:
            study_hours = float(request.form.get("StudyHours", 0))
            attendance = float(request.form.get("Attendance", 0))
            previous_marks = float(request.form.get("PreviousMarks", 0))
            sleep_hours = float(request.form.get("SleepHours", 0))
        except Exception as e:
            logger.error(f"Invalid numeric input: {e}")
            return render_template(
                "index.html",
                errors=["Please enter valid numbers for all fields"],
                form_data=request.form
            )
        
        # Create feature vector for model (4 features)
        features = [study_hours, attendance, previous_marks, sleep_hours]
        
        # Create feature dict for suggestions
        feature_dict = {
            'StudyHours': study_hours,
            'Attendance': attendance,
            'PreviousMarks': previous_marks,
            'SleepHours': sleep_hours
        }
        
        logger.info(f"Prediction for: {student_name}")
        
        # ===========================
        # 3. MAKE PREDICTION
        # ===========================
        
        try:
            predicted_marks = prediction_engine.predict(features)
            
            # For models without metadata, use default confidence
            confidence = 80.0
            lower_bound = max(0, predicted_marks - 5)
            upper_bound = min(100, predicted_marks + 5)
            
            logger.info(f"Prediction: {predicted_marks}")
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return render_template(
                "index.html",
                errors=["Prediction model error. Please try again."],
                form_data=request.form
            )
        
        # ===========================
        # 4. GENERATE GRADE & STATUS
        # ===========================
        
        grade, status = grading_system.calculate_grade_and_status(predicted_marks)
        pass_probability = grading_system.calculate_pass_probability(predicted_marks)
        risk_assessment = grading_system.assess_risk_level(predicted_marks)
        
        # ===========================
        # 5. GENERATE STUDY PLAN
        # ===========================
        
        comprehensive_plan = study_planner.generate_comprehensive_plan(
            predicted_marks=predicted_marks,
            target_marks=target_marks,
            current_study=study_hours,
            exam_date=exam_date,
            sleep_hours=sleep_hours
        )
        
        # ===========================
        # 6. GENERATE SUGGESTIONS
        # ===========================
        
        suggestions = suggestions_generator.generate_suggestions(
            student_data=feature_dict,
            predicted_marks=predicted_marks
        )
        
        motivational_message = suggestions_generator.generate_motivational_message(
            predicted_marks=predicted_marks,
            target_marks=target_marks
        )
        
        # ===========================
        # 7. PREPARE RESPONSE
        # ===========================
        
        response_data = {
            'name': student_name,
            'prediction': predicted_marks,
            'confidence': confidence,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'grade': grade,
            'status': status,
            'pass_probability': pass_probability,
            'risk_assessment': risk_assessment,
            'days_remaining': comprehensive_plan['days_remaining'],
            'target_status': comprehensive_plan['target_feasibility']['status'],
            'target_status_class': comprehensive_plan['target_feasibility']['status_class'],
            'gap': comprehensive_plan['target_feasibility']['gap'],
            'recommended_study': comprehensive_plan['recommended_study_hours'],
            'planner_message': comprehensive_plan['planner_message'],
            'progress': comprehensive_plan['progress_percentage'],
            'daily_plan': comprehensive_plan['daily_plan'],
            'weekly_plan': comprehensive_plan['weekly_plan'],
            'suggestions': suggestions,
            'motivational_message': motivational_message,
            'exam_date': exam_date,
            'target_marks': target_marks,
            'study': study_hours,
            'attendance': attendance,
            'previous': previous_marks,
            'sleep': sleep_hours
        }
        
        logger.info("Prediction completed successfully")
        
        return render_template("index.html", **response_data)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return render_template(
            "index.html",
            errors=["An unexpected error occurred. Please try again."],
            form_data=request.form
        )


@app.route("/health")
def health_check():
    """Health check endpoint."""
    from flask import jsonify
    from datetime import datetime
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': prediction_engine.model is not None,
        'version': '2.0-simple'
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("index.html", errors=["Page not found"]), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {error}")
    return render_template("index.html", errors=["Internal server error"]), 500


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Student Performance Prediction System - Simple Version")
    print("=" * 60)
    print("\nUsing 4-feature model (compatible with existing model)")
    print("Enhanced with new utility modules!")
    print("\nServer starting at: http://localhost:5000")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
