# Project Structure - Sales Analytics Platform

## Directory Organization

This document provides a comprehensive overview of the project structure and organization.

## Root Structure

```
Exercise 7 - Sales Dashboard/
├── .gitignore                  # Git ignore patterns
├── .venv/                      # Python virtual environment (excluded from git)
├── README.md                   # Main project documentation
├── requirements.txt            # Python dependencies (root reference)
├── run.py                      # Main application launcher
│
├── config/                     # Configuration Files
│   └── requirements.txt        # Python package dependencies
│
├── data/                       # Data Management
│   ├── generate_sample_data.py # Sample data generator
│   ├── generate_enterprise_data.py # Enterprise data generator
│   ├── raw/                    # Raw data storage
│   └── processed/              # Processed/cleaned data
│
├── docs/                       # Documentation
│   ├── README.md               # Technical documentation
│   ├── ENTERPRISE_README.md    # Commercial/business documentation
│   ├── PROJECT_STATUS.md       # Current project status
│   ├── PROJECT_COMPLETION_STATUS.md # Completion tracking
│   ├── TECHNICAL_ENHANCEMENTS.md # Technical improvements log
│   ├── CODE_QUALITY_REPORT.md  # Code quality metrics
│   ├── CLEANUP_COMPLETE.md     # Cleanup documentation
│   └── archive/                # Archived/old documents
│
├── docker/                     # Docker Configuration
│   ├── Dockerfile              # Container build instructions
│   └── docker-compose.yml      # Multi-container setup
│
├── logs/                       # Application Logs
│   └── validation_results.json # System validation results
│
├── notebooks/                  # Jupyter Notebooks
│   ├── 01_Exploratory_Data_Analysis.ipynb
│   └── 02_ML_Model_Training.ipynb
│
├── scripts/                    # Utility Scripts
│   ├── run_dashboard.py        # Dashboard startup script
│   ├── quick_setup.py          # Quick installation setup
│   ├── validate_enterprise_systems.py # System validator
│   └── deploy.py               # Deployment automation
│
├── src/                        # Source Code
│   ├── dashboard/              # Dashboard application
│   │   ├── app.py              # Main dashboard app
│   │   ├── enterprise_app.py   # Enterprise version
│   │   └── components/         # UI components
│   │
│   ├── etl/                    # ETL Pipeline
│   │   ├── load.py             # Data loading
│   │   └── transform.py        # Data transformation
│   │
│   ├── features/               # Feature Engineering
│   │   └── features.py         # Feature computation
│   │
│   └── models/                 # Machine Learning Models
│       └── advanced_ml.py      # ML model implementations
│
├── tests/                      # Test Suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
│
└── automation/                 # Legacy automation scripts
    └── dashboard/              # Legacy dashboard files
```

## Directory Purposes

### `/config`
Contains all configuration files including dependencies, environment settings, and application configurations.

### `/data`
Manages all data-related operations:
- **raw/**: Original, unmodified data files
- **processed/**: Cleaned and transformed data ready for analysis
- **Scripts**: Data generation and management utilities

### `/docs`
Comprehensive documentation:
- Technical guides and API documentation
- Business and commercial documentation
- Project status and progress tracking
- Historical documentation in archive/

### `/docker`
Docker containerization files:
- Dockerfile for image building
- docker-compose.yml for orchestration
- Kubernetes manifests (if applicable)

### `/logs`
Application logging and monitoring:
- Runtime logs
- Validation results
- Error tracking
- Performance metrics

### `/notebooks`
Jupyter notebooks for:
- Exploratory data analysis
- Model training and evaluation
- Data visualization
- Research and experimentation

### `/scripts`
Utility and automation scripts:
- Application launchers
- Setup and installation scripts
- Deployment automation
- System validation tools

### `/src`
Main application source code organized by functionality:
- **dashboard/**: Web application and UI
- **etl/**: Extract, Transform, Load pipeline
- **features/**: Feature engineering and computation
- **models/**: Machine learning model implementations

### `/tests`
Comprehensive test suite:
- **unit/**: Individual component tests
- **integration/**: Module integration tests
- **e2e/**: End-to-end workflow tests

## File Naming Conventions

### Python Files
- `snake_case.py` for module names
- `PascalCase` for class names
- `snake_case` for functions and variables

### Documentation
- `UPPERCASE_MARKDOWN.md` for major documentation
- `lowercase_markdown.md` for technical docs
- `README.md` for directory-level documentation

### Data Files
- `snake_case.csv` for data files
- `YYYYMMDD_prefix_name.ext` for dated files
- Clear, descriptive names

## Version Control

Files excluded from version control (see `.gitignore`):
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `data/raw/` and `data/processed/` - Data files
- `logs/*.log` - Log files
- `*.pyc` - Compiled Python
- IDE-specific files

## Quick Navigation

### Starting the Application
```powershell
python run.py
```

### Running Tests
```powershell
pytest tests/
```

### Generating Data
```powershell
python data/generate_sample_data.py
```

### Viewing Documentation
- Main: `README.md`
- Technical: `docs/README.md`
- Commercial: `docs/ENTERPRISE_README.md`

## Maintenance

### Adding New Features
1. Create feature branch
2. Add code to appropriate `/src` subdirectory
3. Add tests to `/tests`
4. Update documentation in `/docs`
5. Update this structure document if needed

### Adding Dependencies
1. Add to `config/requirements.txt`
2. Update root `requirements.txt`
3. Document in `docs/README.md`

### Updating Documentation
1. Update relevant files in `/docs`
2. Keep this structure document current
3. Archive old versions to `/docs/archive`

---

**Last Updated:** October 15, 2025  
**Version:** 1.0.0  
**Maintained By:** Development Team
