import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000
rows = []

for _ in range(N):
    # ---- Base (somewhat correlated) features, like real students ----
    # Previous marks: students vary widely
    previous = np.clip(np.random.normal(65, 15), 30, 98)

    # Attendance tends to be a bit higher for students who scored well before,
    # but with plenty of individual variation (not a strict rule)
    attendance = np.clip(
        np.random.normal(70 + 0.15 * (previous - 65), 12), 45, 100
    )

    # Study hours: mostly independent, slightly higher for sincere students
    study = np.clip(np.random.normal(5 + 0.02 * (previous - 65), 2.2), 0.5, 10)

    # Sleep hours: students who study a lot late into the night sleep a bit less
    sleep = np.clip(np.random.normal(7 - 0.15 * max(study - 5, 0), 1.3), 3, 10)

    # ---- Non-linear effects (diminishing returns + fatigue penalty) ----
    study_effect = 9 * np.sqrt(study)  # diminishing returns after ~6-7 hrs
    attendance_effect = 0.32 * attendance
    previous_effect = 0.42 * previous

    # Sleep has an ideal zone (7-8 hrs); too little OR too much hurts a bit
    sleep_effect = -0.9 * (sleep - 7.5) ** 2 + 8

    # Fatigue interaction: long study hours with too little sleep hurts more
    # than either factor alone (realistic "burnout" pattern)
    fatigue_penalty = 0
    if study > 7 and sleep < 6:
        fatigue_penalty = 3.5

    base = (
        study_effect
        + attendance_effect
        + previous_effect
        + sleep_effect
        - fatigue_penalty
        - 7  # intercept adjustment
    )

    # Heteroscedastic noise: mid-range scores are noisier than very
    # high/low ones (real exam variability)
    noise_scale = 5.5 if 40 < base < 85 else 3.0
    noise = np.random.normal(0, noise_scale)

    final = np.clip(round(base + noise, 1), 20, 100)

    rows.append([
        round(study, 1),
        round(attendance, 1),
        round(previous, 1),
        round(sleep, 1),
        final,
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "StudyHours",
        "Attendance",
        "PreviousMarks",
        "SleepHours",
        "FinalMarks",
    ],
)

df.to_csv("dataset.csv", index=False)

print("dataset.csv created successfully!")
print(df.describe())