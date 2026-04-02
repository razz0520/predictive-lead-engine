import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# --- PHASE 2: CLEANING ---
df = pd.read_csv('data/bank-additional/bank-additional-full.csv', sep=';')
df.replace('unknown', np.nan, inplace=True)
df['y'] = np.where(df['y'] == 'yes', 1, 0)
df['is_retired'] = np.where((df['age'] > 60) & (df['job'] == 'retired'), 1, 0)

# Drop high-missingness column and impute mode
df.drop(columns=['default'], inplace=True)
cols_to_fix = ['education', 'housing', 'loan', 'job', 'marital']
for col in cols_to_fix:
    df[col] = df[col].fillna(df[col].mode()[0])

# --- PHASE 3: ML PREPARATION ---
# 1. One-Hot Encoding
df_final = pd.get_dummies(df, drop_first=True)

# 2. Define Features and Target
X = df_final.drop('y', axis=1)
y = df_final['y']

# 3. Train-Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Phase 3 Complete.")
print(f"Training Data Shape: {X_train_scaled.shape}")
print(f"Final Feature Count: {X_train_scaled.shape[1]}")