"""
Grading System Module
=====================
Handles grade calculation, performance status, and academic classification.

Author: AI-Based Student Performance Prediction Team
"""

from typing import Dict, Tuple


class GradingSystem:
    """
    Manages grading logic and performance classification.
    
    This class provides methods to calculate grades, performance status,
    and risk levels based on predicted marks.
    """
    
    def __init__(self, grade_boundaries: Dict[str, float], 
                 performance_status: Dict[str, str]):
        """
        Initialize GradingSystem with grade boundaries and status messages.
        
        Args:
            grade_boundaries: Dictionary mapping grades to minimum marks
            performance_status: Dictionary mapping grades to status messages
        """
        self.grade_boundaries = grade_boundaries
        self.performance_status = performance_status
    
    def calculate_grade(self, marks: float) -> str:
        """
        Calculate letter grade based on marks.
        
        Args:
            marks: Predicted or actual marks (0-100)
        
        Returns:
            Letter grade (A+, A, B, C, D, or F)
        """
        # Ensure marks are within valid range
        marks = max(0, min(100, marks))
        
        # Sort grade boundaries in descending order
        sorted_grades = sorted(
            self.grade_boundaries.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Find appropriate grade
        for grade, boundary in sorted_grades:
            if marks >= boundary:
                return grade
        
        return 'F'
    
    def get_performance_status(self, grade: str) -> str:
        """
        Get performance status message for a grade.
        
        Args:
            grade: Letter grade
        
        Returns:
            Performance status message
        """
        return self.performance_status.get(grade, 'Unknown')
    
    def calculate_grade_and_status(self, marks: float) -> Tuple[str, str]:
        """
        Calculate both grade and performance status.
        
        Args:
            marks: Predicted or actual marks
        
        Returns:
            Tuple of (grade, status)
        """
        grade = self.calculate_grade(marks)
        status = self.get_performance_status(grade)
        return grade, status
    
    def calculate_pass_probability(self, marks: float, 
                                   pass_threshold: float = 40.0) -> float:
        """
        Calculate probability of passing based on predicted marks.
        
        Args:
            marks: Predicted marks
            pass_threshold: Minimum passing marks
        
        Returns:
            Pass probability as percentage (0-100)
        """
        if marks >= pass_threshold + 10:
            return 95.0
        elif marks >= pass_threshold + 5:
            return 85.0
        elif marks >= pass_threshold:
            return 70.0
        elif marks >= pass_threshold - 5:
            return 50.0
        elif marks >= pass_threshold - 10:
            return 30.0
        else:
            return 15.0
    
    def assess_risk_level(self, marks: float) -> Dict[str, any]:
        """
        Assess student risk level based on predicted performance.
        
        Args:
            marks: Predicted marks
        
        Returns:
            Dictionary containing risk level, color, and message
        """
        if marks >= 70:
            return {
                'level': 'Low Risk',
                'color': 'success',
                'icon': '✅',
                'message': 'Student is performing well and likely to succeed.'
            }
        elif marks >= 50:
            return {
                'level': 'Moderate Risk',
                'color': 'warning',
                'icon': '⚠️',
                'message': 'Student needs consistent effort to improve performance.'
            }
        else:
            return {
                'level': 'High Risk',
                'color': 'danger',
                'icon': '🚨',
                'message': 'Student requires immediate intervention and support.'
            }
    
    def calculate_improvement_needed(self, current_marks: float, 
                                    target_marks: float) -> Dict[str, any]:
        """
        Calculate improvement metrics needed to reach target.
        
        Args:
            current_marks: Current/predicted marks
            target_marks: Target marks to achieve
        
        Returns:
            Dictionary with improvement metrics
        """
        gap = target_marks - current_marks
        percentage_increase = (gap / current_marks * 100) if current_marks > 0 else 0
        
        # Determine difficulty level
        if gap <= 5:
            difficulty = 'Easy'
            feasibility = 'Highly Achievable'
        elif gap <= 15:
            difficulty = 'Moderate'
            feasibility = 'Achievable with Effort'
        elif gap <= 25:
            difficulty = 'Challenging'
            feasibility = 'Requires Significant Effort'
        else:
            difficulty = 'Very Difficult'
            feasibility = 'May Need to Revise Target'
        
        return {
            'marks_gap': round(gap, 2),
            'percentage_increase': round(percentage_increase, 2),
            'difficulty': difficulty,
            'feasibility': feasibility
        }
    
    def generate_grade_insights(self, marks: float) -> Dict[str, any]:
        """
        Generate comprehensive grade insights.
        
        Args:
            marks: Predicted marks
        
        Returns:
            Dictionary with complete grading insights
        """
        grade, status = self.calculate_grade_and_status(marks)
        risk = self.assess_risk_level(marks)
        pass_prob = self.calculate_pass_probability(marks)
        
        return {
            'marks': round(marks, 2),
            'grade': grade,
            'status': status,
            'pass_probability': round(pass_prob, 2),
            'risk_assessment': risk
        }
