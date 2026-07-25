"""
Study Planner Module
====================
Intelligent study planning and recommendation system.

Author: AI-Based Student Performance Prediction Team
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class StudyPlanner:
    """
    Intelligent study planning system that generates personalized
    study recommendations, schedules, and improvement strategies.
    """
    
    def __init__(self, config):
        """
        Initialize StudyPlanner with configuration.
        
        Args:
            config: Configuration object with thresholds and limits
        """
        self.config = config
    
    def calculate_days_remaining(self, exam_date_str: str) -> int:
        """
        Calculate days remaining until exam.
        
        Args:
            exam_date_str: Exam date in YYYY-MM-DD format
        
        Returns:
            Number of days remaining (minimum 0)
        """
        try:
            today = datetime.today().date()
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
            days = (exam_date - today).days
            return max(0, days)
        except:
            return 0
    
    def assess_target_feasibility(self, predicted_marks: float,
                                  target_marks: float,
                                  days_remaining: int) -> Dict[str, any]:
        """
        Assess if target marks are achievable.
        
        Args:
            predicted_marks: Current predicted marks
            target_marks: Target marks student wants to achieve
            days_remaining: Days until exam
        
        Returns:
            Dictionary with feasibility assessment
        """
        gap = target_marks - predicted_marks
        
        # Determine target status
        if gap <= self.config.TARGET_GAP_ACHIEVABLE:
            status = '🟢 Achievable'
            status_class = 'achievable'
        elif (gap <= self.config.TARGET_GAP_CHALLENGING and 
              days_remaining >= self.config.TARGET_MIN_DAYS_CHALLENGING):
            status = '🟡 Challenging'
            status_class = 'challenging'
        else:
            status = '🔴 Unrealistic'
            status_class = 'unrealistic'
        
        return {
            'status': status,
            'status_class': status_class,
            'gap': round(gap, 2)
        }
    
    def calculate_recommended_study_hours(self, current_study: float,
                                          target_feasibility: Dict[str, any]) -> float:
        """
        Calculate recommended daily study hours.
        
        Args:
            current_study: Current daily study hours
            target_feasibility: Target feasibility assessment
        
        Returns:
            Recommended study hours per day
        """
        status_class = target_feasibility['status_class']
        
        if status_class == 'achievable':
            recommended = max(current_study, self.config.MIN_STUDY_HOURS)
        elif status_class == 'challenging':
            recommended = max(
                current_study + self.config.RECOMMENDED_STUDY_INCREMENT_CHALLENGING,
                self.config.MIN_RECOMMENDED_STUDY
            )
        else:  # unrealistic
            recommended = max(
                current_study + self.config.RECOMMENDED_STUDY_INCREMENT_UNREALISTIC,
                self.config.MIN_RECOMMENDED_STUDY + 1
            )
        
        # Cap at maximum recommended study hours
        recommended = min(recommended, self.config.MAX_RECOMMENDED_STUDY)
        
        return round(recommended, 1)
    
    def generate_planner_message(self, target_feasibility: Dict[str, any]) -> str:
        """
        Generate personalized planner message.
        
        Args:
            target_feasibility: Target feasibility assessment
        
        Returns:
            Personalized message string
        """
        status_class = target_feasibility['status_class']
        
        messages = {
            'achievable': (
                "Your target is realistic. Stay consistent with your preparation "
                "and maintain your current study routine."
            ),
            'challenging': (
                "Your target is possible with extra effort. Focus on regular revision, "
                "practice problems, and seek help when needed."
            ),
            'unrealistic': (
                "Your target is difficult with the remaining time. Focus on improving "
                "your score step by step rather than targeting perfection."
            )
        }
        
        return messages.get(status_class, "Keep working hard!")
    
    def calculate_progress_percentage(self, predicted_marks: float,
                                     target_marks: float) -> float:
        """
        Calculate progress towards target as percentage.
        
        Args:
            predicted_marks: Current predicted marks
            target_marks: Target marks
        
        Returns:
            Progress percentage (0-100)
        """
        if target_marks <= 0:
            return 0.0
        
        progress = (predicted_marks / target_marks) * 100
        return round(min(100, max(0, progress)), 2)
    
    def generate_daily_study_plan(self, recommended_hours: float,
                                  days_remaining: int) -> List[Dict[str, any]]:
        """
        Generate a daily study plan breakdown.
        
        Args:
            recommended_hours: Recommended daily study hours
            days_remaining: Days until exam
        
        Returns:
            List of daily study activities
        """
        # Basic time allocation
        theory_time = recommended_hours * 0.4
        practice_time = recommended_hours * 0.35
        revision_time = recommended_hours * 0.25
        
        plan = [
            {
                'activity': '📖 Theory & Concepts',
                'hours': round(theory_time, 1),
                'description': 'Read textbooks, watch lectures, understand concepts'
            },
            {
                'activity': '✍️ Practice Problems',
                'hours': round(practice_time, 1),
                'description': 'Solve exercises, work on assignments, mock tests'
            },
            {
                'activity': '🔄 Revision',
                'hours': round(revision_time, 1),
                'description': 'Review notes, summarize key points, flashcards'
            }
        ]
        
        return plan
    
    def generate_weekly_plan(self, days_remaining: int) -> List[Dict[str, str]]:
        """
        Generate weekly study plan milestones.
        
        Args:
            days_remaining: Days until exam
        
        Returns:
            List of weekly milestones
        """
        weeks_remaining = max(1, days_remaining // 7)
        
        if weeks_remaining >= 8:
            plan = [
                {'week': 'Week 1-2', 'focus': 'Complete syllabus, identify weak areas'},
                {'week': 'Week 3-4', 'focus': 'Practice problems, strengthen concepts'},
                {'week': 'Week 5-6', 'focus': 'Mock tests, time management practice'},
                {'week': 'Week 7-8', 'focus': 'Intensive revision, formula sheets'},
                {'week': 'Last Week', 'focus': 'Light revision, stay calm, rest well'}
            ]
        elif weeks_remaining >= 4:
            plan = [
                {'week': 'Week 1-2', 'focus': 'Cover important topics, practice daily'},
                {'week': 'Week 3', 'focus': 'Mock tests and problem solving'},
                {'week': 'Week 4', 'focus': 'Final revision and confidence building'}
            ]
        else:
            plan = [
                {'week': 'This Week', 'focus': 'Focus on high-weightage topics'},
                {'week': 'Last Few Days', 'focus': 'Quick revision and stay positive'}
            ]
        
        return plan
    
    def generate_subject_priorities(self, marks: float) -> List[Dict[str, str]]:
        """
        Generate subject/topic priority recommendations.
        
        Args:
            marks: Predicted marks
        
        Returns:
            List of priority recommendations
        """
        if marks < 50:
            priorities = [
                {'priority': 'High', 'focus': 'Basic fundamentals and easy topics'},
                {'priority': 'Medium', 'focus': 'Moderate difficulty problems'},
                {'priority': 'Low', 'focus': 'Advanced topics (if time permits)'}
            ]
        elif marks < 75:
            priorities = [
                {'priority': 'High', 'focus': 'Medium-weightage topics you struggle with'},
                {'priority': 'Medium', 'focus': 'High-difficulty challenging topics'},
                {'priority': 'Low', 'focus': 'Easy topics for confidence boost'}
            ]
        else:
            priorities = [
                {'priority': 'High', 'focus': 'Advanced problems and edge cases'},
                {'priority': 'Medium', 'focus': 'Speed and accuracy improvement'},
                {'priority': 'Low', 'focus': 'Quick revision of basics'}
            ]
        
        return priorities
    
    def generate_wellness_recommendations(self, sleep_hours: float,
                                         stress_level: float = None) -> List[str]:
        """
        Generate wellness and health recommendations.
        
        Args:
            sleep_hours: Current sleep hours
            stress_level: Stress level (1-10)
        
        Returns:
            List of wellness recommendations
        """
        recommendations = []
        
        # Sleep recommendations
        if sleep_hours < 6:
            recommendations.append(
                "⚠️ Increase sleep to 7-8 hours for better memory retention and focus"
            )
        elif sleep_hours > 9:
            recommendations.append(
                "Consider reducing sleep to 7-8 hours for optimal productivity"
            )
        else:
            recommendations.append(
                "✅ Your sleep schedule is healthy. Maintain this routine"
            )
        
        # Break recommendations
        recommendations.append(
            "Take 5-10 minute breaks every hour to maintain concentration"
        )
        
        # Physical activity
        recommendations.append(
            "Include 20-30 minutes of physical activity daily to reduce stress"
        )
        
        # Stress management
        if stress_level and stress_level > 7:
            recommendations.append(
                "⚠️ High stress detected. Practice meditation or breathing exercises"
            )
        
        return recommendations
    
    def generate_comprehensive_plan(self, predicted_marks: float,
                                   target_marks: float,
                                   current_study: float,
                                   exam_date: str,
                                   sleep_hours: float) -> Dict[str, any]:
        """
        Generate comprehensive study plan with all recommendations.
        
        Args:
            predicted_marks: Predicted performance
            target_marks: Target to achieve
            current_study: Current study hours
            exam_date: Exam date string
            sleep_hours: Current sleep hours
        
        Returns:
            Complete study plan dictionary
        """
        days_remaining = self.calculate_days_remaining(exam_date)
        feasibility = self.assess_target_feasibility(
            predicted_marks, target_marks, days_remaining
        )
        recommended_hours = self.calculate_recommended_study_hours(
            current_study, feasibility
        )
        progress = self.calculate_progress_percentage(predicted_marks, target_marks)
        
        return {
            'days_remaining': days_remaining,
            'target_feasibility': feasibility,
            'recommended_study_hours': recommended_hours,
            'planner_message': self.generate_planner_message(feasibility),
            'progress_percentage': progress,
            'daily_plan': self.generate_daily_study_plan(recommended_hours, days_remaining),
            'weekly_plan': self.generate_weekly_plan(days_remaining),
            'subject_priorities': self.generate_subject_priorities(predicted_marks),
            'wellness_recommendations': self.generate_wellness_recommendations(sleep_hours)
        }
