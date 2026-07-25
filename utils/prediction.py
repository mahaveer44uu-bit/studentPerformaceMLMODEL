"""
Prediction Engine Module
========================
Handles model loading, prediction, and explainability.

Author: AI-Based Student Performance Prediction Team
"""

import joblib
import json
import os
import numpy as np
from typing import Dict, List, Tuple, Any


class PredictionEngine:
    """
    Manages ML model loading, predictions, and explanations.
    
    Provides methods for making predictions, calculating confidence,
    and generating explainable AI insights.
    """
    
    def __init__(self, model_path: str, metadata_path: str = None, 
                 scaler_path: str = None):
        """
        Initialize prediction engine.
        
        Args:
            model_path: Path to trained model file
            metadata_path: Path to model metadata JSON
            scaler_path: Path to feature scaler (if used)
        """
        self.model_path = model_path
        self.metadata_path = metadata_path
        self.scaler_path = scaler_path
        
        self.model = None
        self.scaler = None
        self.metadata = {}
        self.feature_names = []
        
        self.load_model()
        self.load_metadata()
        if scaler_path and os.path.exists(scaler_path):
            self.load_scaler()
    
    def load_model(self):
        """Load trained model from disk."""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"✓ Model loaded from {self.model_path}")
            else:
                print(f"⚠ Model file not found: {self.model_path}")
                self.model = None
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            self.model = None
    
    def load_scaler(self):
        """Load feature scaler from disk."""
        try:
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                print(f"✓ Scaler loaded from {self.scaler_path}")
        except Exception as e:
            print(f"⚠ Error loading scaler: {e}")
            self.scaler = None
    
    def load_metadata(self):
        """Load model metadata (metrics, feature names, etc.)."""
        try:
            if self.metadata_path and os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                    self.feature_names = self.metadata.get('feature_names', [])
                print(f"✓ Metadata loaded from {self.metadata_path}")
            else:
                # Default metadata if file doesn't exist
                self.metadata = {
                    'model_name': 'Unknown',
                    'r2_score': 0.0,
                    'mae': 0.0,
                    'rmse': 0.0
                }
        except Exception as e:
            print(f"⚠ Error loading metadata: {e}")
            self.metadata = {}
    
    def predict(self, features: List[float]) -> float:
        """
        Make prediction for given features.
        
        Args:
            features: List of feature values
        
        Returns:
            Predicted marks (0-100)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Cannot make predictions.")
        
        try:
            # Convert to numpy array
            X = np.array(features).reshape(1, -1)
            
            # Apply scaling if scaler exists
            if self.scaler is not None:
                X = self.scaler.transform(X)
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            
            # Ensure prediction is within valid range
            prediction = max(0, min(100, prediction))
            
            return round(float(prediction), 2)
            
        except Exception as e:
            raise ValueError(f"Prediction failed: {e}")
    
    def predict_with_confidence(self, features: List[float]) -> Dict[str, float]:
        """
        Make prediction with confidence interval.
        
        Args:
            features: List of feature values
        
        Returns:
            Dictionary with prediction and confidence metrics
        """
        prediction = self.predict(features)
        
        # Calculate confidence based on model metrics
        # Higher R² score = higher confidence
        r2_score = self.metadata.get('r2_score', 0.75)
        mae = self.metadata.get('mae', 5.0)
        
        # Confidence percentage (simplified)
        confidence = min(95, max(60, r2_score * 100))
        
        # Prediction interval (simplified)
        lower_bound = max(0, prediction - mae * 1.5)
        upper_bound = min(100, prediction + mae * 1.5)
        
        return {
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'lower_bound': round(lower_bound, 2),
            'upper_bound': round(upper_bound, 2),
            'margin_of_error': round(mae * 1.5, 2)
        }
    
    def explain_prediction(self, features: List[float], 
                          feature_names: List[str] = None) -> Dict[str, Any]:
        """
        Generate explanation for prediction using feature importance.
        
        Args:
            features: List of feature values
            feature_names: Names of features (optional)
        
        Returns:
            Dictionary with explanation details
        """
        if feature_names is None:
            feature_names = self.feature_names
        
        if not feature_names:
            feature_names = [f"Feature_{i}" for i in range(len(features))]
        
        # Get feature importance from model if available
        feature_importance = self._get_feature_importance()
        
        # Create feature contributions
        contributions = []
        for i, (name, value) in enumerate(zip(feature_names, features)):
            importance = feature_importance[i] if i < len(feature_importance) else 0
            
            contributions.append({
                'feature': name,
                'value': round(value, 2),
                'importance': round(importance * 100, 2),
                'impact': self._assess_feature_impact(name, value)
            })
        
        # Sort by importance
        contributions.sort(key=lambda x: x['importance'], reverse=True)
        
        # Get top 5 most important features
        top_features = contributions[:5]
        
        # Generate natural language explanation
        explanation_text = self._generate_explanation_text(top_features)
        
        return {
            'top_features': top_features,
            'all_contributions': contributions,
            'explanation_text': explanation_text
        }
    
    def _get_feature_importance(self) -> List[float]:
        """
        Extract feature importance from model.
        
        Returns:
            List of importance scores
        """
        if self.model is None:
            return []
        
        try:
            # Try to get feature importance (works for tree-based models)
            if hasattr(self.model, 'feature_importances_'):
                return self.model.feature_importances_.tolist()
            
            # For linear models, use absolute coefficients
            elif hasattr(self.model, 'coef_'):
                coef = np.abs(self.model.coef_)
                # Normalize to sum to 1
                return (coef / coef.sum()).tolist()
            
            else:
                # Return uniform importance if not available
                n_features = len(self.feature_names) if self.feature_names else 4
                return [1.0 / n_features] * n_features
        
        except:
            return []
    
    def _assess_feature_impact(self, feature_name: str, value: float) -> str:
        """
        Assess impact of a feature value.
        
        Args:
            feature_name: Name of the feature
            value: Feature value
        
        Returns:
            Impact assessment string
        """
        # Simple heuristic-based assessment
        if 'StudyHours' in feature_name:
            if value >= 7:
                return 'Positive (High study time)'
            elif value >= 5:
                return 'Neutral'
            else:
                return 'Negative (Low study time)'
        
        elif 'Attendance' in feature_name:
            if value >= 80:
                return 'Positive (Good attendance)'
            elif value >= 70:
                return 'Neutral'
            else:
                return 'Negative (Poor attendance)'
        
        elif 'Sleep' in feature_name:
            if 6 <= value <= 8:
                return 'Positive (Optimal sleep)'
            else:
                return 'Negative (Non-optimal sleep)'
        
        elif 'Previous' in feature_name or 'Mock' in feature_name:
            if value >= 80:
                return 'Positive (Strong foundation)'
            elif value >= 60:
                return 'Neutral'
            else:
                return 'Negative (Weak foundation)'
        
        else:
            return 'Moderate impact'
    
    def _generate_explanation_text(self, top_features: List[Dict]) -> str:
        """
        Generate natural language explanation.
        
        Args:
            top_features: List of top contributing features
        
        Returns:
            Human-readable explanation string
        """
        if not top_features:
            return "Prediction based on provided inputs."
        
        # Get the most important feature
        most_important = top_features[0]
        
        explanation = f"The prediction is primarily influenced by {most_important['feature']} "
        explanation += f"(importance: {most_important['importance']:.1f}%). "
        
        # Add impact assessment
        explanation += f"This feature has a {most_important['impact'].split('(')[0].strip().lower()} impact. "
        
        # Mention second most important if available
        if len(top_features) > 1:
            second = top_features[1]
            explanation += f"Additionally, {second['feature']} "
            explanation += f"(importance: {second['importance']:.1f}%) also plays a significant role."
        
        return explanation
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and metadata.
        
        Returns:
            Dictionary with model details
        """
        return {
            'model_name': self.metadata.get('model_name', 'Unknown'),
            'model_type': self.metadata.get('model_type', 'Unknown'),
            'r2_score': self.metadata.get('r2_score', 0.0),
            'mae': self.metadata.get('mae', 0.0),
            'rmse': self.metadata.get('rmse', 0.0),
            'training_date': self.metadata.get('training_date', 'Unknown'),
            'dataset_size': self.metadata.get('dataset_size', 'Unknown'),
            'n_features': self.metadata.get('n_features', len(self.feature_names))
        }
