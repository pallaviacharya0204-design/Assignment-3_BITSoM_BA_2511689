import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

# ─────────────────────────────────────────────────────────────
# TASK 1 — DATA EXPLORATION WITH PANDAS
# ─────────────────────────────────────────────────────────────
print("=" * 65)
print("TASK 1 — DATA EXPLORATION WITH PANDAS")
print("=" * 65)

df = pd.read_csv("students.csv")
subject_cols = ['math', 'science', 'english', 'history', 'pe']

# 1. First 5 rows
print("\n── 1. First 5 rows ──")
print(df.head().to_string(index=False))

# 2. Shape and dtypes
print(f"\n── 2. Shape: {df.shape[0]} rows × {df.shape[1]} columns ──")
print(df.dtypes.to_string())

# 3. Summary statistics
print("\n── 3. Summary Statistics ──")
print(df.describe().round(2).to_string())

# 4. Pass / Fail counts
print("\n── 4. Pass / Fail Counts ──")
print(df['passed'].value_counts().rename({1: 'Pass', 0: 'Fail'}).to_string())

# 5. Average per subject for pass vs fail
pass_avg  = df[df['passed'] == 1][subject_cols].mean()
fail_avg  = df[df['passed'] == 0][subject_cols].mean()
avg_df = pd.DataFrame({'Pass Avg': pass_avg, 'Fail Avg': fail_avg})
print("\n── 5. Average Score per Subject (Pass vs Fail) ──")
print(avg_df.round(2).to_string())

# 6. Student with highest overall average
df['temp_avg'] = df[subject_cols].mean(axis=1)
best_idx  = df['temp_avg'].idxmax()
best_row  = df.loc[best_idx]
print(f"\n── 6. Highest Overall Average ──")
print(f"  {best_row['name']}  →  {best_row['temp_avg']:.2f}")
df.drop(columns=['temp_avg'], inplace=True)


# ─────────────────────────────────────────────────────────────
# TASK 2 — DATA VISUALIZATION WITH MATPLOTLIB
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 2 — DATA VISUALIZATION WITH MATPLOTLIB")
print("=" * 65)

df['avg_score'] = df[subject_cols].mean(axis=1)

# ── Plot 1: Bar Chart — Average score per subject ──
fig, ax = plt.subplots(figsize=(8, 5))
subject_means = df[subject_cols].mean()
bars = ax.bar(subject_means.index, subject_means.values,
              color=['#4C72B0','#DD8452','#55A868','#C44E52','#8172B3'],
              edgecolor='white', width=0.6)
ax.set_title('Average Score per Subject (All Students)', fontsize=14, fontweight='bold')
ax.set_xlabel('Subject')
ax.set_ylabel('Average Score')
ax.set_ylim(0, 100)
for bar, val in zip(bars, subject_means.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{val:.1f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('plot1_bar.png', dpi=150)
plt.close()
print("Saved plot1_bar.png")

# ── Plot 2: Histogram — Distribution of math scores ──
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df['math'], bins=5, color='#4C72B0', edgecolor='white', alpha=0.85)
mean_math = df['math'].mean()
ax.axvline(mean_math, color='red', linestyle='--', linewidth=1.8, label=f'Mean: {mean_math:.1f}')
ax.set_title('Distribution of Math Scores', fontsize=14, fontweight='bold')
ax.set_xlabel('Math Score')
ax.set_ylabel('Number of Students')
ax.legend()
plt.tight_layout()
plt.savefig('plot2_histogram.png', dpi=150)
plt.close()
print("Saved plot2_histogram.png")

# ── Plot 3: Scatter — study_hours vs avg_score coloured by passed ──
fig, ax = plt.subplots(figsize=(8, 5))
pass_df = df[df['passed'] == 1]
fail_df = df[df['passed'] == 0]
ax.scatter(pass_df['study_hours_per_day'], pass_df['avg_score'],
           color='#2ca02c', s=80, label='Pass', zorder=3)
ax.scatter(fail_df['study_hours_per_day'], fail_df['avg_score'],
           color='#d62728', s=80, marker='X', label='Fail', zorder=3)
ax.set_title('Study Hours vs Average Score (Pass/Fail)', fontsize=14, fontweight='bold')
ax.set_xlabel('Study Hours per Day')
ax.set_ylabel('Average Score')
ax.legend()
plt.tight_layout()
plt.savefig('plot3_scatter.png', dpi=150)
plt.close()
print("Saved plot3_scatter.png")

# ── Plot 4: Box Plot — attendance_pct by pass/fail ──
fig, ax = plt.subplots(figsize=(7, 5))
pass_att = df[df['passed'] == 1]['attendance_pct'].tolist()
fail_att = df[df['passed'] == 0]['attendance_pct'].tolist()
bp = ax.boxplot([pass_att, fail_att], labels=['Pass', 'Fail'],
                patch_artist=True, widths=0.5)
bp['boxes'][0].set_facecolor('#2ca02c')
bp['boxes'][1].set_facecolor('#d62728')
for patch in bp['boxes']:
    patch.set_alpha(0.7)
ax.set_title('Attendance % Distribution: Pass vs Fail', fontsize=14, fontweight='bold')
ax.set_xlabel('Outcome')
ax.set_ylabel('Attendance (%)')
plt.tight_layout()
plt.savefig('plot4_boxplot.png', dpi=150)
plt.close()
print("Saved plot4_boxplot.png")

# ── Plot 5: Line Plot — math & science scores per student ──
fig, ax = plt.subplots(figsize=(11, 5))
x = range(len(df))
ax.plot(x, df['math'],    marker='o', linestyle='-',  color='#4C72B0', label='Math')
ax.plot(x, df['science'], marker='s', linestyle='--', color='#DD8452', label='Science')
ax.set_xticks(list(x))
ax.set_xticklabels(df['name'], rotation=45, ha='right')
ax.set_title('Math & Science Scores per Student', fontsize=14, fontweight='bold')
ax.set_xlabel('Student')
ax.set_ylabel('Score')
ax.legend()
plt.tight_layout()
plt.savefig('plot5_line.png', dpi=150)
plt.close()
print("Saved plot5_line.png")


# ─────────────────────────────────────────────────────────────
# TASK 3 — DATA VISUALIZATION WITH SEABORN
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 3 — DATA VISUALIZATION WITH SEABORN")
print("=" * 65)

sns.set_theme(style='whitegrid')
pass_label_map = {1: 'Pass', 0: 'Fail'}
df['outcome'] = df['passed'].map(pass_label_map)

# ── Seaborn Plot 1: Bar — avg math & science split by passed ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
sns.barplot(data=df, x='outcome', y='math',    palette={'Pass':'#2ca02c','Fail':'#d62728'}, ax=ax1)
ax1.set_title('Avg Math Score by Outcome')
ax1.set_xlabel('Outcome'); ax1.set_ylabel('Average Math Score')

sns.barplot(data=df, x='outcome', y='science', palette={'Pass':'#2ca02c','Fail':'#d62728'}, ax=ax2)
ax2.set_title('Avg Science Score by Outcome')
ax2.set_xlabel('Outcome'); ax2.set_ylabel('Average Science Score')

plt.suptitle('Math & Science Averages: Pass vs Fail', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('seaborn_plot1_barplot.png', dpi=150)
plt.close()
print("Saved seaborn_plot1_barplot.png")

# ── Seaborn Plot 2: Scatter + regression by passed ──
fig, ax = plt.subplots(figsize=(9, 5))
sns.regplot(data=df[df['passed']==1], x='attendance_pct', y='avg_score',
            color='#2ca02c', label='Pass', scatter_kws={'s':60}, ax=ax)
sns.regplot(data=df[df['passed']==0], x='attendance_pct', y='avg_score',
            color='#d62728', label='Fail', scatter_kws={'s':60, 'marker':'X'}, ax=ax)
ax.set_title('Attendance % vs Average Score with Regression Lines', fontsize=13, fontweight='bold')
ax.set_xlabel('Attendance (%)')
ax.set_ylabel('Average Score')
ax.legend()
plt.tight_layout()
plt.savefig('seaborn_plot2_regplot.png', dpi=150)
plt.close()
print("Saved seaborn_plot2_regplot.png")

# Seaborn vs Matplotlib comparison:
# Seaborn produced polished, publication-quality plots with fewer lines of code —
# grouped bar plots and regression overlays required no manual colour management or
# loop logic. Matplotlib offered finer control (e.g. custom box colours, explicit
# tick rotation) but needed more boilerplate for anything involving groups or stats.
# For exploratory analysis, Seaborn is faster; for highly custom figures, Matplotlib wins.


# ─────────────────────────────────────────────────────────────
# TASK 4 — MACHINE LEARNING WITH SCIKIT-LEARN
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("TASK 4 — MACHINE LEARNING WITH SCIKIT-LEARN")
print("=" * 65)

feature_cols = ['math', 'science', 'english', 'history', 'pe',
                'attendance_pct', 'study_hours_per_day']

X = df[feature_cols]
y = df['passed']

# Step 1 — Split & Scale
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Step 2 — Train
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)

train_acc = accuracy_score(y_train, model.predict(X_train_scaled))
print(f"\n── Step 2: Training Accuracy: {train_acc * 100:.1f}% ──")

# Step 3 — Evaluate
y_pred = model.predict(X_test_scaled)
test_acc = accuracy_score(y_test, y_pred)
print(f"\n── Step 3: Test Accuracy: {test_acc * 100:.1f}% ──")

test_names = df.loc[X_test.index, 'name'].values
print(f"\n{'Student':<10} {'Actual':<8} {'Predicted':<10} {'Correct?'}")
print("-" * 42)
for name, actual, pred in zip(test_names, y_test.values, y_pred):
    actual_lbl = "Pass" if actual == 1 else "Fail"
    pred_lbl   = "Pass" if pred   == 1 else "Fail"
    mark = "✅" if actual == pred else "❌"
    print(f"{name:<10} {actual_lbl:<8} {pred_lbl:<10} {mark}")

# Step 4 — Feature Importance
coefs = model.coef_[0]
importance = sorted(zip(feature_cols, coefs), key=lambda x: abs(x[1]), reverse=True)
print("\n── Step 4: Feature Coefficients (sorted by |value|) ──")
for feat, coef in importance:
    direction = "→ Pass" if coef > 0 else "→ Fail"
    print(f"  {feat:<25}  {coef:+.4f}  {direction}")

# Feature importance bar chart
fig, ax = plt.subplots(figsize=(9, 5))
feats, vals = zip(*importance)
colours = ['#2ca02c' if v > 0 else '#d62728' for v in vals]
ax.barh(feats, vals, color=colours, edgecolor='white')
ax.axvline(0, color='black', linewidth=0.8)
ax.set_title('Logistic Regression Feature Coefficients', fontsize=13, fontweight='bold')
ax.set_xlabel('Coefficient Value  (green = pushes Pass, red = pushes Fail)')
ax.set_ylabel('Feature')
plt.tight_layout()
plt.savefig('plot6_feature_importance.png', dpi=150)
plt.close()
print("Saved plot6_feature_importance.png")

# Step 5 — Predict new student (Bonus)
print("\n── Step 5 (Bonus): Predict New Student ──")
new_student = [[75, 70, 68, 65, 80, 82, 3.2]]
new_scaled  = scaler.transform(new_student)
prediction  = model.predict(new_scaled)[0]
proba       = model.predict_proba(new_scaled)[0]
result      = "Pass ✅" if prediction == 1 else "Fail ❌"
print(f"  Features : math=75, science=70, english=68, history=65, pe=80, att=82%, study=3.2h")
print(f"  Prediction: {result}")
print(f"  Probabilities — Fail: {proba[0]:.2%}  |  Pass: {proba[1]:.2%}")

print("\nAll tasks complete.")
