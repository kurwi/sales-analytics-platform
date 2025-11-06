"""
Sales Analytics Platform Demo Launcher
Runs the Streamlit app on port 8502 for portfolio integration
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Sales Analytics Streamlit app."""
    project_root = Path(__file__).parent
    streamlit_app = project_root / "streamlit_app.py"
    
    print("=" * 60)
    print("🚀 Starting Sales Analytics Platform Demo")
    print("=" * 60)
    print(f"\n📂 Project: {project_root}")
    print(f"🌐 URL: http://localhost:8502")
    print("\n⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(streamlit_app),
            "--server.port=8502",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ], cwd=str(project_root), check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Sales Analytics Platform stopped by user.")
    except Exception as e:
        print(f"\n❌ Error launching demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
