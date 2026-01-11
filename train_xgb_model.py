import pandas as pd
import pickle
import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv("intents.csv")

X = df["text"]
y = df["intent"]

# Encode labels
le = LabelEncoder()
y_enc = le.fit_transform(y)

# Vectorize
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train XGBoost
model = xgb.XGBClassifier(
    objective="multi:softprob",
    num_class=len(set(y_enc)),
    eval_metric="mlogloss"
)
model.fit(X_vec, y_enc)

# Save everything
with open("xgb_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ XGBoost model saved")
