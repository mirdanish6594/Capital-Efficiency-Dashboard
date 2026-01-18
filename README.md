# Financial Analyst Portfolio: Strategic Performance Dashboard

## 📊 Project Overview
This project demonstrates the transformation of raw sales data into actionable financial intelligence. By leveraging **Python (Streamlit)** and **SQL (SQLite)**, I built an interactive dashboard that moves beyond basic reporting to strategic analysis, focusing on **Profitability**, **Working Capital Efficiency**, and **Credit Risk**.

The application mimics a real-world financial reporting tool, allowing stakeholders to drill down into margins, identify "dead stock," and mitigate accounts receivable risk.

## 🚀 Key Features & Financial Insights

### 1. CFO Executive Summary
* **High-Level KPIs:** Real-time calculation of Total Revenue, Gross Profit, and Overall Margin %.
* **Profitability Analysis:** Break down of gross margins by product line to identify high-value segments versus volume drivers.

### 2. Efficiency & Working Capital Management
* **Inventory Turnover Analysis:** Identifies capital tied up in slow-moving inventory ("Dead Cash").
* **Risk Quadrant Matrix:** A scatter plot visualizing high-value inventory with low turnover ratios, highlighting areas for immediate liquidation or discounting.

### 3. Credit Risk & Accounts Receivable
* **Credit Utilization Monitoring:** Tracks customers' outstanding balances against their credit limits.
* **High-Risk Alerts:** Automatically flags customers exceeding 50% credit utilization to prevent bad debt exposure.

### 4. Pareto Analysis (The 80/20 Rule)
* **Revenue Concentration:** Visualizes customer concentration risk, demonstrating that a small percentage of customers often drive the majority of revenue.

## 🛠️ Technical Stack
* **Language:** Python 3.9+
* **Database:** SQLite (Embedded SQL engine for portability)
* **Visualization:** Plotly Express (Interactive financial charting)
* **Framework:** Streamlit (Web application framework)
* **Data Manipulation:** Pandas (ETL and dataframe management)

## ⚙️ How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/mirdanish6594/Data-analysis-in-a-model-car-database.git](https://github.com/mirdanish6594/Data-analysis-in-a-model-car-database.git)
    cd Data-analysis-in-a-model-car-database
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate the Database**
    This script creates a local SQLite database (`financial_db.sqlite`) and populates it with clean sample data to ensure the dashboard runs immediately without server configuration.
    ```bash
    cd dashboard
    python data_gen.py
    ```

4.  **Launch the Dashboard**
    ```bash
    streamlit run app.py
    ```

## 📁 Project Structure
```text
├── dashboard/
│   ├── app.py                  # Main Executive Dashboard (CFO View)
│   ├── data_gen.py             # ETL Script: Generates SQLite Database
│   ├── financial_db.sqlite     # The Database (Created on run)
│   └── pages/
│       ├── 2_Efficiency_&_Risk.py   # Inventory & Credit Risk Analysis
│       └── 3_Pareto_Analysis.py     # 80/20 Customer Analysis
├── requirements.txt            # Python dependencies
└── README.md                   # Project Documentation
```

### **Final Step: Run the Setup**
1.  Paste the content above into `requirements.txt` and `README.md`.
2.  Install the libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the generator:
    ```bash
    cd dashboard
    python data_gen.py
    ```
4.  Run the app:
    ```bash
    streamlit run app.py
    ```