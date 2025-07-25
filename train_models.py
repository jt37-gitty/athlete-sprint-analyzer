import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

df = pd.read_csv("athlete_sprint_analysis_800.csv")

assert all(col in df.columns for col in ['T1', 'T2', 'T3', 'TotalTime'])

t1_model = LinearRegression().fit(df[['TotalTime']], df['T1'])
t2_model = LinearRegression().fit(df[['TotalTime']], df['T2'])

os.makedirs("backend/models", exist_ok=True)
joblib.dump(t1_model, "backend/models/t1_model.pkl")
joblib.dump(t2_model, "backend/models/t2_model.pkl")

print("Models trained and saved.")
