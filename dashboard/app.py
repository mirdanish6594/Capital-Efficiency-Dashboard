import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
import sys

# --- PAGE CONFIG ---
st.set_page_config(page_title="CFO Dashboard", layout="wide")

# --- PATH SETUP & SELF-HEALING DATABASE ---
# Get the absolute path of the folder where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to the database
DB_PATH = os.path.join(BASE_DIR, "financial_db.sqlite")

def get_connection():
    """
    Connects to the SQLite database.
    If the database file doesn't exist, it triggers the generation script.
    """
    if not os.path.exists(DB_PATH):
        # If not, we need to generate it.
        try:
            # Add current directory to path so we can import local modules
            if BASE_DIR not in sys.path:
                sys.path.append(BASE_DIR)
            
            # Import the generator function from data_gen.py
            from data_gen import create_database
            
            with st.spinner('Generating Financial Database for the first time...'):
                create_database()
        except ImportError:
            st.error("Could not find data_gen.py to generate the database.")
            st.stop()
        except Exception as e:
            st.error(f"Error creating database: {e}")
            st.stop()
            
    # Connect to the database using the absolute path
    return sqlite3.connect(DB_PATH)

@st.cache_data
def get_financial_data():
    """Fetch Profitability & Margin Analysis"""
    try:
        conn = get_connection()
        query = """
        SELECT 
            p.productLine, 
            SUM(od.quantityOrdered * od.priceEach) AS Revenue,
            SUM(od.quantityOrdered * p.buyPrice) AS CostOfGoodsSold,
            SUM(od.quantityOrdered * (od.priceEach - p.buyPrice)) AS GrossProfit
        FROM products p
        JOIN orderdetails od ON p.productCode = od.productCode
        JOIN orders o ON od.orderNumber = o.orderNumber
        WHERE o.status = 'Shipped'
        GROUP BY p.productLine;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# --- DASHBOARD LAYOUT ---
st.title("📊 Financial Performance Executive Summary")
st.markdown("Financial health overview focusing on **Profitability**, **Margins**, and **Revenue Composition**.")

# Load Data
df = get_financial_data()

if not df.empty:
    # 1. TOP ROW KPIs
    total_revenue = df['Revenue'].sum()
    total_profit = df['GrossProfit'].sum()
    total_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Gross Profit", f"${total_profit:,.0f}")
    col3.metric("Overall Margin", f"{total_margin:.1f}%")

    st.divider()

    # 2. CHARTS ROW
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Profitability by Product Line")
        # Calculate margin per line for the chart
        df['Margin %'] = (df['GrossProfit'] / df['Revenue']) * 100
        
        fig = px.bar(df, x='productLine', y='Revenue', title="Revenue vs. Margin %",
                     hover_data=['GrossProfit', 'Margin %'], color='Revenue')
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("Profit Contribution")
        fig2 = px.pie(df, values='GrossProfit', names='productLine', hole=0.4,
                      title="Share of Total Gross Profit")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data found. Please ensure the database generation script ran successfully.")
