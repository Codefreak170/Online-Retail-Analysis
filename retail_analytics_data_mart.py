# =====================================================
# SQL ANALYSIS + DATA PREP FOR POWER BI
# =====================================================

import sqlite3
import pandas as pd


DB_NAME = "online_retail_clean.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def run_query(connection, query):
    return pd.read_sql_query(query, connection)


with sqlite3.connect(DB_NAME) as conn:

    # =================================================
    # SALES SUMMARY
    # =================================================
    sales_query = """
        SELECT 
            customer_id,
            invoice,
            description,
            country,
            year,
            month,
            week,
            price,
            quantity AS total_quantity,
            quantity * price AS total_revenue,
            invoicedate
        FROM retail_data
        WHERE quantity > 0
    """
    sales_summary = run_query(conn, sales_query)


    # =================================================
    # PRODUCT PERFORMANCE
    # =================================================
    product_query = """
        SELECT 
            invoice,
            stockcode,
            description,
            quantity AS total_quantity
        FROM retail_data
        WHERE quantity > 0
        ORDER BY total_quantity DESC
    """
    products_by_quantity = run_query(conn, product_query)


    # =================================================
    # CUSTOMER ACTIVITY
    # =================================================
    customer_query = """
        SELECT 
            customer_id,
            SUM(quantity * price) AS total_spent,
            MAX(invoicedate) AS last_purchase_date,
            COUNT(DISTINCT year || '-' || month) AS active_months
        FROM retail_data
        WHERE quantity > 0
        GROUP BY customer_id
        ORDER BY total_spent DESC
    """
    customer_activity = run_query(conn, customer_query)


    # =================================================
    # RETURNS SUMMARY
    # =================================================
    returns_query = """
        SELECT 
            customer_id,
            invoice,
            country,
            year,
            month,
            week,
            stockcode,
            description,
            price,
            quantity AS total_returns_quantity,
            quantity * price AS total_returns_value,
            invoicedate
        FROM retail_data
        WHERE quantity < 0
    """
    returns_summary = run_query(conn, returns_query)


# =====================================================
# EXPORT TO CSV (FOR POWER BI)
# =====================================================

sales_summary.to_csv("sales_summary.csv", index=False)
products_by_quantity.to_csv("products_by_quantity.csv", index=False)
customer_activity.to_csv("customer_activity.csv", index=False)
returns_summary.to_csv("returns_summary.csv", index=False)
