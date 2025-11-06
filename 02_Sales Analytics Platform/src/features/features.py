"""
KPI computation and feature engineering module.

This module provides comprehensive business metric calculations for sales analytics,
including standard e-commerce KPIs, customer segmentation (RFM), and growth metrics.

Functions:
    compute_aov: Calculate Average Order Value
    compute_arpu: Calculate Average Revenue Per User
    compute_repeat_purchase_rate: Calculate customer retention metric
    compute_sales_growth: Calculate period-over-period growth
    compute_all_kpis: Batch compute all standard KPIs
    compute_rfm: Perform RFM segmentation analysis
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

def compute_aov(df: pd.DataFrame) -> float:
    """
    Calculate Average Order Value (AOV).
    
    Args:
        df (pd.DataFrame): Transaction dataset with 'revenue' and 'order_id' columns
    
    Returns:
        float: Average order value in currency units
    
    Raises:
        KeyError: If required columns are missing
    """
    if df.empty:
        logger.warning("Empty dataframe provided to compute_aov")
        return 0.0
        
    total_revenue = df['revenue'].sum()
    orders = df['order_id'].nunique()
    return float(total_revenue / orders) if orders > 0 else 0.0

def compute_arpu(df: pd.DataFrame) -> float:
    """Average Revenue Per User"""
    total_revenue = df['revenue'].sum()
    customers = df['customer_id'].nunique()
    return total_revenue / customers if customers > 0 else 0

def compute_repeat_purchase_rate(df: pd.DataFrame) -> float:
    """Percentage of customers with more than one order"""
    customer_orders = df.groupby('customer_id')['order_id'].nunique()
    repeat_customers = (customer_orders > 1).sum()
    total_customers = len(customer_orders)
    return (repeat_customers / total_customers * 100) if total_customers > 0 else 0

def compute_sales_growth(df: pd.DataFrame, current_period: pd.DataFrame, previous_period: pd.DataFrame) -> float:
    """Sales growth percentage"""
    current_revenue = current_period['revenue'].sum()
    previous_revenue = previous_period['revenue'].sum()
    if previous_revenue > 0:
        return ((current_revenue - previous_revenue) / previous_revenue) * 100
    return 0

def compute_all_kpis(df: pd.DataFrame) -> dict:
    """Compute all KPIs at once"""
    return {
        'total_revenue': df['revenue'].sum(),
        'total_orders': df['order_id'].nunique(),
        'total_customers': df['customer_id'].nunique(),
        'total_qty': df['qty'].sum(),
        'aov': compute_aov(df),
        'arpu': compute_arpu(df),
        'repeat_rate': compute_repeat_purchase_rate(df),
        'avg_qty_per_order': df['qty'].mean()
    }

def compute_rfm(df: pd.DataFrame, reference_date=None) -> pd.DataFrame:
    """Compute RFM (Recency, Frequency, Monetary) for customers"""
    if reference_date is None:
        reference_date = df['date'].max()
    
    rfm = df.groupby('customer_id').agg(
        recency=('date', lambda x: (reference_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('revenue', 'sum')
    ).reset_index()
    
    # Score RFM (1-5 scale)
    rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
    rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
    
    rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
    
    return rfm

if __name__ == "__main__":
    df = pd.read_csv('data/processed/sales_transformed.csv', parse_dates=['date'])
    kpis = compute_all_kpis(df)
    print("KPIs:")
    for key, value in kpis.items():
        print(f"  {key}: {value:,.2f}")
