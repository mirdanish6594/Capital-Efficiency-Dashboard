import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Efficiency & Risk", layout="wide")

def get_connection():
    return sqlite3.connect("financial_db.sqlite")

st.title("⚠️ Efficiency & Risk Analysis")

# --- SECTION 1: INVENTORY TURNOVER ---
st.header("1. Working Capital: Inventory Efficiency")
st.write("Identifying 'dead stock' where capital is tied up in slow-moving inventory.")

turnover_query = """
WITH SalesData AS (
    SELECT productCode, SUM(quantityOrdered) as totalSold
    FROM orderdetails
    GROUP BY productCode
)
SELECT 
    p.productName,
    p.productLine,
    p.quantityInStock,
    p.buyPrice,
    (p.quantityInStock * p.buyPrice) AS InventoryValue,
    COALESCE(s.totalSold, 0) AS TotalUnitsSold,
    (CAST(COALESCE(s.totalSold, 0) AS FLOAT) / NULLIF(p.quantityInStock,0)) AS TurnoverRatio
FROM products p
LEFT JOIN SalesData s ON p.productCode = s.productCode
ORDER BY InventoryValue DESC;
"""

conn = get_connection()
df_inv = pd.read_sql(turnover_query, conn)

fig_inv = px.scatter(df_inv, x="TurnoverRatio", y="InventoryValue", 
                     size="buyPrice", color="productLine",
                     hover_name="productName",
                     title="Inventory Matrix: High Value vs. Low Turnover (Risk Quadrant)",
                     labels={"TurnoverRatio": "Turnover Ratio (Higher is Better)", "InventoryValue": "Capital Tied Up ($)"})
st.plotly_chart(fig_inv, use_container_width=True)

# --- SECTION 2: CREDIT RISK ---
st.divider()
st.header("2. Credit Risk: Customer Limit Utilization")
st.write("Customers approaching their credit limit represent potential bad debt risk.")

risk_query = """
WITH CustomerSales AS (
    SELECT 
        c.customerNumber, 
        SUM(od.quantityOrdered * od.priceEach) AS TotalPurchased
    FROM customers c
    JOIN orders o ON c.customerNumber = o.customerNumber
    JOIN orderdetails od ON o.orderNumber = od.orderNumber
    WHERE o.status != 'Cancelled'
    GROUP BY c.customerNumber
)
SELECT 
    c.customerName,
    c.creditLimit,
    (COALESCE(cs.TotalPurchased, 0) - (SELECT COALESCE(SUM(amount),0) FROM payments WHERE customerNumber = c.customerNumber)) AS OutstandingBalance
FROM customers c
LEFT JOIN CustomerSales cs ON c.customerNumber = cs.customerNumber
WHERE c.creditLimit > 0;
"""

df_risk = pd.read_sql(risk_query, conn)
conn.close()

# Calculate Utilization in Pandas
df_risk['Utilization %'] = (df_risk['OutstandingBalance'] / df_risk['creditLimit']) * 100
df_high_risk = df_risk[df_risk['Utilization %'] > 50].sort_values('Utilization %', ascending=False)

col1, col2 = st.columns([1, 2])
with col1:
    st.error(f"High Risk Customers: {len(df_high_risk)}")
    st.dataframe(df_high_risk[['customerName', 'Utilization %', 'OutstandingBalance']], hide_index=True)

with col2:
    if not df_high_risk.empty:
        fig_risk = px.bar(df_high_risk, x='customerName', y='Utilization %', 
                          title="Customers >50% Credit Utilization", color='Utilization %', color_continuous_scale='Reds')
        st.plotly_chart(fig_risk, use_container_width=True)
    else:
        st.success("No customers are currently exceeding risk thresholds.")