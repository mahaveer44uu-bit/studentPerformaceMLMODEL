"""
ADVANCED MODEL TRAINING SCRIPT
- 5000 rows dataset
- Multiple ML algorithms
- Hyperparameter tuning
- Cross-validation
- Best model selection
- Detailed metrics
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🚀 ADVANCED MODEL TRAINING - 5000 ROWS DATASET")
print("="*80)

# ========================================
# STEP 1: GENERATE 5000 ROWS DATASET
# ========================================
print("\n📊 Step 1: Generating 5000 rows dataset...")

np.random.seed(42)
N = 5000
rows = []

for _ in range(N):
    # Previous marks: students vary widely
    previous = np.clip(np.random.normal(65, 15), 30, 98)
    
    # Attendance correlates slightly with previous performance
    attendance = np.clip(
        np.random.normal(70 + 0.15 * (previous - 65), 12), 45, 100
    )
    
    # Study hours: mostly independent
    study = np.clip(np.random.normal(5 + 0.02 * (previous - 65), 2.2), 0.5, 15)
    
    # Sleep hours: independent
    sleep = np.clip(np.random.normal(7, 1.2), 4, 10)
    
    # Final marks calculation with realistic relationships
    final = (
        0.35 * previous +           # Strong weight on previous performance
        0.30 * attendance +          # Attendance matters
        3.5 * study +                # Study hours have good impact
        1.5 * sleep +                # Sleep helps a bit
        np.random.normal(0, 4)       # Natural variation
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

# Save dataset
df.to_csv("dataset/dataset_5000.csv", index=False)
print(f"✅ Generated {len(df)} rows")
print(f"✅ Saved to: dataset/dataset_5000.csv")

# Dataset statistics
print(f"\n📈 Dataset Statistics:")
print(df.describe().round(2))

# ========================================
# STEP 2: PREPARE DATA
# ========================================
print("\n🔧 Step 2: Preparing data...")

X = df[["StudyHours", "Attendance", "PreviousMarks", "SleepHours"]]
y = df["FinalMarks"]

# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")

# ========================================
# STEP 3: TRAIN MULTIPLE MODELS
# ========================================
print("\n🤖 Step 3: Training multiple ML models...")
print("-"*80)

models = {}
results = []

# Model 1: Linear Regression
print("\n1️⃣  Training Linear Regression...")
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
r2_lr = r2_score(y_test, y_pred_lr)
mae_lr = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
cv_lr = cross_val_score(lr, X_train, y_train, cv=5, scoring='r2').mean()

models['Linear Regression'] = lr
results.append({
    'Model': 'Linear Regression',
    'R²': r2_lr,
    'MAE': mae_lr,
    'RMSE': rmse_lr,
    'CV_R²': cv_lr
})
print(f"   R² Score: {r2_lr:.4f}")
print(f"   MAE: {mae_lr:.4f}")
print(f"   RMSE: {rmse_lr:.4f}")
print(f"   Cross-Val R²: {cv_lr:.4f}")

# Model 2: Ridge Regression (with tuning)
print("\n2️⃣  Training Ridge Regression (with hyperparameter tuning)...")
ridge_params = {'alpha': [0.1, 1, 10, 100]}
ridge = GridSearchCV(Ridge(), ridge_params, cv=5, scoring='r2')
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)
r2_ridge = r2_score(y_test, y_pred_ridge)
mae_ridge = mean_absolute_error(y_test, y_pred_ridge)
rmse_ridge = np.sqrt(mean_squared_error(y_test, y_pred_ridge))

models['Ridge Regression'] = ridge
results.append({
    'Model': 'Ridge Regression',
    'R²': r2_ridge,
    'MAE': mae_ridge,
    'RMSE': rmse_ridge,
    'CV_R²': ridge.best_score_,
    'Best_Params': ridge.best_params_
})
print(f"   Best Alpha: {ridge.best_params_['alpha']}")
print(f"   R² Score: {r2_ridge:.4f}")
print(f"   MAE: {mae_ridge:.4f}")
print(f"   RMSE: {rmse_ridge:.4f}")

# Model 3: Lasso Regression (with tuning)
print("\n3️⃣  Training Lasso Regression (with hyperparameter tuning)...")
lasso_params = {'alpha': [0.1, 1, 10, 100]}
lasso = GridSearchCV(Lasso(), lasso_params, cv=5, scoring='r2')
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)
r2_lasso = r2_score(y_test, y_pred_lasso)
mae_lasso = mean_absolute_error(y_test, y_pred_lasso)
rmse_lasso = np.sqrt(mean_squared_error(y_test, y_pred_lasso))

models['Lasso Regression'] = lasso
results.append({
    'Model': 'Lasso Regression',
    'R²': r2_lasso,
    'MAE': mae_lasso,
    'RMSE': rmse_lasso,
    'CV_R²': lasso.best_score_,
    'Best_Params': lasso.best_params_
})
print(f"   Best Alpha: {lasso.best_params_['alpha']}")
print(f"   R² Score: {r2_lasso:.4f}")
print(f"   MAE: {mae_lasso:.4f}")

# Model 4: Decision Tree (with tuning)
print("\n4️⃣  Training Decision Tree (with hyperparameter tuning)...")
dt_params = {
    'max_depth': [5, 10, 15, 20],
    'min_samples_split': [2, 5, 10]
}
dt = GridSearchCV(DecisionTreeRegressor(random_state=42), dt_params, cv=5, scoring='r2')
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
r2_dt = r2_score(y_test, y_pred_dt)
mae_dt = mean_absolute_error(y_test, y_pred_dt)
rmse_dt = np.sqrt(mean_squared_error(y_test, y_pred_dt))

models['Decision Tree'] = dt
results.append({
    'Model': 'Decision Tree',
    'R²': r2_dt,
    'MAE': mae_dt,
    'RMSE': rmse_dt,
    'CV_R²': dt.best_score_,
    'Best_Params': dt.best_params_
})
print(f"   Best Params: {dt.best_params_}")
print(f"   R² Score: {r2_dt:.4f}")
print(f"   MAE: {mae_dt:.4f}")

# Model 5: Random Forest (with tuning)
print("\n5️⃣  Training Random Forest (with hyperparameter tuning)...")
rf_params = {
    'n_estimators': [100, 200],
    'max_depth': [10, 15, 20],
    'min_samples_split': [2, 5]
}
rf = GridSearchCV(
    RandomForestRegressor(random_state=42), 
    rf_params, 
    cv=3,  # Reduced CV for speed
    scoring='r2',
    n_jobs=-1
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
r2_rf = r2_score(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

models['Random Forest'] = rf
results.append({
    'Model': 'Random Forest',
    'R²': r2_rf,
    'MAE': mae_rf,
    'RMSE': rmse_rf,
    'CV_R²': rf.best_score_,
    'Best_Params': rf.best_params_
})
print(f"   Best Params: {rf.best_params_}")
print(f"   R² Score: {r2_rf:.4f}")
print(f"   MAE: {mae_rf:.4f}")

# Model 6: Gradient Boosting (with tuning)
print("\n6️⃣  Training Gradient Boosting (with hyperparameter tuning)...")
gb_params = {
    'n_estimators': [100, 200],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 5]
}
gb = GridSearchCV(
    GradientBoostingRegressor(random_state=42),
    gb_params,
    cv=3,
    scoring='r2',
    n_jobs=-1
)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
r2_gb = r2_score(y_test, y_pred_gb)
mae_gb = mean_absolute_error(y_test, y_pred_gb)
rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))

models['Gradient Boosting'] = gb
results.append({
    'Model': 'Gradient Boosting',
    'R²': r2_gb,
    'MAE': mae_gb,
    'RMSE': rmse_gb,
    'CV_R²': gb.best_score_,
    'Best_Params': gb.best_params_
})
print(f"   Best Params: {gb.best_params_}")
print(f"   R² Score: {r2_gb:.4f}")
print(f"   MAE: {mae_gb:.4f}")

# ========================================
# STEP 4: COMPARE MODELS
# ========================================
print("\n" + "="*80)
print("📊 MODEL COMPARISON")
print("="*80)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('R²', ascending=False)

print("\n🏆 Models Ranked by R² Score:")
print(results_df[['Model', 'R²', 'MAE', 'RMSE']].to_string(index=False))

# ========================================
# STEP 5: SELECT BEST MODEL
# ========================================
print("\n" + "="*80)
print("🏆 BEST MODEL SELECTION")
print("="*80)

best_model_name = results_df.iloc[0]['Model']
best_r2 = results_df.iloc[0]['R²']
best_mae = results_df.iloc[0]['MAE']
best_rmse = results_df.iloc[0]['RMSE']

print(f"\n✨ Best Model: {best_model_name}")
print(f"   R² Score: {best_r2:.4f} ({best_r2*100:.2f}%)")
print(f"   MAE: {best_mae:.4f}")
print(f"   RMSE: {best_rmse:.4f}")

# ========================================
# STEP 6: SAVE BEST MODEL
# ========================================
print("\n💾 Saving best model...")

best_model = models[best_model_name]

# Save to models folder
joblib.dump(best_model, "models/student_model.pkl")
print(f"✅ Saved to: models/student_model.pkl")

# Also save with specific name
model_filename = f"models/best_model_{best_model_name.lower().replace(' ', '_')}.pkl"
joblib.dump(best_model, model_filename)
print(f"✅ Backup saved to: {model_filename}")

# Save model info
model_info = {
    'model_name': best_model_name,
    'r2_score': float(best_r2),
    'mae': float(best_mae),
    'rmse': float(best_rmse),
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'features': list(X.columns),
    'dataset_rows': N
}

import json
with open('models/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=4)
print(f"✅ Model info saved to: models/model_info.json")

# ========================================
# STEP 7: FEATURE IMPORTANCE
# ========================================
print("\n" + "="*80)
print("📈 FEATURE IMPORTANCE")
print("="*80)

if hasattr(best_model.best_estimator_ if hasattr(best_model, 'best_estimator_') else best_model, 'feature_importances_'):
    feature_model = best_model.best_estimator_ if hasattr(best_model, 'best_estimator_') else best_model
    importances = feature_model.feature_importances_
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print("\n🎯 Feature Importance:")
    for idx, row in feature_importance.iterrows():
        print(f"   {row['Feature']}: {row['Importance']:.4f} ({row['Importance']*100:.2f}%)")
    
    # Save feature importance
    feature_importance.to_csv('models/feature_importance.csv', index=False)
    print(f"\n✅ Feature importance saved to: models/feature_importance.csv")
elif hasattr(best_model.best_estimator_ if hasattr(best_model, 'best_estimator_') else best_model, 'coef_'):
    coef_model = best_model.best_estimator_ if hasattr(best_model, 'best_estimator_') else best_model
    coefficients = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': coef_model.coef_
    }).sort_values('Coefficient', ascending=False)
    
    print("\n📊 Model Coefficients:")
    for idx, row in coefficients.iterrows():
        print(f"   {row['Feature']}: {row['Coefficient']:.4f}")

# ========================================
# STEP 8: TEST PREDICTION
# ========================================
print("\n" + "="*80)
print("🧪 TEST PREDICTION")
print("="*80)

# Test with sample data
test_sample = [[6, 85, 75, 7]]  # Study, Attendance, Previous, Sleep
prediction = best_model.predict(test_sample)[0]

print(f"\n📝 Sample Input:")
print(f"   Study Hours: 6")
print(f"   Attendance: 85%")
print(f"   Previous Marks: 75")
print(f"   Sleep Hours: 7")
print(f"\n🎯 Predicted Final Marks: {prediction:.2f}")

# ========================================
# FINAL SUMMARY
# ========================================
print("\n" + "="*80)
print("✅ TRAINING COMPLETE!")
print("="*80)

print(f"\n📊 Summary:")
print(f"   ✅ Dataset: 5000 rows")
print(f"   ✅ Models Trained: 6")
print(f"   ✅ Best Model: {best_model_name}")
print(f"   ✅ Accuracy: {best_r2*100:.2f}%")
print(f"   ✅ Saved: models/student_model.pkl")

print(f"\n🎉 Your app will now use the BEST model!")
print(f"\n💡 Run your app: python app.py")

print("\n" + "="*80)
