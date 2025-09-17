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

## Dataset  

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
## Methodology  

### Exploratory Data Analysis (EDA)  
The EDA phase helped uncover key transaction behaviors and potential fraud patterns:  

- **Amount Analysis**:  
  - Mean = 3,496.41 | Std Dev = 3,507.29 | Min = 0.03 | Max = 30,221.30  
  - Distribution is **right-skewed** (skewness = 1.95).  
  - Log transformation produced a more **normally distributed variable**, useful for modeling.
  - 
![Amount Distribution](https://github.com/user-attachments/assets/8bcb173f-cf51-4a15-b579-b2bcea5f1ee2)


  
 ![Log-Scaled Amount Distribution](https://github.com/user-attachments/assets/8cae5a48-7465-4ba3-adac-1a9eab3c6ce5) 

- **Time of Day Trends**:  
  Most transactions occur at **night**, suggesting heightened monitoring is required during peak hours.  
  ![Time of Day Trends](https://github.com/user-attachments/assets/8c57592b-49be-4a95-8f1f-ab3dec4b86f6)  

- **Day of the Week**:  
  Saturdays show the highest number of transactions (~1,750), while weekdays remain stable (~1,300–1,450).
    
  ![Day of Week Transactions](https://github.com/user-attachments/assets/c6420c8c-6d16-41d6-8f9f-743e8ab974ea)

   

- **Locations**:  
  Eldoret, Mombasa, and Kisumu show slightly higher transaction amounts compared to other cities.  
  ![Transaction Amount by Location](https://github.com/user-attachments/assets/4f838039-141a-4e43-b5bf-dfa502dceec2)


---

### Data Preprocessing  
1. **Cleaning** – handled missing values, corrected data types.  
2. **Feature Scaling** – applied scaling to numerical features (e.g., transaction amount).  
3. **Transformation** – added engineered features such as log(amount), time of day, and transaction frequency.  

---

### Modeling 
- We used the Isolation Forest algorithm to detect unusual transactions. Since this is an unsupervised model, it doesn’t need pre-labeled fraud cases; instead, it learns what “normal” behavior looks like and flags outliers.

- Visualizing Model Results
- **Blue dots** represent transactions the model classified as **normal.**
- **Red dots** represent **anomalies** flagged by the model.

**t-SNE Plot**

This projects high-dimensional transaction data into 2D for easier visualization.
The result: normal transactions form tight clusters, while anomalies appear at the edges or are isolated, confirming they behave differently.

![t-SNE Plot](https://github.com/user-attachments/assets/8e9a8482-7f4b-41d8-9432-42f778a2551f)

**UMAP Plot**

Another dimensionality reduction method, preserving both local and global structures.

Similar to t-SNE, UMAP shows anomalies separated from dense clusters of normal transactions, reinforcing the model’s accuracy.
 
  ![UMAP Plot](https://github.com/user-attachments/assets/7a14cda3-3003-4589-91ab-8bea128c3ac7)

- Model parameters (e.g., contamination rate) were tuned for better detection.  


