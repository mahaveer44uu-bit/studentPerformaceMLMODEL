"""
MODEL ACCURACY TESTER
- Tests current model on various data
- Shows accuracy metrics
- Generates test report
- Compares predictions vs actual
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import os

print("="*80)
print("🧪 MODEL ACCURACY TESTING")
print("="*80)

# ========================================
# STEP 1: LOAD MODEL
# ========================================
print("\n📦 Step 1: Loading model...")

model_path = "models/student_model.pkl"

if not os.path.exists(model_path):
    # Try alternate location
    if os.path.exists("student_model.pkl"):
        model_path = "student_model.pkl"
    else:
        print("❌ Error: Model file not found!")
        print("   Looking for: models/student_model.pkl")
        print("\n💡 Please train the model first:")
        print("   → Double-click: TRAIN_BEST_MODEL.bat")
        exit()

try:
    model = joblib.load(model_path)
    print(f"✅ Model loaded from: {model_path}")
    
    # Check model type
    model_name = type(model).__name__
    if hasattr(model, 'best_estimator_'):
        model_name = type(model.best_estimator_).__name__
    print(f"   Model Type: {model_name}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit()

# ========================================
# STEP 2: LOAD OR GENERATE TEST DATA
# ========================================
print("\n📊 Step 2: Preparing test data...")

# Try to load existing dataset
dataset_path = None
for path in ["dataset.csv", "dataset/dataset.csv", "dataset/dataset_5000.csv"]:
    if os.path.exists(path):
        dataset_path = path
        break

if dataset_path:
    print(f"   Loading existing dataset: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"✅ Loaded {len(df)} records")
else:
    print("   No dataset found. Generating 1000 test records...")
    np.random.seed(99)  # Different seed for testing
    N = 1000
    rows = []
    
    for _ in range(N):
        previous = np.clip(np.random.normal(65, 15), 30, 98)
        attendance = np.clip(np.random.normal(70 + 0.15 * (previous - 65), 12), 45, 100)
        study = np.clip(np.random.normal(5 + 0.02 * (previous - 65), 2.2), 0.5, 15)
        sleep = np.clip(np.random.normal(7, 1.2), 4, 10)
        
        final = (
            0.35 * previous +
            0.30 * attendance +
            3.5 * study +
            1.5 * sleep +
            np.random.normal(0, 4)
        )
        final = np.clip(final, 35, 98)
        
        rows.append({
            "StudyHours": round(study, 1),
            "Attendance": round(attendance, 1),
            "PreviousMarks": round(previous, 1),
            "SleepHours": round(sleep, 1),
            "FinalMarks": round(final, 1)
        })
    
    df = pd.DataFrame(rows)
    print(f"✅ Generated {len(df)} test records")

# Prepare features and target
X = df[["StudyHours", "Attendance", "PreviousMarks", "SleepHours"]]
y_true = df["FinalMarks"]

print(f"\n📈 Test Data Statistics:")
print(df.describe().round(2))

# ========================================
# STEP 3: MAKE PREDICTIONS
# ========================================
print("\n🔮 Step 3: Making predictions...")

try:
    y_pred = model.predict(X)
    print(f"✅ Generated {len(y_pred)} predictions")
except Exception as e:
    print(f"❌ Error making predictions: {e}")
    exit()

# ========================================
# STEP 4: CALCULATE ACCURACY METRICS
# ========================================
print("\n📊 Step 4: Calculating accuracy metrics...")
print("-"*80)

# R² Score (Coefficient of Determination)
r2 = r2_score(y_true, y_pred)
print(f"\n🎯 R² Score (Accuracy): {r2:.4f} ({r2*100:.2f}%)")
print(f"   → Explains {r2*100:.2f}% of variance")
print(f"   → Higher is better (max 100%)")

# Mean Absolute Error
mae = mean_absolute_error(y_true, y_pred)
print(f"\n📏 Mean Absolute Error (MAE): {mae:.4f}")
print(f"   → Average error: ±{mae:.2f} marks")
print(f"   → Lower is better")

# Root Mean Squared Error
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
print(f"\n📐 Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"   → Typical error: ±{rmse:.2f} marks")
print(f"   → Penalizes large errors more")

# Mean Absolute Percentage Error
mape = mean_absolute_percentage_error(y_true, y_pred) * 100
print(f"\n📊 Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
print(f"   → Average percentage error: {mape:.2f}%")
print(f"   → Lower is better")

# Max Error
max_error = np.max(np.abs(y_true - y_pred))
print(f"\n⚠️  Maximum Error: {max_error:.2f} marks")
print(f"   → Worst prediction was off by {max_error:.2f} marks")

# ========================================
# STEP 5: DETAILED ANALYSIS
# ========================================
print("\n" + "="*80)
print("📈 DETAILED ANALYSIS")
print("="*80)

# Create comparison dataframe
comparison = pd.DataFrame({
    'Actual': y_true,
    'Predicted': y_pred,
    'Error': y_true - y_pred,
    'Abs_Error': np.abs(y_true - y_pred)
})

# Error distribution
print("\n📊 Error Distribution:")
print(f"   Errors within ±2 marks: {(comparison['Abs_Error'] <= 2).sum()} ({(comparison['Abs_Error'] <= 2).sum()/len(comparison)*100:.1f}%)")
print(f"   Errors within ±3 marks: {(comparison['Abs_Error'] <= 3).sum()} ({(comparison['Abs_Error'] <= 3).sum()/len(comparison)*100:.1f}%)")
print(f"   Errors within ±5 marks: {(comparison['Abs_Error'] <= 5).sum()} ({(comparison['Abs_Error'] <= 5).sum()/len(comparison)*100:.1f}%)")
print(f"   Errors within ±10 marks: {(comparison['Abs_Error'] <= 10).sum()} ({(comparison['Abs_Error'] <= 10).sum()/len(comparison)*100:.1f}%)")

# Best and worst predictions
print("\n🏆 Best Predictions (Smallest Errors):")
best = comparison.nsmallest(5, 'Abs_Error')
for idx, row in best.iterrows():
    print(f"   Actual: {row['Actual']:.1f}, Predicted: {row['Predicted']:.1f}, Error: {row['Error']:+.2f}")

print("\n⚠️  Worst Predictions (Largest Errors):")
worst = comparison.nlargest(5, 'Abs_Error')
for idx, row in worst.iterrows():
    print(f"   Actual: {row['Actual']:.1f}, Predicted: {row['Predicted']:.1f}, Error: {row['Error']:+.2f}")

# ========================================
# STEP 6: SAMPLE PREDICTIONS
# ========================================
print("\n" + "="*80)
print("🧪 SAMPLE PREDICTIONS")
print("="*80)

# Test with specific examples
test_cases = [
    {
        'name': 'Excellent Student',
        'data': [[10, 95, 90, 8]],
        'expected': '~92'
    },
    {
        'name': 'Good Student',
        'data': [[6, 85, 75, 7]],
        'expected': '~78'
    },
    {
        'name': 'Average Student',
        'data': [[4, 70, 60, 6]],
        'expected': '~65'
    },
    {
        'name': 'Struggling Student',
        'data': [[2, 55, 45, 5]],
        'expected': '~50'
    },
    {
        'name': 'Low Sleep Impact',
        'data': [[7, 80, 70, 4]],  # Low sleep
        'expected': '~72'
    },
    {
        'name': 'High Study Impact',
        'data': [[12, 80, 70, 7]],  # High study
        'expected': '~78'
    }
]

print("\n📝 Testing various student profiles:\n")

for i, test in enumerate(test_cases, 1):
    pred = model.predict(test['data'])[0]
    features = test['data'][0]
    print(f"{i}. {test['name']}:")
    print(f"   Input: Study={features[0]}hrs, Attendance={features[1]}%, Previous={features[2]}, Sleep={features[3]}hrs")
    print(f"   Predicted: {pred:.2f} marks (Expected: {test['expected']})")
    print()

# ========================================
# STEP 7: MODEL QUALITY ASSESSMENT
# ========================================
print("="*80)
print("🎓 MODEL QUALITY ASSESSMENT")
print("="*80)

print(f"\n📊 Overall Performance:")

if r2 >= 0.90:
    quality = "EXCELLENT ⭐⭐⭐⭐⭐"
    description = "Outstanding! Model explains >90% of variance."
elif r2 >= 0.85:
    quality = "VERY GOOD ⭐⭐⭐⭐"
    description = "Great performance! Model is highly reliable."
elif r2 >= 0.80:
    quality = "GOOD ⭐⭐⭐"
    description = "Solid performance! Model is reliable for predictions."
elif r2 >= 0.75:
    quality = "ACCEPTABLE ⭐⭐"
    description = "Decent performance. Can be improved with more data/tuning."
else:
    quality = "NEEDS IMPROVEMENT ⭐"
    description = "Model needs better training or more features."

print(f"   Quality Rating: {quality}")
print(f"   {description}")

print(f"\n💡 Accuracy Interpretation:")
print(f"   → Your model is accurate within ±{mae:.1f} marks on average")
print(f"   → {r2*100:.1f}% of predictions are explained by the model")
print(f"   → Typical prediction error: ±{rmse:.1f} marks")

# ========================================
# STEP 8: SAVE REPORT
# ========================================
print("\n💾 Saving test report...")

report = f"""
MODEL ACCURACY TEST REPORT
{'='*80}

Test Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
Model Path: {model_path}
Model Type: {model_name}

DATASET INFORMATION
{'='*80}
Test Samples: {len(df)}
Features: StudyHours, Attendance, PreviousMarks, SleepHours
Target: FinalMarks

ACCURACY METRICS
{'='*80}
R² Score (Accuracy):        {r2:.4f} ({r2*100:.2f}%)
Mean Absolute Error (MAE):  {mae:.4f} marks
Root Mean Squared Error:    {rmse:.4f} marks
Mean Absolute % Error:      {mape:.2f}%
Maximum Error:              {max_error:.2f} marks

ERROR DISTRIBUTION
{'='*80}
Within ±2 marks:  {(comparison['Abs_Error'] <= 2).sum()} ({(comparison['Abs_Error'] <= 2).sum()/len(comparison)*100:.1f}%)
Within ±3 marks:  {(comparison['Abs_Error'] <= 3).sum()} ({(comparison['Abs_Error'] <= 3).sum()/len(comparison)*100:.1f}%)
Within ±5 marks:  {(comparison['Abs_Error'] <= 5).sum()} ({(comparison['Abs_Error'] <= 5).sum()/len(comparison)*100:.1f}%)
Within ±10 marks: {(comparison['Abs_Error'] <= 10).sum()} ({(comparison['Abs_Error'] <= 10).sum()/len(comparison)*100:.1f}%)

MODEL QUALITY
{'='*80}
Rating: {quality}
{description}

INTERPRETATION
{'='*80}
- Model accuracy: {r2*100:.1f}%
- Average error: ±{mae:.1f} marks
- Typical error: ±{rmse:.1f} marks

CONCLUSION
{'='*80}
The model {'performs well' if r2 >= 0.80 else 'needs improvement'} for predicting student performance.
Predictions are typically within ±{rmse:.1f} marks of actual results.
"""

with open('models/accuracy_report.txt', 'w') as f:
    f.write(report)

print("✅ Report saved to: models/accuracy_report.txt")

# Save detailed comparison
comparison.to_csv('models/predictions_comparison.csv', index=False)
print("✅ Detailed predictions saved to: models/predictions_comparison.csv")

# ========================================
# FINAL SUMMARY
# ========================================
print("\n" + "="*80)
print("✅ TESTING COMPLETE!")
print("="*80)

print(f"\n📊 Key Metrics:")
print(f"   ✅ R² Score: {r2*100:.2f}%")
print(f"   ✅ Average Error: ±{mae:.2f} marks")
print(f"   ✅ Quality: {quality}")

print(f"\n📁 Files Created:")
print(f"   ✅ models/accuracy_report.txt")
print(f"   ✅ models/predictions_comparison.csv")

print(f"\n💡 Next Steps:")
if r2 < 0.85:
    print(f"   → Train a better model: Double-click TRAIN_BEST_MODEL.bat")
    print(f"   → Expected improvement: Up to 89% accuracy!")
else:
    print(f"   → Your model is performing well!")
    print(f"   → Ready for demo and deployment!")

print("\n" + "="*80)
