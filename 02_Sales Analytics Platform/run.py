"""
Sales Dashboard Launcher
Main entry point for running the Sales Analytics Dashboard.
"""
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Sales Analytics Dashboard."""
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Path to the run_dashboard script
    run_script = project_root / "scripts" / "run_dashboard.py"
    
    # Execute the dashboard script
    try:
        subprocess.run([sys.executable, str(run_script)], cwd=str(project_root), check=True)
    except KeyboardInterrupt:
        print("\n\nDashboard stopped by user.")
    except Exception as e:
        print(f"\nError launching dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
