# Capital Efficiency Dashboard

<div align="center">

![Dashboard Banner](https://img.shields.io/badge/Financial-Analytics-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

**Transform raw sales data into actionable financial intelligence**

[Live Demo](https://capital-efficiency-dashboard-gqj2baegfydjfx5wdirbhg.streamlit.app/) • [Report Issue](https://github.com/mirdanish6594/capital-efficiency-database/issues) • [Request Feature](https://github.com/mirdanish6594/capital-efficiency-database/issues)

</div>

---

## 📊 Overview

This project demonstrates the transformation of raw sales data into strategic financial insights using **Python (Streamlit)** and **SQL (SQLite)**. Built as a real-world financial reporting tool, this interactive dashboard enables stakeholders to analyze **profitability**, **working capital efficiency**, and **credit risk** — moving beyond basic reporting to drive strategic business decisions.

The application mimics enterprise-grade financial systems, allowing users to drill down into profit margins, identify slow-moving inventory, and proactively manage accounts receivable risk.

### 🎯 Business Value

- **CFO-Ready Analytics**: Executive-level KPIs calculated in real-time
- **Capital Optimization**: Identify cash trapped in dead inventory
- **Risk Mitigation**: Prevent bad debt through early credit risk detection
- **Strategic Planning**: Pareto analysis reveals customer concentration risk

---

## ✨ Key Features & Financial Insights

### 1️⃣ CFO Executive Summary
- **Real-Time KPIs**: Dynamic calculation of Total Revenue, Gross Profit, and Overall Margin %
- **Profitability Breakdown**: Product line margin analysis to distinguish high-value segments from volume drivers
- **Trend Visualization**: Interactive charts showing revenue and profit trends over time

### 2️⃣ Efficiency & Working Capital Management
- **Inventory Turnover Analysis**: Quantifies capital locked in slow-moving stock
- **Risk Quadrant Matrix**: Scatter plot identifying high-value, low-turnover inventory requiring immediate action
- **Dead Stock Alerts**: Automated flagging of inventory tying up working capital

### 3️⃣ Credit Risk & Accounts Receivable
- **Credit Utilization Monitoring**: Tracks customer balances against credit limits
- **High-Risk Customer Alerts**: Flags customers exceeding 50% credit utilization
- **AR Aging Analysis**: Prevents bad debt exposure through proactive monitoring

### 4️⃣ Pareto Analysis (80/20 Rule)
- **Revenue Concentration**: Visualizes which customers drive the majority of revenue
- **Customer Segmentation**: Identifies key accounts requiring relationship management
- **Strategic Risk Assessment**: Highlights dependency on small customer base

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **Database** | SQLite (Embedded SQL engine) |
| **Web Framework** | Streamlit |
| **Visualization** | Plotly Express |
| **Data Processing** | Pandas |
| **Deployment** | Streamlit Cloud |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (for cloning)

### Installation

1. **Clone the Repository**
```bash
   git clone https://github.com/mirdanish6594/capital-efficiency-database.git
   cd capital-efficiency-database
```

2. **Install Dependencies**
```bash
   pip install -r requirements.txt
```

3. **Generate the Database**
   
   This script creates a local SQLite database (`financial_db.sqlite`) and populates it with sample data:
```bash
   cd dashboard
   python data_gen.py
```

4. **Launch the Dashboard**
```bash
   streamlit run app.py
```

5. **Access the Application**
   
   Open your browser and navigate to `http://localhost:8501`

### 🌐 Live Demo

Access the deployed application here: **[Capital Efficiency Dashboard](https://capital-efficiency-dashboard-gqj2baegfydjfx5wdirbhg.streamlit.app/)**

---

## 📁 Project Structure
```
capital-efficiency-database/
│
├── dashboard/
│   ├── app.py                          # Main Executive Dashboard (CFO View)
│   ├── data_gen.py                     # ETL Script: Database Generator
│   ├── financial_db.sqlite             # SQLite Database (Auto-generated)
│   │
│   └── pages/
│       ├── 2_Efficiency_&_Risk.py      # Inventory & Credit Risk Analytics
│       └── 3_Pareto_Analysis.py        # Customer Concentration Analysis
│
├── requirements.txt                    # Python Dependencies
├── README.md                          # Project Documentation
└── .gitignore                         # Git Ignore Rules
```

### File Descriptions

- **`app.py`**: Main dashboard featuring executive KPIs, revenue trends, and profitability analysis
- **`data_gen.py`**: Automated ETL script that generates realistic financial data and creates the SQLite database
- **`2_Efficiency_&_Risk.py`**: Working capital and credit risk analysis page
- **`3_Pareto_Analysis.py`**: 80/20 customer revenue concentration analysis
- **`financial_db.sqlite`**: Local database file (generated on first run)

---

## 💡 Use Cases

### For CFOs & Finance Teams
- Monitor real-time profitability metrics
- Identify margin improvement opportunities
- Track working capital efficiency

### For Sales Leadership
- Understand customer revenue concentration
- Identify strategic account relationships
- Optimize credit terms and pricing

### For Operations Managers
- Reduce inventory carrying costs
- Improve inventory turnover ratios
- Eliminate dead stock

### For Credit Analysts
- Proactively manage AR exposure
- Flag high-risk customer accounts
- Prevent bad debt write-offs

---

## 📊 Sample Insights

The dashboard provides answers to critical business questions:

- Which product lines drive the highest margins?
- How much capital is tied up in slow-moving inventory?
- Which customers pose the greatest credit risk?
- What percentage of revenue comes from the top 20% of customers?
- Where should we focus our working capital optimization efforts?

---

## 🔧 Configuration

### Database Customization

To modify the data generation parameters, edit `data_gen.py`:
```python
# Adjust these parameters for different scenarios
num_customers = 100
num_products = 50
num_transactions = 500
```

### Visualization Customization

Chart themes and colors can be modified in the respective page files using Plotly's configuration options.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Danish Mir**

- GitHub: [@mirdanish6594](https://github.com/mirdanish6594)
- LinkedIn: [Connect with me](https://linkedin.com/in/mirdanish6594)

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)
- Database management with [SQLite](https://www.sqlite.org/)

---

## 📧 Support

If you encounter any issues or have questions:

- Open an [Issue](https://github.com/mirdanish6594/capital-efficiency-database/issues)
- Email: mirdanish6594@gmail.com

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by Danish Mir

</div>
