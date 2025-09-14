# app/main.py

from fastapi import FastAPI, Query
import pandas as pd
import numpy as np
import joblib
from app.schemas import Transaction, TransactionResponse, BatchTransaction, BatchTransactionResponse
from typing import List, Optional

# ---------------- Load data, model & preprocessor ----------------
df_cleaned = pd.read_csv("data/cleaned_Kenya_Fraud_data.csv")
model = joblib.load("models/isolation_forest.joblib")
preprocessor = joblib.load("models/preprocessor.joblib")

# ---------------- FastAPI app ----------------
app = FastAPI(
    title="Fraud Detection API",
    description="API to predict fraudulent transactions using Isolation Forest",
    version="1.0"
)

# ---------------- Helper function ----------------
def predict_anomaly(input_df: pd.DataFrame) -> pd.DataFrame:
    # Log-transform the amount
    input_df['log_amount'] = np.log1p(input_df['amount'])
    
    # Transform features
    X_input = preprocessor.transform(input_df)
    
    # Predict
    pred_flag = model.predict(X_input)
    anomaly_score = model.decision_function(X_input)
    
    input_df['is_anomaly'] = (pred_flag == -1).astype(int)
    input_df['anomaly_score'] = anomaly_score
    
    return input_df

# ---------------- Single transaction endpoint ----------------
@app.post("/predict", response_model=TransactionResponse)
def predict(transaction: Transaction):
    input_df = pd.DataFrame([transaction.dict()])
    result_df = predict_anomaly(input_df)
    
    return TransactionResponse(
        is_anomaly=int(result_df['is_anomaly'].iloc[0]),
        anomaly_score=float(result_df['anomaly_score'].iloc[0])
    )

# ---------------- Batch transaction endpoint ----------------
@app.post("/predict_batch", response_model=BatchTransactionResponse)
def predict_batch(batch: BatchTransaction):
    input_df = pd.DataFrame([t.dict() for t in batch.transactions])
    result_df = predict_anomaly(input_df)
    
    results = [
        TransactionResponse(
            is_anomaly=int(row['is_anomaly']),
            anomaly_score=float(row['anomaly_score'])
        )
        for _, row in result_df.iterrows()
    ]
    return BatchTransactionResponse(results=results)

# ---------------- Filter transactions endpoint ----------------
@app.get("/transactions")
def get_transactions(
    transaction_type: list[str] = Query(None),
    location: list[str] = Query(None),
    user_type: list[str] = Query(None),
    limit: int = 1000
):
    df_filtered = df_cleaned.copy()

    if transaction_type:
        df_filtered = df_filtered[df_filtered['transaction_type'].isin(transaction_type)]
    if location:
        df_filtered = df_filtered[df_filtered['location'].isin(location)]
    if user_type:
        df_filtered = df_filtered[df_filtered['user_type'].isin(user_type)]

    df_filtered = df_filtered.head(limit)

    # ---------------- Compute anomalies ----------------
    df_filtered['log_amount'] = np.log1p(df_filtered['amount'])
    X = preprocessor.transform(df_filtered)
    pred_flag = model.predict(X)
    df_filtered['is_anomaly'] = (pred_flag == -1).astype(int)
    df_filtered['anomaly_score'] = model.decision_function(X)

    return df_filtered.to_dict(orient="records")