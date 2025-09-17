# FraudWatch Africa: Unsupervised Mobile Money Transaction Fraud Detection

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

## 7. Dashboard & Deployment

The **FraudWatch Africa** dashboard provides an interactive interface for exploring, monitoring, and predicting fraudulent transactions in real-time. It is built using **Streamlit** for the frontend and **FastAPI** for backend predictions.

### Live Demo

<p align="left">
  <a href="https://fraudwatchafrica.streamlit.app" target="_blank">
    <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit" alt="Streamlit App"/>
  </a>
  <a href="https://kenya-fraud-detection.onrender.com" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-Endpoint-green?style=for-the-badge&logo=fastapi" alt="FastAPI Endpoint"/>
  </a>
</p>

### 8. Dashboard Features

- **Home Page** – Project introduction and banner.  
- **Dashboard Page** – KPIs, flagged anomalies, filters, and anomaly visualizations.  
- **Predict Transaction Page** – Enter transaction details for single prediction.  
- **Batch Prediction Page** – Upload CSV for batch fraud predictions.  

### Deployment Setup

- **Streamlit** serves as the interactive dashboard frontend.  
- **FastAPI** powers the backend with REST API endpoints.  
- Communication is seamless: the dashboard sends requests to FastAPI for anomaly predictions in real time.  

### Screenshot  

![FraudWatch Africa Dashboard](https://github.com/user-attachments/assets/076c8c9a-1e27-4112-89dc-967884fc0684)

## 9. Tools & Technologies  

Here’s an overview of the tools and technologies used in this project:  

![Fraud Detection Stack](fraud_detection_stack.png)

## 10. Conclusion  

This project demonstrated how **unsupervised learning** can be applied to the challenge of fraud detection in mobile money platforms, especially in environments where **labeled fraud data is scarce**.  

By leveraging **Isolation Forest**, we successfully identified anomalous transactions that may represent fraudulent activity. The results highlighted:  

- Strong potential for detecting unusual transaction behaviors in real time.  
- Practical use of dashboards (Streamlit) for monitoring and decision support.  
- Seamless integration with FastAPI for deployment, ensuring accessibility and scalability.  

The solution emphasizes how **data science can drive financial security** in African markets, protecting millions of users and strengthening trust in mobile money systems.  

## 11. Future Work  

While the current system provides a strong foundation, there are opportunities to make it more powerful and robust:  

- **Enhanced Models:** Experiment with advanced techniques such as Autoencoders, One-Class SVM, and Graph Neural Networks for improved anomaly detection.  
- **Feature Engineering:** Incorporate additional features like transaction velocity, device fingerprinting, and geospatial tracking to capture more complex fraud patterns.  
- **Scalability:** Deploy the system on cloud platforms with distributed data pipelines (e.g., Apache Kafka, Spark) to handle millions of transactions in real time.  
- **User Feedback Loop:** Integrate mechanisms for human investigators to label flagged transactions, creating feedback that strengthens the model over time.  
- **Cross-Border Expansion:** Extend beyond Kenya to support fraud detection across multiple African mobile money markets.  
- **Explainability:** Add interpretable AI components so stakeholders can understand why a transaction is flagged as suspicious.  

This roadmap ensures the solution continues evolving into a **production-grade fraud detection system** that adapts to emerging threats.  



## 12. How to Run the Project  

If you’d like to explore the project locally, follow these steps:  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```
2️⃣ Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate     # On Windows
```

3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
4️⃣ Run the FastAPI Backend
```
uvicorn app.main:app --reload
```
API available at: http://127.0.0.1:8000/docs

5️⃣ Run the Streamlit Dashboard
```
streamlit run app/streamlit_app.py
```
Dashboard available at: http://localhost:8501





