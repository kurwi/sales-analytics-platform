"""
Quick Setup Script for Enterprise Systems
Installs all required dependencies for Exercise 6 and Exercise 7
"""

import subprocess
import sys
from pathlib import Path

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def install_package(package_name, display_name=None):
    """Install a Python package using pip"""
    display = display_name or package_name
    print(f"📦 Installing {display}...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name, "--quiet"
        ])
        print(f"   ✅ {display} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"   ❌ Failed to install {display}")
        return False

def main():
    """Main setup function"""
    print_header("ENTERPRISE SYSTEMS QUICK SETUP")
    print("This script will install all required Python packages")
    print("for both Exercise 6 and Exercise 7 (located in 'Exercise 7 - Sales Dashboard').\n")
    
    # List of packages to install
    packages = [
        ("scikit-learn", "scikit-learn (Machine Learning)"),
        ("streamlit", "Streamlit (Dashboard Framework)"),
        ("scikit-surprise", "Surprise (Recommendation Library)"),
        ("dash", "Dash (Dashboard Framework)"),
        ("dash-bootstrap-components", "Dash Bootstrap Components"),
    ]
    
    # Install packages
    print_header("INSTALLING PACKAGES")
    
    results = []
    for package, display in packages:
        success = install_package(package, display)
        results.append((display, success))
    
    # Summary
    print_header("INSTALLATION SUMMARY")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    for display, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {display}")
    
    print(f"\n📊 Success Rate: {successful}/{total} packages installed")
    
    if successful == total:
        print("\n✅ All packages installed successfully!")
        print("\n🚀 NEXT STEPS:")
        print("\n1. Generate data for Exercise 6:")
        print("   cd 'Exercise 6 - Product Recommendation System'")
        print("   python data/generate_sample_data.py")
    print("\n2. Generate data for Exercise 7 (using quick_setup.py):")
    print("   cd 'Exercise 7 - Sales Dashboard'")
    print("   python quick_setup.py")
        print("\n3. Run validation again:")
        print("   python validate_enterprise_systems.py")
        print("\n4. Launch dashboards:")
        print("   Exercise 6: streamlit run dashboard/business_analytics.py")
        print("   Exercise 7: python run_dashboard.py")
    else:
        print("\n⚠️  Some packages failed to install.")
        print("Please install them manually using:")
        print("  pip install <package-name>")
    
    return successful == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
