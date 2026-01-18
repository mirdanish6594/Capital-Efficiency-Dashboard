import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
import sys

st.set_page_config(page_title="Pareto Analysis", layout="wide")

# --- PATH SETUP & ROBUST CONNECTION ---
# 1. Calculate the path to the root 'dashboard' folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR) # Go up one level to 'dashboard'
DB_PATH = os.path.join(BASE_DIR, "financial_db.sqlite")

def get_connection():
    if not os.path.exists(DB_PATH):
        try:
            if BASE_DIR not in sys.path:
                sys.path.append(BASE_DIR)
            from data_gen import create_database
            with st.spinner('Regenerating Financial Database...'):
                create_database()
        except Exception as e:
            st.error(f"Could not generate database: {e}")
            st.stop()
    return sqlite3.connect(DB_PATH)

st.title("🎯 Pareto Analysis (The 80/20 Rule)")
st.write("Analyzing customer concentration to identify key revenue drivers.")

pareto_query = """
SELECT 
    c.customerName, 
    SUM(od.quantityOrdered * od.priceEach) AS TotalRevenue
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE o.status = 'Shipped'
GROUP BY c.customerName
ORDER BY TotalRevenue DESC;
"""

try:
    conn = get_connection()
    df_pareto = pd.read_sql(pareto_query, conn)
    conn.close()

    if not df_pareto.empty:
        # Calculate Cumulative Percentage
        df_pareto['Cumulative Revenue'] = df_pareto['TotalRevenue'].cumsum()
        df_pareto['Total Revenue Sum'] = df_pareto['TotalRevenue'].sum()
        df_pareto['Cumulative %'] = (df_pareto['Cumulative Revenue'] / df_pareto['Total Revenue Sum']) * 100
        df_pareto['Customer Rank'] = range(1, len(df_pareto) + 1)

        # Pareto Chart
        fig = px.line(df_pareto, x='Customer Rank', y='Cumulative %', title="Revenue Concentration Curve", markers=True)
        fig.add_bar(x=df_pareto['Customer Rank'], y=df_pareto['TotalRevenue'], name='Individual Revenue')
        st.plotly_chart(fig, use_container_width=True)

        # Insight Box
        top_20_pct_count = int(len(df_pareto) * 0.2)
        if top_20_pct_count > 0:
            revenue_from_top_20 = df_pareto.iloc[top_20_pct_count-1]['Cumulative %']
            st.info(f"💡 **Insight:** The top 20% of your customers ({top_20_pct_count} customers) contribute to **{revenue_from_top_20:.1f}%** of your total revenue.")
        else:
            st.info("💡 Not enough data to calculate top 20% impact yet.")
    else:
        st.warning("No sales data available yet.")

except Exception as e:
    st.error(f"An error occurred loading data: {e}")
