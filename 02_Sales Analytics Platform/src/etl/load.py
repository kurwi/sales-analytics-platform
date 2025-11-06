"""
Data loading and validation module
"""
import pandas as pd
from pathlib import Path

REQUIRED_COLS = {'order_id', 'date', 'customer_id', 'product_id', 'qty', 'price', 'region', 'channel'}

def load_csv(path: str) -> pd.DataFrame:
    """Load and validate CSV data"""
    df = pd.read_csv(path, parse_dates=['date'])
    assert REQUIRED_COLS.issubset(df.columns), f"Missing required columns: {REQUIRED_COLS - set(df.columns)}"
    return df.drop_duplicates()

def validate_and_save(df: pd.DataFrame, out_path: str):
    """Validate data types and save to CSV"""
    df['qty'] = df['qty'].astype(int)
    df['price'] = df['price'].astype(float)
    
    # Add revenue if not present
    if 'revenue' not in df.columns:
        df['revenue'] = df['qty'] * df['price']
    
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    # Use CSV instead of parquet for faster setup
    out_path_csv = out_path.replace('.parquet', '.csv')
    df.to_csv(out_path_csv, index=False)
    print(f"[OK] Validated and saved {len(df):,} records to {out_path_csv}")

if __name__ == "__main__":
    df = load_csv('data/raw/sales_data.csv')
    validate_and_save(df, 'data/processed/sales_validated.csv')
