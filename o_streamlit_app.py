# app/streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px

# ------------------ Page Config ----------------
st.set_page_config(
    page_title="Kenya Fraud Detection",
    page_icon="💳",
    layout="wide"
)

# ------------------ Sidebar Navigation ----------------
page = st.sidebar.selectbox("Navigate", ["Home", "Dashboard", "About"])

# ------------------ Home Page ----------------
if page == "Home":
    st.title("💳 Kenya Fraud Detection")
    st.image(
        "assets/fraud_detection_banner.png", 
        use_container_width=True
    )
    st.markdown("""
    Welcome! This is your one-stop dashboard for detecting anomalies 
    and fraudulent transactions in Kenya. Explore dashboards, predict transactions, 
    and download reports with ease.
    """)

# ------------------ About Page ----------------
elif page == "About":
    st.title("👥 Meet the Team")

    # Team members with custom gradients
    team = [
        {
            "name": "Maureen Akunna Okoro",
            "role": "Team Lead · Data Analyst / Scientist",
            "email": "mailto:okoromaureen590@gmail.com",
            "linkedin": "https://ng.linkedin.com/in/maureen-okoro-8a1972245",
            "color": "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)"
        },
        {
            "name": "Masheia Dzimba",
            "role": "Data Scientist",
            "email": "mailto:mdzimba@mail.yu.edu",
            "linkedin": "https://www.linkedin.com/in/masheia-d-965099121",
            "color": "linear-gradient(135deg, #ff512f 0%, #dd2476 100%)"
        },
        {
            "name": "Nasiru Ibrahim",
            "role": "Data Scientist",
            "email": "mailto:nasiruibrahim3034@gmail.com",
            "linkedin": "https://www.linkedin.com/in/nasiru-ibrahim-89b489177",
            "color": "linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)"
        }
    ]

    # About Us section
    st.markdown("""
    ## About Us  

    We are a team of **Data Science and Analytics Interns at Dataverse Africa**, passionate about transforming complex data into practical solutions.  
    Our work focuses on **fraud detection, anomaly monitoring, and turning raw information into insights** that drive meaningful impact.  

    ### What We Do  
    - Detect patterns and anomalies using advanced data science techniques  
    - Build tools that strengthen fraud prevention and risk management  
    - Deliver actionable insights through dashboards and data storytelling  

    ### Our Journey  
    Through this project, we have:  
    - Gained hands-on experience in fraud detection, machine learning, and analytics  
    - Collaborated effectively as a multidisciplinary team  
    - Developed skills combining research, coding, and storytelling  

    ---
    
    ### Our Commitment  
    We are committed to **continuous learning, innovation, and creating solutions** that empower organizations and communities across Africa and beyond.  
    """)

# ------------------ Dashboard & Predictions ----------------
elif page == "Dashboard":
    st.sidebar.header("Filter Transactions")

    # Temporary local load to populate filter options
    df_sample = pd.read_csv("data/cleaned_Kenya_Fraud_data.csv")
    transaction_types = df_sample['transaction_type'].unique()
    locations = df_sample['location'].unique()
    user_types = df_sample['user_type'].unique()

    selected_types = st.sidebar.multiselect("Transaction Type", transaction_types, default=list(transaction_types))
    selected_locations = st.sidebar.multiselect("Location", locations, default=list(locations))
    selected_users = st.sidebar.multiselect("User Type", user_types, default=list(user_types))

    # ------------------ Fetch filtered transactions from FastAPI ------------------
    @st.cache_data
    def get_filtered_transactions(types, locations, users, limit=1000):
        params = {
            "transaction_type": types,
            "location": locations,
            "user_type": users,
            "limit": limit
        }
        try:
            response = requests.get("https://kenya-fraud-detection.onrender.com/transactions", params=params)
            response.raise_for_status()
            df = pd.DataFrame(response.json())
            return df
        except Exception as e:
            st.error(f"Error fetching filtered transactions: {e}")
            return pd.DataFrame()

    with st.spinner("Fetching filtered transactions..."):
        filtered_df = get_filtered_transactions(selected_types, selected_locations, selected_users)

    # ------------------ Tabs ------------------
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💡 Predict Transaction", "📦 Batch Predict"])

    # ------------------ Tab 1: Dashboard ------------------
    with tab1:
        st.markdown("## Fraud Detection Dashboard")

        total_tx = len(filtered_df)
        total_anomalies = filtered_df['is_anomaly'].sum() if 'is_anomaly' in filtered_df.columns else 0
        percent_anomalies = round(total_anomalies / total_tx * 100, 2) if total_tx > 0 else 0

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Transactions", total_tx)
        kpi2.metric("Flagged Anomalies", total_anomalies)
        kpi3.metric("% Anomalies", f"{percent_anomalies}%", delta_color="inverse")

        if 'is_anomaly' in filtered_df.columns:
            anomaly_table = filtered_df[filtered_df['is_anomaly'] == 1]
            st.markdown("### ⚠️ Flagged Transactions")
            st.dataframe(anomaly_table.head(10).style.highlight_max(axis=0, color="salmon"))

            st.download_button(
                "Download Flagged Anomalies CSV",
                anomaly_table.to_csv(index=False).encode(),
                "flagged_anomalies.csv",
                "text/csv"
            )

            # Plots
            st.markdown("### 📈 Anomalies by Transaction Type")
            tx_counts = anomaly_table['transaction_type'].value_counts().reset_index()
            tx_counts.columns = ['transaction_type', 'count']
            fig_tx = px.bar(tx_counts, x='transaction_type', y='count', color='count', color_continuous_scale='Reds')
            st.plotly_chart(fig_tx, use_container_width=True)

            st.markdown("### 📍 Anomalies by Location")
            loc_counts = anomaly_table['location'].value_counts().reset_index()
            loc_counts.columns = ['location', 'count']
            fig_loc = px.bar(loc_counts, x='location', y='count', color='count', color_continuous_scale='Reds')
            st.plotly_chart(fig_loc, use_container_width=True)

    # ------------------ Tab 2: Predict Single Transaction ------------------
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

        if st.button("Predict Transaction"):
            input_data = {
                "transaction_type": transaction_type_input,
                "amount": amount_input,
                "location": location_input,
                "device_type": device_input,
                "network_provider": network_input,
                "user_type": user_type_input,
                "is_foreign_number": 1 if is_foreign_input == "Yes" else 0,
                "is_sim_recently_swapped": 1 if sim_swap_input == "Yes" else 0,
                "has_multiple_accounts": 1 if multiple_accounts_input == "Yes" else 0,
            }

            with st.spinner("Predicting..."):
                try:
                    response = requests.post("https://kenya-fraud-detection.onrender.com/predict", json=input_data)
                    response.raise_for_status()
                    result = response.json()

                    if result["is_anomaly"] == 1:
                        st.error(f"⚠️ This transaction can be a fraud! Score: {result['anomaly_score']:.3f}")
                    else:
                        st.success(f"✅ This transaction looks normal. Score: {result['anomaly_score']:.3f}")

                except Exception as e:
                    st.error(f"Error calling API: {e}")

    # ------------------ Tab 3: Batch Predict ------------------
    with tab3:
        st.markdown("## 📦 Batch Predict Transactions")
        st.markdown("Upload a CSV with your transactions to get anomaly predictions.")

        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
        if uploaded_file is not None:
            batch_df = pd.read_csv(uploaded_file)
            st.dataframe(batch_df.head())

            if st.button("Predict Batch"):
                mapping = {"Yes": 1, "No": 0}
                for col in ["is_foreign_number", "is_sim_recently_swapped", "has_multiple_accounts"]:
                    if col in batch_df.columns:
                        batch_df[col] = batch_df[col].map(mapping).fillna(batch_df[col])

                transactions_list = batch_df.to_dict(orient="records")
                batch_input = {"transactions": transactions_list}

                with st.spinner("Predicting batch..."):
                    try:
                        response = requests.post("https://kenya-fraud-detection.onrender.com/predict_batch", json=batch_input)
                        response.raise_for_status()
                        results = response.json()["results"]

                        batch_df['is_anomaly'] = [r['is_anomaly'] for r in results]
                        batch_df['anomaly_score'] = [r['anomaly_score'] for r in results]

                        st.success("Batch predictions completed!")
                        st.dataframe(batch_df.head())

                        st.download_button(
                            "Download Batch Predictions CSV",
                            batch_df.to_csv(index=False).encode(),
                            "batch_predictions.csv",
                            "text/csv"
                        )

                    except Exception as e:
                        st.error(f"Error calling API: {e}")
