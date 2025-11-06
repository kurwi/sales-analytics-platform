"""
Data transformation and aggregation module
"""
import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform and enrich sales data"""
    df = df.copy()
    
    # Ensure revenue column
    if 'revenue' not in df.columns:
        df['revenue'] = df['qty'] * df['price']
    
    # Standardize region names
    df['region'] = df['region'].str.strip().str.title()
    
    # Extract date components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.dayofweek
    df['week'] = df['date'].dt.isocalendar().week
    
    return df

def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by day"""
    return df.groupby(df['date'].dt.date).agg(
        orders=('order_id', 'nunique'),
        revenue=('revenue', 'sum'),
        qty=('qty', 'sum'),
        customers=('customer_id', 'nunique')
    ).reset_index()

def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by region"""
    return df.groupby('region').agg(
        orders=('order_id', 'nunique'),
        revenue=('revenue', 'sum'),
        customers=('customer_id', 'nunique')
    ).reset_index()

def aggregate_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by product"""
    return df.groupby('product_id').agg(
        orders=('order_id', 'count'),
        revenue=('revenue', 'sum'),
        qty=('qty', 'sum')
    ).reset_index().sort_values('revenue', ascending=False)

if __name__ == "__main__":
    df = pd.read_csv('data/processed/sales_validated.csv', parse_dates=['date'])
    df_transformed = transform_data(df)
    df_transformed.to_csv('data/processed/sales_transformed.csv', index=False)
    print(f"[OK] Transformed {len(df_transformed):,} records")
