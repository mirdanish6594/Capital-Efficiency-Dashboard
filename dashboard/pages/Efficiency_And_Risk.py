import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
import sys

st.set_page_config(page_title="Efficiency & Risk", layout="wide")

# --- PATH SETUP & ROBUST CONNECTION ---
# 1. Calculate the path to the root 'dashboard' folder
# We are in 'dashboard/pages', so we need to go up one level
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR) # Go up to 'dashboard'
DB_PATH = os.path.join(BASE_DIR, "financial_db.sqlite")

def get_connection():
    """Connects to the database, regenerating it if missing."""
    if not os.path.exists(DB_PATH):
        try:
            # Add base directory to path so we can import data_gen
            if BASE_DIR not in sys.path:
                sys.path.append(BASE_DIR)
            
            from data_gen import create_database
            with st.spinner('Regenerating Financial Database...'):
                create_database()
        except Exception as e:
            st.error(f"Could not generate database: {e}")
            st.stop()
            
    return sqlite3.connect(DB_PATH)

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

try:
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
    if not df_risk.empty:
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
    else:
        st.info("No credit risk data available.")

except Exception as e:
    st.error(f"An error occurred loading data: {e}")
