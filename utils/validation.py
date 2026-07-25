"""
Input Validation Module
=======================
Validates and sanitizes user inputs for security and data integrity.

Author: AI-Based Student Performance Prediction Team
"""

from typing import Dict, Tuple, Any
import re
from datetime import datetime


class InputValidator:
    """
    Handles validation and sanitization of all user inputs.
    
    Ensures data integrity, prevents injection attacks, and
    validates ranges for all input features.
    """
    
    def __init__(self, validation_ranges: Dict[str, Tuple[float, float]]):
        """
        Initialize validator with valid ranges for each feature.
        
        Args:
            validation_ranges: Dictionary mapping feature names to (min, max) tuples
        """
        self.validation_ranges = validation_ranges
        self.errors = []
    
    def reset_errors(self):
        """Clear error list."""
        self.errors = []
    
    def validate_name(self, name: str) -> Tuple[bool, str]:
        """
        Validate student name.
        
        Args:
            name: Student name string
        
        Returns:
            Tuple of (is_valid, sanitized_name)
        """
        if not name or not isinstance(name, str):
            self.errors.append("Student name is required")
            return False, ""
        
        # Remove extra whitespace
        name = name.strip()
        
        # Check length
        if len(name) < 2:
            self.errors.append("Student name must be at least 2 characters")
            return False, ""
        
        if len(name) > 100:
            self.errors.append("Student name must be less than 100 characters")
            return False, ""
        
        # Allow only letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            self.errors.append("Student name contains invalid characters")
            return False, ""
        
        return True, name
    
    def validate_numeric(self, value: Any, field_name: str) -> Tuple[bool, float]:
        """
        Validate numeric input fields.
        
        Args:
            value: Input value to validate
            field_name: Name of the field for error messages
        
        Returns:
            Tuple of (is_valid, converted_value)
        """
        # Check if field has defined ranges
        if field_name not in self.validation_ranges:
            self.errors.append(f"Unknown field: {field_name}")
            return False, 0.0
        
        # Try to convert to float
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            self.errors.append(f"{field_name} must be a valid number")
            return False, 0.0
        
        # Check range
        min_val, max_val = self.validation_ranges[field_name]
        
        if numeric_value < min_val or numeric_value > max_val:
            self.errors.append(
                f"{field_name} must be between {min_val} and {max_val}"
            )
            return False, 0.0
        
        return True, round(numeric_value, 2)
    
    def validate_date(self, date_str: str) -> Tuple[bool, str]:
        """
        Validate exam date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        
        Returns:
            Tuple of (is_valid, date_string)
        """
        if not date_str:
            self.errors.append("Exam date is required")
            return False, ""
        
        try:
            exam_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if date is not too far in the past
            today = datetime.today().date()
            days_diff = (exam_date - today).days
            
            if days_diff < -30:
                self.errors.append("Exam date cannot be more than 30 days in the past")
                return False, ""
            
            if days_diff > 365:
                self.errors.append("Exam date cannot be more than 1 year in the future")
                return False, ""
            
            return True, date_str
            
        except ValueError:
            self.errors.append("Invalid exam date format. Use YYYY-MM-DD")
            return False, ""
    
    def validate_all_inputs(self, form_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate all form inputs at once.
        
        Args:
            form_data: Dictionary of form field names to values
        
        Returns:
            Tuple of (all_valid, sanitized_data)
        """
        self.reset_errors()
        sanitized_data = {}
        all_valid = True
        
        # Validate student name
        if 'StudentName' in form_data:
            valid, name = self.validate_name(form_data['StudentName'])
            if valid:
                sanitized_data['StudentName'] = name
            else:
                all_valid = False
        
        # Validate exam date
        if 'ExamDate' in form_data:
            valid, date = self.validate_date(form_data['ExamDate'])
            if valid:
                sanitized_data['ExamDate'] = date
            else:
                all_valid = False
        
        # Validate target marks
        if 'TargetMarks' in form_data:
            valid, target = self.validate_numeric(form_data['TargetMarks'], 'TargetMarks')
            if valid:
                # Target marks use same range as FinalMarks (0-100)
                if 0 <= target <= 100:
                    sanitized_data['TargetMarks'] = target
                else:
                    self.errors.append("Target marks must be between 0 and 100")
                    all_valid = False
            else:
                all_valid = False
        
        # Validate all numeric features
        numeric_fields = [
            'StudyHours', 'Attendance', 'PreviousMarks', 'SleepHours',
            'StressLevel', 'InternetUsage', 'AssignmentCompletion',
            'ClassParticipation', 'PreviousSemesterGPA', 'InternalMarks',
            'FamilySupport', 'HealthScore', 'ExamPrepDays',
            'DistractionHours', 'MockTestScore', 'ExtracurricularActivity'
        ]
        
        for field in numeric_fields:
            if field in form_data:
                valid, value = self.validate_numeric(form_data[field], field)
                if valid:
                    sanitized_data[field] = value
                else:
                    all_valid = False
        
        return all_valid, sanitized_data
    
    def get_errors(self) -> list:
        """
        Get list of validation errors.
        
        Returns:
            List of error messages
        """
        return self.errors
    
    def sanitize_string(self, text: str, max_length: int = 500) -> str:
        """
        Sanitize string input to prevent XSS and injection.
        
        Args:
            text: Input string
            max_length: Maximum allowed length
        
        Returns:
            Sanitized string
        """
        if not text:
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        # Trim whitespace
        text = text.strip()
        
        # Limit length
        text = text[:max_length]
        
        # Remove potentially dangerous characters
        # (Basic sanitization - in production, use libraries like bleach)
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        return text
    
    def validate_feature_vector(self, features: list) -> Tuple[bool, list]:
        """
        Validate a feature vector for model prediction.
        
        Args:
            features: List of feature values
        
        Returns:
            Tuple of (is_valid, sanitized_features)
        """
        self.reset_errors()
        
        if not isinstance(features, list):
            self.errors.append("Features must be a list")
            return False, []
        
        # Check if we have the right number of features
        # This should match the number of features the model expects
        expected_features = len(self.validation_ranges)
        
        if len(features) != expected_features:
            self.errors.append(
                f"Expected {expected_features} features, got {len(features)}"
            )
            return False, []
        
        # Validate each feature is numeric and within range
        sanitized = []
        for i, value in enumerate(features):
            try:
                num_val = float(value)
                # Additional range check could be added here
                sanitized.append(num_val)
            except (ValueError, TypeError):
                self.errors.append(f"Feature at index {i} is not a valid number")
                return False, []
        
        return True, sanitized
