"""
Suggestions Generator Module
============================
Generates personalized improvement suggestions based on student data.

Author: AI-Based Student Performance Prediction Team
"""

from typing import List, Dict


class SuggestionsGenerator:
    """
    Generates personalized, actionable suggestions for students
    based on their performance indicators and predicted outcomes.
    """
    
    def __init__(self, config):
        """
        Initialize suggestions generator with configuration.
        
        Args:
            config: Configuration object with thresholds
        """
        self.config = config
    
    def generate_suggestions(self, student_data: Dict, predicted_marks: float) -> List[str]:
        """
        Generate comprehensive personalized suggestions.
        
        Args:
            student_data: Dictionary with student feature values
            predicted_marks: Predicted final marks
        
        Returns:
            List of actionable suggestion strings
        """
        suggestions = []
        
        # Attendance suggestions
        suggestions.extend(self._attendance_suggestions(student_data.get('Attendance', 0)))
        
        # Study hours suggestions
        suggestions.extend(self._study_hours_suggestions(student_data.get('StudyHours', 0)))
        
        # Sleep suggestions
        suggestions.extend(self._sleep_suggestions(student_data.get('SleepHours', 0)))
        
        # Previous performance suggestions
        suggestions.extend(self._previous_marks_suggestions(student_data.get('PreviousMarks', 0)))
        
        # Stress level suggestions
        if 'StressLevel' in student_data:
            suggestions.extend(self._stress_suggestions(student_data['StressLevel']))
        
        # Assignment completion suggestions
        if 'AssignmentCompletion' in student_data:
            suggestions.extend(self._assignment_suggestions(student_data['AssignmentCompletion']))
        
        # Class participation suggestions
        if 'ClassParticipation' in student_data:
            suggestions.extend(self._participation_suggestions(student_data['ClassParticipation']))
        
        # Internet usage suggestions
        if 'InternetUsage' in student_data:
            suggestions.extend(self._internet_suggestions(student_data['InternetUsage']))
        
        # Mock test suggestions
        if 'MockTestScore' in student_data:
            suggestions.extend(self._mock_test_suggestions(student_data['MockTestScore']))
        
        # Overall performance suggestions
        suggestions.extend(self._performance_suggestions(predicted_marks))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion not in seen:
                seen.add(suggestion)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions
    
    def _attendance_suggestions(self, attendance: float) -> List[str]:
        """Generate attendance-related suggestions."""
        suggestions = []
        
        if attendance < 60:
            suggestions.append(
                "🚨 Critical: Your attendance is very low. Aim for at least 75% attendance."
            )
            suggestions.append(
                "Missing classes leads to knowledge gaps. Try to attend all remaining classes."
            )
        elif attendance < 75:
            suggestions.append(
                "⚠️ Improve your attendance to above 75% to avoid missing important concepts."
            )
        elif attendance < 85:
            suggestions.append(
                "📈 Good attendance! Try to maintain above 85% for optimal learning."
            )
        else:
            suggestions.append(
                "✅ Excellent attendance! Keep it up."
            )
        
        return suggestions
    
    def _study_hours_suggestions(self, study_hours: float) -> List[str]:
        """Generate study hours suggestions."""
        suggestions = []
        
        if study_hours < 3:
            suggestions.append(
                "📚 Increase your daily study hours significantly. Aim for at least 5-6 hours."
            )
        elif study_hours < 5:
            suggestions.append(
                "📖 Increase your daily study hours to 5-7 hours for better preparation."
            )
        elif study_hours > 9:
            suggestions.append(
                "⚠️ You're studying a lot! Ensure you're studying efficiently and taking breaks."
            )
        else:
            suggestions.append(
                "✅ Your study hours are in a good range. Focus on quality over quantity."
            )
        
        return suggestions
    
    def _sleep_suggestions(self, sleep_hours: float) -> List[str]:
        """Generate sleep-related suggestions."""
        suggestions = []
        
        if sleep_hours < 5:
            suggestions.append(
                "😴 Critical: You need more sleep! Aim for 7-8 hours for better memory and focus."
            )
        elif sleep_hours < 6:
            suggestions.append(
                "⚠️ Sleep at least 6-8 hours daily for better concentration and retention."
            )
        elif sleep_hours > 9:
            suggestions.append(
                "Too much sleep can reduce productivity. Try to maintain 7-8 hours."
            )
        else:
            suggestions.append(
                "✅ Your sleep schedule is healthy. Maintain this routine."
            )
        
        return suggestions
    
    def _previous_marks_suggestions(self, previous_marks: float) -> List[str]:
        """Generate suggestions based on previous performance."""
        suggestions = []
        
        if previous_marks < 50:
            suggestions.append(
                "📝 Focus heavily on building strong fundamentals and basics."
            )
            suggestions.append(
                "Consider getting help from teachers or tutors to improve understanding."
            )
        elif previous_marks < 60:
            suggestions.append(
                "📚 Strengthen your fundamentals with regular practice and revision."
            )
        elif previous_marks < 75:
            suggestions.append(
                "👍 Build on your solid foundation by tackling more challenging problems."
            )
        else:
            suggestions.append(
                "🌟 Great previous performance! Maintain consistency and aim higher."
            )
        
        return suggestions
    
    def _stress_suggestions(self, stress_level: float) -> List[str]:
        """Generate stress management suggestions."""
        suggestions = []
        
        if stress_level >= 8:
            suggestions.append(
                "🧘 High stress alert! Practice relaxation techniques like meditation or deep breathing."
            )
            suggestions.append(
                "Consider talking to a counselor or trusted adult about your stress."
            )
        elif stress_level >= 6:
            suggestions.append(
                "⚠️ Moderate stress detected. Take regular breaks and engage in hobbies."
            )
        else:
            suggestions.append(
                "✅ Your stress levels are manageable. Keep maintaining work-life balance."
            )
        
        return suggestions
    
    def _assignment_suggestions(self, completion_rate: float) -> List[str]:
        """Generate assignment completion suggestions."""
        suggestions = []
        
        if completion_rate < 60:
            suggestions.append(
                "📝 Complete all assignments on time. They reinforce learning and improve grades."
            )
        elif completion_rate < 80:
            suggestions.append(
                "Try to complete at least 90% of assignments for better understanding."
            )
        else:
            suggestions.append(
                "✅ Excellent assignment completion rate! Keep it up."
            )
        
        return suggestions
    
    def _participation_suggestions(self, participation: float) -> List[str]:
        """Generate class participation suggestions."""
        suggestions = []
        
        if participation < 5:
            suggestions.append(
                "🙋 Participate more actively in class discussions and ask questions."
            )
        elif participation < 7:
            suggestions.append(
                "Increase your class participation to clarify doubts and deepen understanding."
            )
        else:
            suggestions.append(
                "✅ Great class participation! Active learning helps retention."
            )
        
        return suggestions
    
    def _internet_suggestions(self, internet_hours: float) -> List[str]:
        """Generate internet usage suggestions."""
        suggestions = []
        
        if internet_hours > 6:
            suggestions.append(
                "📱 Reduce non-academic internet usage. It's affecting your study time."
            )
            suggestions.append(
                "Use apps or tools to limit social media during study hours."
            )
        elif internet_hours > 4:
            suggestions.append(
                "⚠️ Monitor your internet usage. Keep it under 3-4 hours for better focus."
            )
        
        return suggestions
    
    def _mock_test_suggestions(self, mock_score: float) -> List[str]:
        """Generate mock test suggestions."""
        suggestions = []
        
        if mock_score < 50:
            suggestions.append(
                "📊 Your mock test score indicates need for improvement. Focus on weak topics."
            )
            suggestions.append(
                "Take more practice tests and analyze your mistakes carefully."
            )
        elif mock_score < 70:
            suggestions.append(
                "Practice more mock tests to improve speed and accuracy."
            )
        else:
            suggestions.append(
                "✅ Strong mock test performance! Maintain this momentum."
            )
        
        return suggestions
    
    def _performance_suggestions(self, predicted_marks: float) -> List[str]:
        """Generate overall performance suggestions."""
        suggestions = []
        
        if predicted_marks >= 90:
            suggestions.append(
                "🌟 Excellent predicted performance! Maintain your current strategy."
            )
            suggestions.append(
                "Challenge yourself with advanced problems to reach perfection."
            )
        elif predicted_marks >= 80:
            suggestions.append(
                "👍 You're close to excellence! A little more effort can get you to 90+."
            )
            suggestions.append(
                "Focus on accuracy and time management in exams."
            )
        elif predicted_marks >= 70:
            suggestions.append(
                "📈 Good performance trajectory. Consistent effort can help you achieve an A grade."
            )
        elif predicted_marks >= 60:
            suggestions.append(
                "⚠️ You're at average level. Increase study hours and focus on weak areas."
            )
        else:
            suggestions.append(
                "🚨 Immediate action needed! Seek help, increase study time, and stay focused."
            )
            suggestions.append(
                "Regular study and better attendance can significantly improve your marks."
            )
        
        return suggestions
    
    def generate_motivational_message(self, predicted_marks: float, 
                                     target_marks: float) -> str:
        """
        Generate motivational message based on performance.
        
        Args:
            predicted_marks: Predicted performance
            target_marks: Target to achieve
        
        Returns:
            Motivational message string
        """
        gap = target_marks - predicted_marks
        
        if gap <= 0:
            return "🎉 You're on track to exceed your target! Stay consistent and believe in yourself!"
        elif gap <= 10:
            return "💪 You're very close to your target! A focused effort will get you there!"
        elif gap <= 20:
            return "🎯 Your target is challenging but achievable! Work smart and stay determined!"
        else:
            return "🌱 Every expert was once a beginner. Focus on steady improvement, one step at a time!"
