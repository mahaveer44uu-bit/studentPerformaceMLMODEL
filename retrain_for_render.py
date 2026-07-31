"""
Retrain model with Render-compatible packages
This will create a new student_model.pkl compatible with Python 3.9
"""

import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

print("=" * 60)
print("🔄 RETRAINING MODEL FOR RENDER DEPLOYMENT")
print("=" * 60)

# Load dataset
print("\n📊 Loading dataset...")
df = pd.read_csv('dataset.csv')
print(f"✓ Dataset loaded: {len(df)} rows")

# Prepare features
X = df[['StudyHours', 'Attendance', 'PreviousMarks', 'SleepHours']]
y = df['FinalMarks']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n🤖 Training Gradient Boosting model...")
model = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"✓ Model trained! R² Score: {score:.4f} ({score*100:.2f}%)")

# Save with protocol 4 (compatible with Python 3.4+)
print("\n💾 Saving model (protocol=4 for compatibility)...")
joblib.dump(model, 'student_model.pkl', protocol=4)

print("✓ Model saved successfully!")
print("\n" + "=" * 60)
print("✅ DONE! Your model is now Render-compatible!")
print("=" * 60)
print("\nNext steps:")
print("1. Run: git add student_model.pkl")
print("2. Run: git commit -m 'Update model for Render compatibility'")
print("3. Run: git push origin main")
print("4. Render will auto-deploy!")
