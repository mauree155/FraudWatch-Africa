import streamlit as st
import pandas as pd
import requests

# Title
st.title("🇰🇪 Kenya Fraud Detection App")
st.markdown("Analyze transactions, predict anomalies, and explore fraud patterns.")

# Load sample dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sample_data.csv")  # Use your dataset file
    return df

df_sample = load_data()

# Dropdown values
transaction_types = df_sample['transaction_type'].unique()
locations = df_sample['location'].unique()
user_types = df_sample['user_type'].unique()

# FastAPI base URL (Render deployed)
API_URL = "https://kenya-fraud-detection.onrender.com"

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Explore Transactions", "💡 Predict Single Transaction", "📦 Batch Predictions"])

# --------------------------------------------------------------------
# TAB 1 - Explore Transactions
# --------------------------------------------------------------------
with tab1:
    st.markdown("## 📊 Explore Transactions")

    selected_transaction_types = st.multiselect("Transaction Types", transaction_types, default=transaction_types[:3])
    selected_locations = st.multiselect("Locations", locations, default=locations[:3])
    selected_user_types = st.multiselect("User Types", user_types, default=user_types)

    params = {
        "transaction_type": selected_transaction_types,
        "location": selected_locations,
        "user_type": selected_user_types,
        "limit": 1000
    }

    if st.button("Fetch Transactions"):
        try:
            response = requests.get(f"{API_URL}/transactions", params=params)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(pd.DataFrame(data))
            else:
                st.error(f"Error fetching transactions: {response.text}")
        except Exception as e:
            st.error(f"Error fetching filtered transactions: {e}")

# --------------------------------------------------------------------
# TAB 2 - Predict Single Transaction
# --------------------------------------------------------------------
with tab2:
    st.markdown("## 💡 Predict Single Transaction")

    transaction_type_input = st.selectbox("Transaction Type", transaction_types)
    amount_input = st.number_input("Transaction Amount", min_value=0.0, value=1000.0)
    location_input = st.selectbox("Location", locations)
    device_input = st.selectbox("Device Type", df_sample['device_type'].unique())
    network_input = st.selectbox("Network Provider", df_sample['network_provider'].unique())
    user_type_input = st.selectbox("User Type", user_types)

    # Show Yes/No in UI but map to 0/1
    is_foreign_input = st.selectbox("Foreign Number?", ["No", "Yes"])
    sim_swap_input = st.selectbox("Recently Swapped SIM?", ["No", "Yes"])
    multiple_accounts_input = st.selectbox("Has Multiple Accounts?", ["No", "Yes"])

    if st.button("Predict Fraud"):
        input_data = {
            "transaction_type": transaction_type_input,
            "amount": amount_input,
            "location": location_input,
            "device_type": device_input,
            "network_provider": network_input,
            "user_type": user_type_input,
            "is_foreign_number": 1 if is_foreign_input == "Yes" else 0,
            "is_sim_recently_swapped": 1 if sim_swap_input == "Yes" else 0,
            "has_multiple_accounts": 1 if multiple_accounts_input == "Yes" else 0
        }

        try:
            response = requests.post(f"{API_URL}/predict", json=input_data)
            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Prediction: {'🚨 Fraudulent' if prediction['anomaly'] == 1 else '✅ Legitimate'}")
                st.json(prediction)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error making prediction: {e}")

# --------------------------------------------------------------------
# TAB 3 - Batch Predictions
# --------------------------------------------------------------------
with tab3:
    st.markdown("## 📦 Batch Predict Transactions")
    st.markdown("Upload a CSV with your transactions to get anomaly predictions.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.dataframe(batch_df.head())

        if st.button("Run Batch Prediction"):
            try:
                batch_input = batch_df.to_dict(orient="records")
                response = requests.post(f"{API_URL}/predict_batch", json=batch_input)
                if response.status_code == 200:
                    predictions = response.json()
                    result_df = pd.DataFrame(predictions)
                    st.dataframe(result_df)
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error running batch prediction: {e}")
