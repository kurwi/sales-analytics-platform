#!/usr/bin/env python3
"""
Generate synthetic sales data for dashboard testing
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate dates
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(365)]

# Generate sample data
n_records = 10000
data = {
    'order_id': [f'ORD{i:06d}' for i in range(n_records)],
    'date': np.random.choice(dates, n_records),
    'customer_id': [f'CUST{np.random.randint(1, 2001):04d}' for _ in range(n_records)],
    'product_id': [f'PROD{np.random.randint(1, 501):03d}' for _ in range(n_records)],
    'qty': np.random.randint(1, 11, n_records),
    'price': np.round(np.random.uniform(10, 500, n_records), 2),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_records),
    'channel': np.random.choice(['Online', 'Store', 'Mobile', 'Partner'], n_records)
}

df = pd.DataFrame(data)
df['revenue'] = df['qty'] * df['price']

# Save to CSV
df.to_csv('data/raw/sales_data.csv', index=False)
print(f"[OK] Generated {len(df):,} sales records")
print(f"Total Revenue: ${df['revenue'].sum():,.2f}")
print(f"Unique Customers: {df['customer_id'].nunique():,}")
print(f"Unique Products: {df['product_id'].nunique():,}")
