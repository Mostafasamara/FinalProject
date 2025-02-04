import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from django.conf import settings

# ✅ Define Paths
MODEL_PATH_LIFESTYLE = os.path.join(settings.BASE_DIR, "predictor", "student_lifestyle_model.pkl")
SCALER_PATH_LIFESTYLE = os.path.join(settings.BASE_DIR, "predictor", "student_lifestyle_scaler.pkl")

MODEL_PATH_PERFORMANCE = os.path.join(settings.BASE_DIR, "predictor", "student_performance_model.pkl")
SCALER_PATH_PERFORMANCE = os.path.join(settings.BASE_DIR, "predictor", "student_performance_scaler.pkl")

FEATURES_PATH = os.path.join(settings.BASE_DIR, "predictor", "performance_features.pkl")

DATA_LIFESTYLE_PATH = os.path.join(settings.BASE_DIR, "predictor", "student_lifestyle_dataset.csv")
DATA_PERFORMANCE_PATH = os.path.join(settings.BASE_DIR, "predictor", "student_performance_data.csv")


def encode_categorical_features(df):
    """Convert categorical columns into numeric values using one-hot encoding."""

    # ✅ Convert binary categorical values ('Yes'/'No') to numeric (1/0)
    binary_columns = ["PartTimeJob", "ExtraCurricularActivities"]
    for col in binary_columns:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)

    # ✅ Apply One-Hot Encoding to categorical variables (Gender, Major)
    df = pd.get_dummies(df, columns=["Gender", "Major"], drop_first=True)

    return df


def train_lifestyle_model():
    """Train model based on lifestyle dataset"""
    print("🚀 Training lifestyle model...")

    df = pd.read_csv(DATA_LIFESTYLE_PATH)

    # ✅ Drop ID column if it exists
    df.drop(columns=['Student_ID'], errors='ignore', inplace=True)

    # ✅ Ensure `GPA` is removed from features
    if 'GPA' in df.columns:
        y = df.pop('GPA')
    else:
        raise ValueError("❌ 'GPA' column is missing from lifestyle dataset!")

    # ✅ Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)

    # ✅ Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ✅ Train Model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # ✅ Save model & scaler
    joblib.dump(model, MODEL_PATH_LIFESTYLE)
    joblib.dump(scaler, SCALER_PATH_LIFESTYLE)

    print(f"✅ Lifestyle Model saved at: {MODEL_PATH_LIFESTYLE}")


def train_performance_model():
    """Train model based on performance dataset"""
    print("🚀 Training performance model...")

    df_performance = pd.read_csv(DATA_PERFORMANCE_PATH)

    # ✅ Drop ID columns if they exist
    df_performance.drop(columns=['Student_ID'], errors='ignore', inplace=True)

    # ✅ Encode categorical variables using One-Hot Encoding
    df_performance = encode_categorical_features(df_performance)

    # ✅ Ensure `GPA` is removed before saving feature names
    if 'GPA' in df_performance.columns:
        y = df_performance.pop('GPA')
    else:
        raise ValueError("❌ 'GPA' column is missing from dataset!")

    # ✅ Save updated feature names
    trained_features = df_performance.columns.tolist()
    joblib.dump(trained_features, FEATURES_PATH)

    print("🔹 Saved Training Feature Names (Ordered):", trained_features)

    # ✅ Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(df_performance, y, test_size=0.2, random_state=42)

    # ✅ Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ✅ Train Model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # ✅ Save model & scaler
    joblib.dump(model, MODEL_PATH_PERFORMANCE)
    joblib.dump(scaler, SCALER_PATH_PERFORMANCE)

    print(f"✅ Performance Model saved successfully at: {MODEL_PATH_PERFORMANCE}")


def predict_student_performance(lifestyle_data, performance_data):
    """Predicts GPA using both lifestyle and performance models."""

    try:
        # ✅ Load models & scalers
        lifestyle_model = joblib.load(MODEL_PATH_LIFESTYLE)
        lifestyle_scaler = joblib.load(SCALER_PATH_LIFESTYLE)
        performance_model = joblib.load(MODEL_PATH_PERFORMANCE)
        performance_scaler = joblib.load(SCALER_PATH_PERFORMANCE)
        features_list = joblib.load(FEATURES_PATH)  # Ensure correct feature order
    except Exception as e:
        raise ValueError(f"❌ Model loading failed: {str(e)}")

    # ✅ Convert lifestyle data into DataFrame
    lifestyle_df = pd.DataFrame([lifestyle_data])

    # ✅ Convert performance data into DataFrame & encode categorical features
    performance_df = pd.DataFrame([performance_data])
    performance_df = encode_categorical_features(performance_df)

    # ✅ Normalize lifestyle features
    lifestyle_scaled = lifestyle_scaler.transform(lifestyle_df)

    # ✅ Predict lifestyle impact on performance
    lifestyle_gpa_prediction = lifestyle_model.predict(lifestyle_scaled)

    # ✅ Add predicted GPA as a new feature to performance data
    performance_df["Predicted_Lifestyle_GPA"] = lifestyle_gpa_prediction

    # ✅ Ensure performance_df has the correct feature order
    missing_features = [col for col in features_list if col not in performance_df.columns]
    for feature in missing_features:
        performance_df[feature] = 0  # Add missing features with default values

    # ✅ Normalize performance data
    performance_scaled = performance_scaler.transform(performance_df[features_list])

    # ✅ Predict final GPA
    final_gpa_prediction = performance_model.predict(performance_scaled)

    return final_gpa_prediction[0]  # Return single predicted GPA value


# ✅ Train models only when this file is run directly
if __name__ == "__main__":
    try:
        print("🚀 Training Models on Startup...")
        train_lifestyle_model()
        train_performance_model()
    except Exception as e:
        print(f"❌ Model training error: {str(e)}")
