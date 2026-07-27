"""
Train and evaluate student performance prediction models.

Compares multiple regressors with 5-fold cross-validation, tunes the top
candidates, and saves the best model for Flask (4 raw features, no scaler).
"""

import json
import os
import sys

import joblib
import pandas as pd
from sklearn.ensemble import (
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import GridSearchCV, KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
FEATURES = ["StudyHours", "Attendance", "PreviousMarks", "SleepHours"]
TARGET = "FinalMarks"
CV_FOLDS = 5
SCORING = {
    "r2": "r2",
    "neg_mae": "neg_mean_absolute_error",
    "neg_rmse": "neg_root_mean_squared_error",
}


def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _dataset_path():
    root = _project_root()
    for candidate in ("dataset.csv", os.path.join("dataset", "dataset.csv")):
        path = os.path.join(root, candidate)
        if os.path.exists(path):
            return path
    raise FileNotFoundError("dataset.csv not found in project root or dataset/")


def evaluate(model, X_train, X_test, y_train, y_test):
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    return {
        "train_r2": r2_score(y_train, train_pred),
        "test_r2": r2_score(y_test, test_pred),
        "train_mae": mean_absolute_error(y_train, train_pred),
        "test_mae": mean_absolute_error(y_test, test_pred),
        "train_rmse": root_mean_squared_error(y_train, train_pred),
        "test_rmse": root_mean_squared_error(y_test, test_pred),
        "r2_gap": r2_score(y_train, train_pred) - r2_score(y_test, test_pred),
    }


def run_cv(model, X, y):
    cv = KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_validate(
        model, X, y, cv=cv, scoring=SCORING, n_jobs=-1, return_train_score=True
    )
    return {
        "cv_test_r2_mean": scores["test_r2"].mean(),
        "cv_test_r2_std": scores["test_r2"].std(),
        "cv_test_mae_mean": -scores["test_neg_mae"].mean(),
        "cv_test_rmse_mean": -scores["test_neg_rmse"].mean(),
        "cv_train_test_r2_gap": scores["train_r2"].mean() - scores["test_r2"].mean(),
    }


def build_candidates():
    candidates = {
        "Linear Regression": Pipeline(
            [("scaler", StandardScaler()), ("model", LinearRegression())]
        ),
        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=5,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            random_state=RANDOM_STATE,
        ),
        "Extra Trees": ExtraTreesRegressor(
            n_estimators=300,
            max_depth=12,
            min_samples_leaf=5,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }
    try:
        from xgboost import XGBRegressor

        candidates["XGBoost"] = XGBRegressor(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
    except ImportError:
        print("XGBoost not installed; skipping.")
    return candidates


def tune_top_models(X_train, y_train, ranked_names):
    tuned = {}

    if "Random Forest" in ranked_names[:2]:
        search = GridSearchCV(
            RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
            {
                "n_estimators": [200, 400],
                "max_depth": [8, 12, None],
                "min_samples_leaf": [2, 5, 10],
                "max_features": ["sqrt", 0.8],
            },
            cv=CV_FOLDS,
            scoring="r2",
            n_jobs=-1,
        )
        search.fit(X_train, y_train)
        tuned["Random Forest"] = search

    if "Gradient Boosting" in ranked_names[:2]:
        search = GridSearchCV(
            GradientBoostingRegressor(random_state=RANDOM_STATE),
            {
                "n_estimators": [150, 250],
                "max_depth": [3, 4, 5],
                "learning_rate": [0.03, 0.05, 0.08],
                "subsample": [0.7, 0.85, 1.0],
                "min_samples_leaf": [5, 10, 20],
            },
            cv=CV_FOLDS,
            scoring="r2",
            n_jobs=-1,
        )
        search.fit(X_train, y_train)
        tuned["Gradient Boosting"] = search

    if "Extra Trees" in ranked_names[:2]:
        search = GridSearchCV(
            ExtraTreesRegressor(random_state=RANDOM_STATE, n_jobs=-1),
            {
                "n_estimators": [200, 400],
                "max_depth": [8, 12, None],
                "min_samples_leaf": [2, 5, 10],
                "max_features": ["sqrt", 0.8],
            },
            cv=CV_FOLDS,
            scoring="r2",
            n_jobs=-1,
        )
        search.fit(X_train, y_train)
        tuned["Extra Trees"] = search

    if "Linear Regression" in ranked_names[:2]:
        pipe = Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())])
        cv = KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
        scores = cross_validate(pipe, X_train, y_train, cv=cv, scoring="r2")
        tuned["Linear Regression"] = type(
            "LRResult",
            (),
            {"best_estimator_": pipe, "best_score_": scores["test_score"].mean(), "best_params_": {}},
        )()

    return tuned


def main():
    root = _project_root()
    os.chdir(root)

    data = pd.read_csv(_dataset_path())
    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    print("\n" + "=" * 60)
    print("5-FOLD CROSS-VALIDATION COMPARISON")
    print("=" * 60)

    candidates = build_candidates()
    cv_results = []
    for name, model in candidates.items():
        metrics = run_cv(model, X, y)
        cv_results.append({"model": name, **metrics})
        print(f"\n{name}")
        print("-" * 40)
        print(f"CV R²   : {metrics['cv_test_r2_mean']:.4f} (+/- {metrics['cv_test_r2_std']:.4f})")
        print(f"CV MAE  : {metrics['cv_test_mae_mean']:.4f}")
        print(f"CV RMSE : {metrics['cv_test_rmse_mean']:.4f}")
        print(f"Train/Test R² gap (CV): {metrics['cv_train_test_r2_gap']:.4f}")

    ranked = sorted(cv_results, key=lambda item: item["cv_test_r2_mean"], reverse=True)
    ranked_names = [item["model"] for item in ranked]

    print("\n" + "=" * 60)
    print("HYPERPARAMETER TUNING (TOP CANDIDATES)")
    print("=" * 60)

    tuned = tune_top_models(X_train, y_train, ranked_names)
    best_name = None
    best_score = -999
    best_model = None
    best_params = {}

    for name, search in tuned.items():
        holdout = evaluate(search.best_estimator_, X_train, X_test, y_train, y_test)
        adjusted = search.best_score_ - 0.05 * max(0, holdout["r2_gap"] - 0.02)
        print(f"\n{name}")
        print("-" * 40)
        print(f"Tuned CV R² : {search.best_score_:.4f}")
        print(f"Best params : {search.best_params_}")
        print(f"Holdout R²  : {holdout['test_r2']:.4f}")
        print(f"Holdout MAE : {holdout['test_mae']:.4f}")
        print(f"Holdout RMSE: {holdout['test_rmse']:.4f}")
        print(f"Train/Test R² gap: {holdout['r2_gap']:.4f}")
        if adjusted > best_score:
            best_score = adjusted
            best_name = name
            best_model = search.best_estimator_
            best_params = search.best_params_

    print("\n" + "=" * 60)
    print("FINAL MODEL")
    print("=" * 60)
    print(f"Selected   : {best_name}")
    print(f"Tuned CV R²: {best_score:.4f}")
    print(f"Params     : {best_params}")

    holdout = evaluate(best_model, X_train, X_test, y_train, y_test)
    print(f"Holdout R² : {holdout['test_r2']:.4f}")
    print(f"Holdout MAE: {holdout['test_mae']:.4f}")
    print(f"Holdout RMSE: {holdout['test_rmse']:.4f}")

    best_model.fit(X, y)

    models_dir = os.path.join(root, "models")
    os.makedirs(models_dir, exist_ok=True)
    model_paths = [
        os.path.join(models_dir, "student_model.pkl"),
        os.path.join(root, "student_model.pkl"),
    ]
    for path in model_paths:
        joblib.dump(best_model, path)
        print(f"Saved model -> {path}")

    metadata = {
        "model_name": best_name,
        "best_params": best_params,
        "feature_names": FEATURES,
        "cv_results": cv_results,
        "holdout_metrics": holdout,
        "tuned_cv_r2": best_score,
    }
    metadata_path = os.path.join(models_dir, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata -> {metadata_path}")


if __name__ == "__main__":
    main()
