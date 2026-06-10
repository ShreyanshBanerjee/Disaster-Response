import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os


os.makedirs("models", exist_ok=True)

df = pd.read_csv("us_flood_risk_dataset.csv")
features = [c for c in df.columns if c != "label"]

X = df[features]
y = df["label"]

le = LabelEncoder()
y = le.fit_transform(y)

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
XTrain_s = scaler.fit_transform(XTrain)
XTest_s  = scaler.transform(XTest)

model = RandomForestClassifier(n_estimators=300, max_depth=25, random_state=42, class_weight="balanced")
model.fit(XTrain_s, yTrain)

print("Accuracy:", model.score(XTest_s, yTest))

joblib.dump(model, "models/flood_risk_model.pkl")
joblib.dump(scaler, "models/feature_scaler.pkl")
joblib.dump(le, "models/label_encoder.pkl")