import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    root_mean_squared_error
)

# ==========================
# Load Dataset
# ==========================
data = pd.read_csv("dataset.csv")

X = data[["StudyHours", "Attendance", "PreviousMarks", "SleepHours"]]
y = data["FinalMarks"]

# ==========================
# Train Test Split
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================
# Models
# ==========================
models = {
    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
}

best_model = None
best_score = -999
best_name = ""

print("\n" + "="*55)
print("MODEL COMPARISON")
print("="*55)

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    r2 = r2_score(y_test, prediction)
    mae = mean_absolute_error(y_test, prediction)
    rmse = root_mean_squared_error(y_test, prediction)

    print(f"\n{name}")
    print("-"*35)
    print(f"R² Score : {r2:.4f}")
    print(f"MAE      : {mae:.4f}")
    print(f"RMSE     : {rmse:.4f}")

    if r2 > best_score:
        best_score = r2
        best_model = model
        best_name = name

# ==========================
# Save Best Model
# ==========================

joblib.dump(best_model, "student_model.pkl")

print("\n" + "="*55)
print("BEST MODEL")
print("="*55)

print(f"Model Name : {best_name}")
print(f"R² Score   : {best_score:.4f}")

print("\nBest model saved successfully as student_model.pkl")