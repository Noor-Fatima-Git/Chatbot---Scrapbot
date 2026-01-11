import pandas as pd
import xgboost as xgb
import pickle

# Dummy training data (example: salary prediction)
data = {
    "experience": [1, 2, 3, 4, 5],
    "salary": [30000, 45000, 60000, 80000, 100000]
}

df = pd.DataFrame(data)

X = df[["experience"]]
y = df["salary"]

model = xgb.XGBRegressor(
    objective="reg:squarederror",
    n_estimators=50
)

model.fit(X, y)

# Save model
with open("xgb_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("XGBOOST MODEL TRAINED")
