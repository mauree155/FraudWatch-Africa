# FraudWatch Africa: Unsupervised Mobile Money Transaction Fraud Detection

<img width="1590" height="650" alt="screenshot of app" src="https://github.com/user-attachments/assets/076c8c9a-1e27-4112-89dc-967884fc0684" />

## Table of Contents   
1. [Project Background](#project-background)  
2. [Dataset](#dataset)  
3. [Methodology](#methodology)  
   - [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)  
   - [Data Preprocessing](#data-preprocessing)  
   - [Modeling](#modeling)  
4. [Results & Insights](#results--insights)  
4. [Dashboard & Deployment](#dashboard--deployment)  
8. [Tools & Technologies](#tools--technologies)  
9. [Conclusion](#conclusion)  
10. [Future Work](#future-work)  
11. [How to Run the Project](#how-to-run-the-project)  
12. [Acknowledgments](#acknowledgments)

## 1. Project Background  

### 1.1 Mobile Money in Africa  
Mobile money has transformed financial inclusion in Africa. Services like **M-Pesa (Kenya)**, **MTN Mobile Money (Uganda)**, and **Airtel Money (West Africa)** allow millions of people to send money, pay bills, and manage their finances without relying on traditional banks.  

With over **300 million active users in Sub-Saharan Africa**, mobile money platforms are now the backbone of everyday transactions.  

However, this rapid growth also introduces **security challenges**:  
- Limited regulatory oversight  
- High transaction volumes  
- The anonymity of mobile wallets  

Together, these factors make mobile money ecosystems a **prime target for fraudsters**. Common fraud tactics include:  
- SIM swaps  
- Account takeovers  
- Fraudulent transfers  

### 1.2 The Fraud Detection Challenge  
Fraudulent transactions are notoriously **difficult to detect** because they rarely follow predictable patterns. Traditional supervised machine learning approaches require **labeled fraudulent data**, which is often scarce or unavailable.  

To address this challenge, this project leverages **unsupervised learning**, where the model learns to identify **outliers** that deviate from normal transaction behavior — a promising approach in fraud detection for data-scarce environments.  
## 2. Project Goal  

This project aims to design a **scalable, real-time fraud detection system** tailored to mobile money platforms in Africa.  

Key objectives include:  
- Develop an **unsupervised anomaly detection model** (Isolation Forest) to flag unusual transaction patterns.  
- Provide a **Streamlit dashboard** for interactive visualization of anomalies.  
- Deploy the model using **FastAPI** to enable **real-time fraud detection** for mobile money services.  

## 3. Key Features  

- **Data Simulation**: A synthetic dataset mimicking real-world mobile money transactions in African markets.  
- **Unsupervised Model (Isolation Forest)**: Detect anomalies using transaction amount, frequency, location, and device type.  
- **Interactive Dashboard (Streamlit)**: Visual monitoring of flagged transactions and fraud patterns.  
- **Real-time API (FastAPI)**: Seamless deployment of the fraud detection engine for live monitoring and integration.  

## 4. Dataset  

The dataset used in this project simulates **10,000 mobile money transactions** to reflect real-world activity in African markets. It includes various features such as:
- **User IDs & Device IDs** – uniquely identify customers and their devices  
- **Transaction Amounts** – numerical values of money transfers  
- **Transaction Types** – send, receive, cash-in, cash-out, buy airtime, deposit, withdrawal  
- **User Locations** – geographic regions within Africa (e.g., Nairobi, Lagos, Kampala)  
- **Transaction Channels** – USSD, Mobile App, Web, Agent  
- **SIM Swap Flags** – indicator for possible SIM swap fraud  
- **Agent IDs** – identify transactions carried out through agents  

### Purpose of Simulation  
Since real mobile money transaction datasets are rarely publicly available (due to privacy concerns), a synthetic dataset was generated to:  
- Represent typical **user behaviors**  
- Simulate **fraudulent patterns** (e.g., unusual amounts, odd times, suspicious device usage)  
- Provide enough diversity for training and validating the unsupervised model

## 5. Methodology

This project was executed using **Python**, with analysis performed in **Jupyter Notebook** and deployment via **Streamlit** and **FastAPI**.

### 5.1 Exploratory Data Analysis (EDA)

- Examined the dataset to understand distributions, patterns, and potential anomalies.  
- Investigated transaction amounts, timing (hour of day, day of week), user locations, devices, and transaction types.  
- Identified preliminary trends such as skewed transaction amounts and temporal patterns, which informed feature engineering and model expectations.

-
### 5.2 Data Preprocessing

- **Handling Missing Values**:  
  - Numerical columns filled with median values.  
  - Categorical columns filled with mode values.  
- **Feature Engineering**:  
  - Created `log_amount` to reduce skewness in transaction amounts.  
  - Extracted `hour` and `day_of_week` from transaction timestamps.  
  - Added `time_of_day` (morning, afternoon, evening, night) for better interpretability.  
- **Feature Scaling**: Applied scaling to numerical features to improve model stability and training efficiency.  

### 5.3 Modeling: Anomaly Detection

- **Algorithm Used**: `Isolation Forest`, an unsupervised model for anomaly detection.  
- **Training Details**:  
  - Model trained on the full dataset without labeled fraud data.  
  - Contamination rate set to **5%** to correspond with expected anomaly proportion.  
- **Anomaly Identification**: Model learned “normal” patterns and flagged deviations as anomalies.

### 5.4 Evaluation

- Inspected flagged transactions to assess model effectiveness.  
- Applied dimensionality reduction techniques (t-SNE, UMAP) to visualize separation between normal and anomalous transactions.  
- Tuned hyperparameters such as contamination rate to optimize anomaly detection.  


### 5.5 Deployment

- **Streamlit Dashboard**: Provides an interface to explore and monitor flagged transactions interactively.  
- **FastAPI Endpoint**: Enables real-time fraud detection by sending new transaction data to the model and receiving predictions.

## 6. Results and Discussion

### 6.1 Transaction Amount Analysis

- The `amount` column is **right-skewed** with a mean of 3,496.41, standard deviation of 3,507.29, minimum of 0.03, and maximum of 30,221.30.  
- Applying a **log transformation** (`log_amount`) produced a more normally distributed variable, which improves model performance in detecting anomalies.  
- Most transactions fall within a “normal” range, while a small fraction (~5%) represent **outliers**, which the Isolation Forest model successfully flagged.

![Amount Distribution](https://github.com/user-attachments/assets/8bcb173f-cf51-4a15-b579-b2bcea5f1ee2)

 ![Log-Scaled Amount Distribution](https://github.com/user-attachments/assets/8cae5a48-7465-4ba3-adac-1a9eab3c6ce5) 


### 6.2 Transaction Timing Patterns

- **Time of Day**: Most transactions occur at **night (10 PM – 4 AM)**, suggesting fraudsters may exploit low-monitoring periods. Morning transactions follow closely, while afternoon and evening remain low.  
- **Day of Week**: Saturdays have the highest volume (~1,750 transactions), with weekdays relatively stable (~1,300–1,450).  

 ![Time of Day Trends](https://github.com/user-attachments/assets/8c57592b-49be-4a95-8f1f-ab3dec4b86f6) 

  ![Day of Week Transactions](https://github.com/user-attachments/assets/c6420c8c-6d16-41d6-8f9f-743e8ab974ea)

**Insight**: Monitoring should be more vigilant during high-activity periods, especially nights and weekends.


### 6.3 Location-based Patterns

- Most locations show average transaction amounts between 3,300 and 3,700.  
- Eldoret, Mombasa, and Kisumu exhibit slightly higher transaction amounts, indicating potential risk areas.  

![Transaction Amount by Location](https://github.com/user-attachments/assets/3ee878bd-6b66-4aa5-a55e-36be57c546e5)


---

### 6.4 User and Device Insights

- The majority of anomalies originate from **agents** rather than individual users (386 out of 500 anomalies).  
- By device type: iOS leads in flagged transactions, followed by Android and Feature Phones.  
- Network distribution of anomalies is fairly even: Safaricom (173), Telkom Kenya (171), Airtel (156).
- 
![Transactions by user](https://github.com/user-attachments/assets/1307d641-f43f-4fa8-81b6-f808dbea37d5)


![Transactions by Device type](https://github.com/user-attachments/assets/452c37fa-6fa4-473b-82c4-414ef134a623)


### 6.5 Transaction Type Patterns

- **Send Money**, **Buy Airtime**, and **Deposit Cash** are the transaction types most frequently flagged as anomalies.  
- This suggests that fraud monitoring can prioritize these transaction types for enhanced scrutiny.

![Transactions by types](https://github.com/user-attachments/assets/6de40f93-e6d0-4beb-aac9-156014fb09d3)

### 6.6 Transactions by network providers

- The distribution of anomalies across network providers is relatively even, with **Safaricom** having the most anomalies (173), 
followed closely by Telkom Kenya (171), and then Airtel (156). 

This indicates that no single network provider is disproportionately affected by the types of anomalies detected by this model.

![Transactions by network providers](https://github.com/user-attachments/assets/0e54e894-de1f-47f4-8d10-81b4cc000951)



### 6.7 Dimensionality Reduction and Model Validation

- **t-SNE Visualization**: Projects transactions into 2D; **blue points = normal**, **red points = anomalies**. Normal transactions form tight clusters, while anomalies appear isolated or on cluster edges.  
- **UMAP Visualization**: Preserves local and global structure; confirms separation between normal and anomalous transactions.  

![t-SNE Plot](https://github.com/user-attachments/assets/8e9a8482-7f4b-41d8-9432-42f778a2551f)

![UMAP Plot](https://github.com/user-attachments/assets/7a14cda3-3003-4589-91ab-8bea128c3ac7)

**Key Insight**: Both t-SNE and UMAP confirm that the Isolation Forest model effectively identifies anomalies, providing visual proof that flagged transactions deviate from typical behavior.

### 6.7 Summary of Findings

- ~5% of transactions are flagged as anomalies, consistent with the contamination parameter.  
- Anomalies are concentrated in **nighttime hours**, **weekends**, specific **locations**, **transaction types**, and **device types**.  
- The model’s predictions align with observed behavioral patterns, indicating the unsupervised approach is effective for fraud detection without labeled data.

## 7. Live Demo and Deployment

### 7.1 Streamlit Dashboard – FraudWatch Africa

FraudWatch Africa is an **interactive web application** built using Streamlit for monitoring and predicting anomalous transactions on Kenyan mobile money platforms.

**Features:**
- **Home Page:** Project overview with a banner image and welcome message.
- **Dashboard Tab:**  
  - Displays total transactions, flagged anomalies, and % of anomalies.  
  - Interactive table of flagged transactions with **CSV download** option.  
  - Visualizations: anomalies by transaction type and location.  
- **Predict Single Transaction Tab:**  
  - Input transaction details to get a real-time anomaly prediction.  
  - Handles categorical features (foreign number, SIM swap, multiple accounts) automatically.  
- **Batch Prediction Tab:**  
  - Upload CSV files with multiple transactions for bulk anomaly predictions.  
  - Returns predicted anomalies and scores, with **downloadable results**.

**Running Locally:**
```bash
streamlit run app/streamlit_app.py
```

The FastAPI backend enables real-time detection and batch processing of transactions:

Endpoints:

POST /predict – Predicts a single transaction (normal vs. anomalous).

POST /predict_batch – Predicts multiple transactions from uploaded CSV.

GET /transactions – Retrieves filtered transactions for dashboard visualization.

Sample Request for Single Transaction:
```
{
  "transaction_type": "Send Money",
  "amount": 1200.0,
  "location": "Nairobi",
  "device_type": "iOS",
  "network_provider": "Safaricom",
  "user_type": "Agent",
  "is_foreign_number": 0,
  "is_sim_recently_swapped": 1,
  "has_multiple_accounts": 0
}

```
Sample Response:
```
{
  "transaction_id": 12345,
  "is_anomaly": 1,
  "anomaly_score": 0.87
}
```

## 🛠️ Tools & Technologies  

Here’s an overview of the tools and technologies used in this project:  

![Fraud Detection Stack](https://sdmntprwestus3.oaiusercontent.com/files/00000000-7cd8-61fd-b9a9-0b8ec9c35c3f/raw?se=2025-09-17T21%3A28%3A10Z&sp=r&sv=2024-08-04&sr=b&scid=03799171-aaeb-55b0-bb18-89d92b4da473&skoid=f28c0102-4d9d-4950-baf0-4a8e5f6cf9d4&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-09-17T17%3A18%3A58Z&ske=2025-09-18T17%3A18%3A58Z&sks=b&skv=2024-08-04&sig=Shb8AeBM87B9IB/unIjB3F7DOjvcwT5TYNzYPCmS8SE%3D)


