"""
Setup configuration for Sales Analytics Platform
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding='utf-8').splitlines()

setup(
    name="sales-analytics-platform",
    version="1.0.0",
    author="Development Team",
    author_email="team@salesanalytics.com",
    description="Enterprise B2B Sales Analytics Platform with ML-powered forecasting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourorg/sales-analytics-platform",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sales-dashboard=scripts.run_dashboard:main",
            "sales-setup=scripts.quick_setup:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="sales analytics machine-learning forecasting b2b dashboard",
    project_urls={
        "Documentation": "https://github.com/yourorg/sales-analytics-platform/docs",
        "Source": "https://github.com/yourorg/sales-analytics-platform",
        "Tracker": "https://github.com/yourorg/sales-analytics-platform/issues",
    },
)
