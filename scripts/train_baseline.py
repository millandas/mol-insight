import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report

# Load dataset
df = pd.read_csv('/Users/philippevannson/Desktop/AMARCHs3/merged.csv')

print(df.head())
# --- Preprocessing ---
# Drop columns with missing target data
df = df.dropna(subset=['sex', 'age'])

# Drop non-feature columns (tissue, identifiers, etc.)
# Use axis=1 for columns and assign back to df
columns_to_drop = []
if 'tissue' in df.columns:
    columns_to_drop.append('tissue')
if 'sample-id' in df.columns:
    columns_to_drop.append('sample-id')
if 'sample_id' in df.columns:
    columns_to_drop.append('sample_id')
if 'Unnamed: 0' in df.columns:
    columns_to_drop.append('Unnamed: 0')

if columns_to_drop:
    df = df.drop(columns=columns_to_drop)

# Assume the target columns are named 'sex' (gender: 'male'/'female') and 'age'
# Encode categorical (sex)
le = LabelEncoder()
df['sex_enc'] = le.fit_transform(df['sex'])  # female=0, male=1 (by convention of LabelEncoder)

# Example: remove identifier/object columns; keep numeric expression columns
# This assumes all other columns are features except 'sex', 'sex_enc', 'age'
drop_cols = [c for c in ['sex', 'sex_enc', 'age'] if c in df.columns]
feature_cols = [c for c in df.columns if c not in drop_cols]
X = df[feature_cols]
y_gender = df['sex_enc']
y_age = df['age']

# Some models benefit from scaling for continuous features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_gender_train, y_gender_test, y_age_train, y_age_test = train_test_split(
    X_scaled, y_gender, y_age, test_size=0.2, random_state=42
)

print("Predicting gender...")

# Logistic Regression (gender)
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_gender_train)
y_pred_lr = lr.predict(X_test)
print("Logistic Regression Accuracy (gender):", accuracy_score(y_gender_test, y_pred_lr))

# Random Forest (gender)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_gender_train)
y_pred_rf = rf.predict(X_test)
print("Random Forest Accuracy (gender):", accuracy_score(y_gender_test, y_pred_rf))

# Gradient Boosting (gender)
gbc = GradientBoostingClassifier(n_estimators=100, random_state=42)
gbc.fit(X_train, y_gender_train)
y_pred_gbc = gbc.predict(X_test)
print("Gradient Boosting Accuracy (gender):", accuracy_score(y_gender_test, y_pred_gbc))

print("\nClassification report (best model may differ):\n", classification_report(y_gender_test, y_pred_gbc, target_names=le.classes_))

print("\nPredicting age...")

# For age, use regression (split same way)

# Random Forest (age)
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train, y_age_train)
age_pred_rf = rf_reg.predict(X_test)
print("Random Forest MAE (age):", mean_absolute_error(y_age_test, age_pred_rf))

# Gradient Boosting (age)
gbr = GradientBoostingRegressor(n_estimators=100, random_state=42)
gbr.fit(X_train, y_age_train)
age_pred_gb = gbr.predict(X_test)
print("Gradient Boosting MAE (age):", mean_absolute_error(y_age_test, age_pred_gb))

