"""
Student Performance Prediction System - Main Application
==========================================================
Flask web application for AI-based student performance prediction.

This refactored application uses modular utilities for better code
organization, maintainability, and scalability.

Author: AI-Based Student Performance Prediction Team
Version: 2.0
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import logging
from datetime import datetime

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

# Get configuration based on environment
env = os.getenv('FLASK_ENV', 'development')
config_class = get_config(env)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config_class)

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

# Create logs directory if it doesn't exist
os.makedirs(app.config['LOG_DIR'], exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format=app.config['LOG_FORMAT'],
    handlers=[
        logging.FileHandler(app.config['LOG_FILE']),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"Application started in {env} mode")

# ============================================================
# INITIALIZE UTILITY SYSTEMS
# ============================================================

try:
    # Initialize grading system
    grading_system = GradingSystem(
        grade_boundaries=app.config['GRADE_BOUNDARIES'],
        performance_status=app.config['PERFORMANCE_STATUS']
    )
    logger.info("✓ Grading system initialized")
    
    # Initialize study planner
    study_planner = StudyPlanner(config=app.config)
    logger.info("✓ Study planner initialized")
    
    # Initialize prediction engine
    prediction_engine = PredictionEngine(
        model_path=app.config['MODEL_PATH'],
        metadata_path=app.config['MODEL_METADATA_PATH'],
        scaler_path=app.config['SCALER_PATH']
    )
    logger.info("✓ Prediction engine initialized")
    
    # Initialize input validator
    input_validator = InputValidator(
        validation_ranges=app.config['VALIDATION_RANGES']
    )
    logger.info("✓ Input validator initialized")
    
    # Initialize suggestions generator
    suggestions_generator = SuggestionsGenerator(config=app.config)
    logger.info("✓ Suggestions generator initialized")
    
    logger.info("=" * 60)
    logger.info("All systems initialized successfully!")
    logger.info("=" * 60)

except Exception as e:
    logger.error(f"✗ Error initializing systems: {e}")
    raise


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    """Render home page with prediction form."""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return "Internal Server Error", 500


@app.route("/predict", methods=["POST"])
def predict():
    """Handle prediction request and generate comprehensive results."""
    
    try:
        # ===========================
        # 1. INPUT VALIDATION
        # ===========================
        
        logger.info("Processing prediction request")
        
        # Validate all inputs
        is_valid, sanitized_data = input_validator.validate_all_inputs(request.form)
        
        if not is_valid:
            errors = input_validator.get_errors()
            logger.warning(f"Validation failed: {errors}")
            
            # Return to form with error messages
            return render_template(
                "index.html",
                errors=errors,
                form_data=request.form
            )
        
        logger.info("✓ Input validation passed")
        
        # ===========================
        # 2. EXTRACT VALIDATED DATA
        # ===========================
        
        student_name = sanitized_data['StudentName']
        exam_date = sanitized_data['ExamDate']
        target_marks = sanitized_data['TargetMarks']
        
        # Extract all features
        features = []
        feature_dict = {}
        
        for feature_name in app.config['FEATURE_COLUMNS']:
            value = sanitized_data.get(feature_name, 0)
            features.append(value)
            feature_dict[feature_name] = value
        
        logger.info(f"Prediction for student: {student_name}")
        
        # ===========================
        # 3. MAKE PREDICTION
        # ===========================
        
        try:
            # Get prediction with confidence
            prediction_result = prediction_engine.predict_with_confidence(features)
            predicted_marks = prediction_result['prediction']
            confidence = prediction_result['confidence']
            lower_bound = prediction_result['lower_bound']
            upper_bound = prediction_result['upper_bound']
            
            logger.info(f"✓ Prediction: {predicted_marks} (confidence: {confidence}%)")
            
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
        
        logger.info(f"✓ Grade: {grade}, Status: {status}")
        
        # ===========================
        # 5. GENERATE STUDY PLAN
        # ===========================
        
        comprehensive_plan = study_planner.generate_comprehensive_plan(
            predicted_marks=predicted_marks,
            target_marks=target_marks,
            current_study=feature_dict.get('StudyHours', 5),
            exam_date=exam_date,
            sleep_hours=feature_dict.get('SleepHours', 7)
        )
        
        logger.info("✓ Study plan generated")
        
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
        
        logger.info(f"✓ Generated {len(suggestions)} suggestions")
        
        # ===========================
        # 7. GENERATE EXPLANATION
        # ===========================
        
        explanation = prediction_engine.explain_prediction(
            features=features,
            feature_names=app.config['FEATURE_COLUMNS']
        )
        
        logger.info("✓ Prediction explanation generated")
        
        # ===========================
        # 8. GET MODEL INFORMATION
        # ===========================
        
        model_info = prediction_engine.get_model_info()
        
        # ===========================
        # 9. PREPARE RESPONSE DATA
        # ===========================
        
        response_data = {
            # Student info
            'name': student_name,
            
            # Prediction results
            'prediction': predicted_marks,
            'confidence': confidence,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            
            # Grading
            'grade': grade,
            'status': status,
            'pass_probability': pass_probability,
            'risk_assessment': risk_assessment,
            
            # Study planning
            'days_remaining': comprehensive_plan['days_remaining'],
            'target_status': comprehensive_plan['target_feasibility']['status'],
            'target_status_class': comprehensive_plan['target_feasibility']['status_class'],
            'gap': comprehensive_plan['target_feasibility']['gap'],
            'recommended_study': comprehensive_plan['recommended_study_hours'],
            'planner_message': comprehensive_plan['planner_message'],
            'progress': comprehensive_plan['progress_percentage'],
            'daily_plan': comprehensive_plan['daily_plan'],
            'weekly_plan': comprehensive_plan['weekly_plan'],
            'subject_priorities': comprehensive_plan['subject_priorities'],
            'wellness_recommendations': comprehensive_plan['wellness_recommendations'],
            
            # Suggestions
            'suggestions': suggestions,
            'motivational_message': motivational_message,
            
            # Explainability
            'explanation_text': explanation['explanation_text'],
            'top_features': explanation['top_features'],
            
            # Model info
            'model_info': model_info,
            
            # Input data (for display)
            'exam_date': exam_date,
            'target_marks': target_marks,
            'input_features': feature_dict
        }
        
        logger.info("✓ Prediction request completed successfully")
        
        # ===========================
        # 10. RENDER RESULTS
        # ===========================
        
        return render_template("index.html", **response_data)
    
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {e}", exc_info=True)
        return render_template(
            "index.html",
            errors=["An unexpected error occurred. Please try again."],
            form_data=request.form
        )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    API endpoint for predictions (JSON input/output).
    
    Request JSON format:
    {
        "StudentName": "John Doe",
        "StudyHours": 6.5,
        "Attendance": 85.0,
        ... (all features)
        "ExamDate": "2026-08-15",
        "TargetMarks": 85
    }
    
    Response JSON format:
    {
        "success": true,
        "prediction": 78.5,
        "grade": "B",
        "confidence": 82.3,
        ...
    }
    """
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate inputs
        is_valid, sanitized_data = input_validator.validate_all_inputs(data)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'errors': input_validator.get_errors()
            }), 400
        
        # Extract features
        features = [sanitized_data.get(f, 0) for f in app.config['FEATURE_COLUMNS']]
        
        # Make prediction
        prediction_result = prediction_engine.predict_with_confidence(features)
        predicted_marks = prediction_result['prediction']
        
        # Generate insights
        grade, status = grading_system.calculate_grade_and_status(predicted_marks)
        risk = grading_system.assess_risk_level(predicted_marks)
        
        # Return JSON response
        return jsonify({
            'success': True,
            'prediction': predicted_marks,
            'confidence': prediction_result['confidence'],
            'grade': grade,
            'status': status,
            'risk_level': risk['level'],
            'pass_probability': grading_system.calculate_pass_probability(predicted_marks)
        })
    
    except Exception as e:
        logger.error(f"API prediction error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': prediction_engine.model is not None
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.url}")
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
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
