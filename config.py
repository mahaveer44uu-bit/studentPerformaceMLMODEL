"""
Configuration Module for Student Performance Prediction System
================================================================
This module centralizes all configuration variables for the application.

Author: AI-Based Student Performance Prediction Team
Version: 2.0
"""

import os
from datetime import timedelta

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class with default settings."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Application Settings
    APP_NAME = "AI-Based Student Performance Prediction System"
    APP_VERSION = "2.0.0"
    
    # Model Configuration
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'student_model.pkl')
    MODEL_METADATA_PATH = os.path.join(BASE_DIR, 'models', 'model_metadata.json')
    SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')
    
    # Dataset Configuration
    DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'dataset.csv')
    DATASET_SIZE = 2000  # Increased from 1000
    RANDOM_SEED = 42
    
    # Feature Configuration
    FEATURE_COLUMNS = [
        'StudyHours',
        'Attendance',
        'PreviousMarks',
        'SleepHours',
        'StressLevel',
        'InternetUsage',
        'AssignmentCompletion',
        'ClassParticipation',
        'PreviousSemesterGPA',
        'InternalMarks',
        'FamilySupport',
        'HealthScore',
        'ExamPrepDays',
        'DistractionHours',
        'MockTestScore',
        'ExtracurricularActivity'
    ]
    
    TARGET_COLUMN = 'FinalMarks'
    
    # Model Training Configuration
    TEST_SIZE = 0.2
    CROSS_VALIDATION_FOLDS = 5
    ENABLE_HYPERPARAMETER_TUNING = True
    ENABLE_FEATURE_ENGINEERING = True
    
    # Grading System
    GRADE_BOUNDARIES = {
        'A+': 90,
        'A': 80,
        'B': 70,
        'C': 60,
        'D': 40,
        'F': 0
    }
    
    # Performance Status Messages
    PERFORMANCE_STATUS = {
        'A+': 'Excellent Performance 🌟',
        'A': 'Very Good 👍',
        'B': 'Good 🙂',
        'C': 'Average',
        'D': 'Needs Improvement',
        'F': 'Fail'
    }
    
    # Target Planner Thresholds
    TARGET_GAP_ACHIEVABLE = 5
    TARGET_GAP_CHALLENGING = 15
    TARGET_MIN_DAYS_CHALLENGING = 20
    
    # Study Recommendations
    MIN_STUDY_HOURS = 5
    RECOMMENDED_STUDY_INCREMENT_CHALLENGING = 1.5
    RECOMMENDED_STUDY_INCREMENT_UNREALISTIC = 2
    MIN_RECOMMENDED_STUDY = 6
    MAX_RECOMMENDED_STUDY = 10
    
    # Validation Ranges
    VALIDATION_RANGES = {
        'StudyHours': (0.5, 12),
        'Attendance': (0, 100),
        'PreviousMarks': (0, 100),
        'SleepHours': (3, 12),
        'StressLevel': (1, 10),
        'InternetUsage': (0, 12),
        'AssignmentCompletion': (0, 100),
        'ClassParticipation': (1, 10),
        'PreviousSemesterGPA': (0, 10),
        'InternalMarks': (0, 100),
        'FamilySupport': (1, 10),
        'HealthScore': (1, 10),
        'ExamPrepDays': (0, 90),
        'DistractionHours': (0, 12),
        'MockTestScore': (0, 100),
        'ExtracurricularActivity': (0, 20)
    }
    
    # Thresholds for Suggestions
    MIN_ATTENDANCE = 75
    MIN_SLEEP_HOURS = 6
    MAX_SLEEP_HOURS = 8
    MIN_STUDY_HOURS_THRESHOLD = 5
    MIN_PREVIOUS_MARKS = 60
    
    # Logging Configuration
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Export Configuration
    EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
    ALLOW_PDF_EXPORT = True
    ALLOW_EXCEL_EXPORT = True
    
    # Security Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Rate Limiting (requests per minute)
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_DEFAULT = "100 per minute"
    
    # Visualization Configuration
    PLOT_STYLE = 'seaborn-v0_8-darkgrid'
    FIGURE_DPI = 100
    CHART_COLORS = ['#2ee59d', '#00b4ff', '#a66aff', '#ff6b9d', '#ffd93d']


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Override with environment variables in production
    # Note: This will use the default SECRET_KEY if not set
    # In actual production deployment, always set SECRET_KEY environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env='default'):
    """Get configuration based on environment."""
    return config.get(env, config['default'])
