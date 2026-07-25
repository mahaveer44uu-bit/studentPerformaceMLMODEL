"""
Enhanced Dataset Generator
===========================
Generates realistic student performance dataset with 16 features.

Features include study habits, attendance, previous performance,
wellness factors, and engagement metrics.

Author: AI-Based Student Performance Prediction Team
Version: 2.0
"""

import numpy as np
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

# Set random seed for reproducibility
np.random.seed(Config.RANDOM_SEED)

def generate_correlated_features(n_samples):
    """
    Generate correlated student features with realistic relationships.
    
    Args:
        n_samples: Number of student records to generate
    
    Returns:
        Dictionary of feature arrays
    """
    data = {}
    
    # ============================================================
    # BASELINE CHARACTERISTICS
    # ============================================================
    
    # Previous Semester GPA (foundation for other features)
    data['PreviousSemesterGPA'] = np.clip(
        np.random.normal(6.5, 1.5, n_samples), 3.0, 10.0
    )
    
    # Previous Marks (correlated with GPA)
    data['PreviousMarks'] = np.clip(
        np.random.normal(
            55 + data['PreviousSemesterGPA'] * 4,
            12
        ),
        30, 98
    )
    
    # Internal Marks (correlated with previous performance)
    data['InternalMarks'] = np.clip(
        np.random.normal(
            50 + data['PreviousMarks'] * 0.35,
            10
        ),
        20, 95
    )
    
    # Mock Test Score (slightly noisy, correlated with ability)
    data['MockTestScore'] = np.clip(
        np.random.normal(
            45 + data['PreviousSemesterGPA'] * 5,
            15
        ),
        20, 100
    )
    
    # ============================================================
    # STUDY HABITS & ENGAGEMENT
    # ============================================================
    
    # Study Hours (higher for more motivated students)
    data['StudyHours'] = np.clip(
        np.random.normal(
            4 + data['PreviousSemesterGPA'] * 0.4,
            2.0
        ),
        0.5, 12
    )
    
    # Attendance (correlated with discipline and performance)
    data['Attendance'] = np.clip(
        np.random.normal(
            60 + data['PreviousSemesterGPA'] * 4 + data['StudyHours'] * 2,
            10
        ),
        45, 100
    )
    
    # Assignment Completion Rate
    data['AssignmentCompletion'] = np.clip(
        np.random.normal(
            50 + data['StudyHours'] * 6 + data['Attendance'] * 0.3,
            15
        ),
        20, 100
    )
    
    # Class Participation (1-10 scale)
    data['ClassParticipation'] = np.clip(
        np.random.normal(
            4 + data['Attendance'] * 0.05 + data['PreviousSemesterGPA'] * 0.3,
            2.0
        ),
        1, 10
    )
    
    # Exam Preparation Days
    data['ExamPrepDays'] = np.clip(
        np.random.normal(
            10 + data['StudyHours'] * 3,
            10
        ),
        2, 60
    )
    
    # ============================================================
    # WELLNESS & LIFESTYLE FACTORS
    # ============================================================
    
    # Sleep Hours (inverse relationship with extreme study hours)
    data['SleepHours'] = np.clip(
        np.random.normal(
            7.5 - np.maximum(0, data['StudyHours'] - 7) * 0.3,
            1.2
        ),
        3, 10
    )
    
    # Stress Level (1-10, higher for overworkers and low performers)
    stress_base = 5
    stress_from_study = np.where(data['StudyHours'] > 8, 2, 0)
    stress_from_performance = np.where(data['PreviousMarks'] < 60, 2, 0)
    stress_from_sleep = np.where(data['SleepHours'] < 6, 1.5, 0)
    
    data['StressLevel'] = np.clip(
        stress_base + stress_from_study + stress_from_performance + 
        stress_from_sleep + np.random.normal(0, 1.5, n_samples),
        1, 10
    )
    
    # Health Score (1-10, affected by sleep and stress)
    data['HealthScore'] = np.clip(
        np.random.normal(
            7 + (data['SleepHours'] - 7) * 0.5 - (data['StressLevel'] - 5) * 0.3,
            1.5
        ),
        1, 10
    )
    
    # ============================================================
    # DISTRACTIONS & EXTERNAL FACTORS
    # ============================================================
    
    # Internet Usage (hours per day, higher for low discipline)
    data['InternetUsage'] = np.clip(
        np.random.normal(
            6 - data['StudyHours'] * 0.3 - data['Attendance'] * 0.02,
            2.5
        ),
        0.5, 12
    )
    
    # Distraction Hours (inverse of focus)
    data['DistractionHours'] = np.clip(
        np.random.normal(
            5 - data['ClassParticipation'] * 0.3 + data['InternetUsage'] * 0.2,
            2.0
        ),
        0.5, 10
    )
    
    # Family Support (1-10 scale)
    data['FamilySupport'] = np.clip(
        np.random.normal(7, 2.0, n_samples),
        1, 10
    )
    
    # Extracurricular Activity (hours per week)
    data['ExtracurricularActivity'] = np.clip(
        np.random.normal(5, 4, n_samples),
        0, 20
    )
    
    return data


def calculate_final_marks(features):
    """
    Calculate final marks using realistic non-linear relationships.
    
    Args:
        features: Dictionary of feature arrays
    
    Returns:
        Array of final marks (0-100)
    """
    n = len(features['StudyHours'])
    
    # ============================================================
    # POSITIVE CONTRIBUTIONS
    # ============================================================
    
    # Study effect (diminishing returns after 7-8 hours)
    study_effect = 8 * np.sqrt(features['StudyHours'])
    
    # Attendance effect (linear, important)
    attendance_effect = 0.28 * features['Attendance']
    
    # Previous marks effect (strong predictor)
    previous_effect = 0.35 * features['PreviousMarks']
    
    # Internal marks effect
    internal_effect = 0.15 * features['InternalMarks']
    
    # Mock test effect
    mock_effect = 0.12 * features['MockTestScore']
    
    # Assignment completion effect
    assignment_effect = 0.08 * features['AssignmentCompletion']
    
    # Class participation effect
    participation_effect = 1.2 * features['ClassParticipation']
    
    # Previous semester GPA effect
    gpa_effect = 2.5 * features['PreviousSemesterGPA']
    
    # Exam preparation effect
    prep_effect = 0.15 * np.log1p(features['ExamPrepDays'])
    
    # Family support effect (small but positive)
    family_effect = 0.8 * features['FamilySupport']
    
    # ============================================================
    # WELLNESS EFFECTS (NON-LINEAR)
    # ============================================================
    
    # Sleep effect (optimal at 7-8 hours)
    sleep_effect = -1.2 * (features['SleepHours'] - 7.5) ** 2 + 9
    
    # Health effect
    health_effect = 0.6 * features['HealthScore']
    
    # ============================================================
    # NEGATIVE CONTRIBUTIONS
    # ============================================================
    
    # Stress penalty (exponential beyond threshold)
    stress_penalty = np.where(
        features['StressLevel'] > 7,
        (features['StressLevel'] - 7) ** 1.5 * 2,
        0
    )
    
    # Internet usage penalty (for excessive use)
    internet_penalty = np.where(
        features['InternetUsage'] > 6,
        (features['InternetUsage'] - 6) * 1.5,
        0
    )
    
    # Distraction penalty
    distraction_penalty = features['DistractionHours'] * 0.8
    
    # ============================================================
    # INTERACTION EFFECTS
    # ============================================================
    
    # Burnout: high study + low sleep = severe penalty
    burnout_penalty = np.where(
        (features['StudyHours'] > 9) & (features['SleepHours'] < 6),
        5,
        0
    )
    
    # Synergy: good attendance + high study = bonus
    synergy_bonus = np.where(
        (features['Attendance'] > 85) & (features['StudyHours'] > 6),
        3,
        0
    )
    
    # Extracurricular balance (small benefit if moderate)
    extra_effect = np.where(
        (features['ExtracurricularActivity'] >= 3) & 
        (features['ExtracurricularActivity'] <= 10),
        2,
        0
    )
    
    # ============================================================
    # FINAL CALCULATION
    # ============================================================
    
    base_score = (
        study_effect +
        attendance_effect +
        previous_effect +
        internal_effect +
        mock_effect +
        assignment_effect +
        participation_effect +
        gpa_effect +
        prep_effect +
        family_effect +
        sleep_effect +
        health_effect +
        synergy_bonus +
        extra_effect
        - stress_penalty
        - internet_penalty
        - distraction_penalty
        - burnout_penalty
        - 15  # Intercept adjustment
    )
    
    # Add realistic noise (heteroscedastic - more variance in middle range)
    noise_scale = np.where(
        (base_score > 40) & (base_score < 85),
        6.0,
        3.5
    )
    noise = np.random.normal(0, noise_scale, n)
    
    final_marks = base_score + noise
    
    # Clip to valid range
    final_marks = np.clip(final_marks, 20, 100)
    
    return final_marks


def generate_dataset(n_samples=2000, output_path='dataset/dataset.csv'):
    """
    Generate complete dataset with all features.
    
    Args:
        n_samples: Number of samples to generate
        output_path: Path to save CSV file
    """
    print("=" * 70)
    print("ENHANCED DATASET GENERATION")
    print("=" * 70)
    print(f"\nGenerating {n_samples} student records with 16 features...")
    
    # Generate all features
    features = generate_correlated_features(n_samples)
    
    # Calculate final marks
    features['FinalMarks'] = calculate_final_marks(features)
    
    # Round all values appropriately
    for key in features:
        if key in ['ClassParticipation', 'StressLevel', 'FamilySupport', 'HealthScore']:
            # Integer scales
            features[key] = np.round(features[key], 0).astype(int)
        else:
            # One decimal place
            features[key] = np.round(features[key], 1)
    
    # Create DataFrame with specific column order
    column_order = [
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
        'ExtracurricularActivity',
        'FinalMarks'
    ]
    
    df = pd.DataFrame({col: features[col] for col in column_order})
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Dataset saved to: {output_path}")
    
    # Print statistics
    print("\n" + "=" * 70)
    print("DATASET STATISTICS")
    print("=" * 70)
    print(df.describe())
    
    print("\n" + "=" * 70)
    print("FEATURE CORRELATIONS WITH FINAL MARKS")
    print("=" * 70)
    correlations = df.corr()['FinalMarks'].sort_values(ascending=False)
    print(correlations)
    
    print("\n" + "=" * 70)
    print("SAMPLE RECORDS")
    print("=" * 70)
    print(df.head(10))
    
    print("\n✓ Dataset generation complete!")
    
    return df


if __name__ == "__main__":
    # Generate dataset
    dataset = generate_dataset(
        n_samples=Config.DATASET_SIZE,
        output_path=Config.DATASET_PATH
    )
