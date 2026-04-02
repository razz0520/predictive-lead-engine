import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# 1. RAW DATA INGESTION & CLEANING (Internalized for safety)
df = pd.read_csv('data/bank-additional/bank-additional-full.csv', sep=';')
df.replace('unknown', np.nan, inplace=True)
df['y'] = np.where(df['y'] == 'yes', 1, 0)
df.drop(columns=['default'], inplace=True)
for col in ['education', 'housing', 'loan', 'job', 'marital']:
    df[col] = df[col].fillna(df[col].mode()[0])

# 2. ENCODING & SPLITTING
df_final = pd.get_dummies(df, drop_first=True)
X = df_final.drop('y', axis=1)
y = df_final['y']

# GET FEATURE NAMES NOW (for saving later)
feature_names = X.columns.tolist()

# FORCE CONVERSION TO NUMPY IMMEDIATELY
X_np = X.to_numpy()
y_np = y.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X_np, y_np, test_size=0.2, random_state=42)

# 3. SCALING (Result is NumPy Array)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("--- Phase 4: Training Balanced Model (NUMPY-ONLY FLOW) ---")

# 4. SMOTE (Result is NumPy Array)
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train_scaled, y_train)

# 5. TRAIN & PREDICT
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_res, y_res) 

# This is a NumPy array vs NumPy array - WARNING IMPOSSIBLE
y_pred = rf_model.predict(X_test_scaled) 

# 6. EVALUATE
print("\n--- FINAL CLASSIFICATION REPORT ---")
report = classification_report(y_test, y_pred)
print(report)

# 7. SAVE EVERYTHING
joblib.dump(rf_model, 'lead_scoring_model.pkl')
joblib.dump(scaler, 'scaler.pkl') # Save scaler for the web app!
joblib.dump(feature_names, 'model_features.pkl')
print("\n[SUCCESS] Warning-free model saved.")