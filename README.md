# RFM Analysis (Python)

## 📌 Project Overview

This project performs RFM (Recency, Frequency, Monetary) Analysis using Python to understand customer purchasing behavior and segment customers into meaningful groups.

RFM Analysis is a powerful technique widely used in data science and marketing to evaluate customer engagement, loyalty, and overall value to a business. By analyzing customer transactions, this project helps identify high-value customers, loyal customers, and those at risk of churn.

---

## 📊 What is RFM Analysis?

RFM stands for:

* **Recency (R)** – How recently a customer made their last purchase
* **Frequency (F)** – How often a customer makes purchases
* **Monetary Value (M)** – How much money a customer spends

Using these three metrics, businesses can better understand customer behavior and create targeted marketing strategies.

---

## 📂 Dataset Description

The dataset used in this project contains the following fields:

* **Customer ID** – Unique identifier for each customer
* **Purchase Date** – Date of transaction
* **Transaction Amount** – Amount spent in each transaction
* **Product Information** – Details about purchased products
* **Order ID** – Unique identifier for each order
* **Location** – Customer or transaction location

---

## 🎯 Objectives

* Calculate Recency, Frequency, and Monetary values for each customer
* Segment customers into different groups based on RFM scores
* Identify high-value and loyal customers
* Detect inactive or at-risk customers
* Provide actionable insights for marketing strategies

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Plotly
* Pycharm

---

## 🔍 Key Steps in Analysis

### 1. Data Preprocessing

* Handling missing values
* Converting purchase dates to datetime format
* Cleaning and structuring transaction data

### 2. RFM Metric Calculation

* **Recency**: Days since last purchase
* **Frequency**: Total number of transactions
* **Monetary**: Total spending per customer

### 3. RFM Scoring

* Assigning scores to R, F, and M values (e.g., 1–5 scale)
* Creating combined RFM score for segmentation

### 4. Customer Segmentation

* Grouping customers into segments such as:

  * High-value customers
  * Loyal customers
  * Potential customers
  * At-risk customers

### 5. Visualization

* Distribution plots for RFM metrics
* Customer segment visualization
* Heatmaps and bar charts

---

## 📈 Insights & Findings

* Identification of top-performing customer segments
* Recognition of customers who need re-engagement
* Understanding spending patterns and purchase frequency
* Insights into customer lifecycle stages

---

## 📌 Future Improvements

* Apply machine learning clustering (K-Means) for advanced segmentation
* Build a dashboard using Streamlit or Power BI
* Automate RFM scoring for real-time analytics

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## 🙌 Acknowledgements

* Data Science and Marketing Analytics community
* Open-source Python ecosystem

---

## 📬 Contact

For any questions or suggestions, feel free to reach out. Email ID: sohailzareen279@gmail.com
