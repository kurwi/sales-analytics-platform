#!/usr/bin/env python3
"""
Quick start script for Sales Dashboard
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    print("Sales Dashboard Quick Start")
    print("=" * 50)
    
    # Step 1: Generate data
    print("\n[1/4] Generating sample data...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'data/generate_sample_data.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
            print("[OK] Sample data generated")
        else:
            print(f"[ERROR] Data generation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Data generation failed: {e}")
        return False
    
    # Step 2: Load and validate
    print("\n[2/4] Loading and validating data...")
    try:
        from src.etl.load import load_csv, validate_and_save
        df = load_csv('data/raw/sales_data.csv')
        validate_and_save(df, 'data/processed/sales_validated.csv')
        print("[OK] Data validated")
    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        return False
    
    # Step 3: Transform
    print("\n[3/4] Transforming data...")
    try:
        from src.etl.transform import transform_data
        import pandas as pd
        df = pd.read_csv('data/processed/sales_validated.csv', parse_dates=['date'])
        df_transformed = transform_data(df)
        df_transformed.to_csv('data/processed/sales_transformed.csv', index=False)
        print("[OK] Data transformed")
    except Exception as e:
        print(f"[ERROR] Transformation failed: {e}")
        return False
    
    # Step 4: Launch dashboard
    print("\n[4/4] Launching dashboard...")
    print("\n" + "="*50)
    print("SUCCESS! Dashboard running at:")
    print("http://localhost:8582")
    print("="*50)
    print("Press Ctrl+C to stop\n")
    
    try:
        from src.dashboard.app import app
        app.run(debug=False, host='0.0.0.0', port=8582)
    except KeyboardInterrupt:
        print("\n\n[STOP] Dashboard stopped")
    except Exception as e:
        print(f"[ERROR] Dashboard failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
        sys.exit(1)
