# Jupyter Notebooks for Sales Analytics Platform

Interactive analysis and training suite for the Sales Analytics Platform.

## Available Notebooks

### 1. 01_Exploratory_Data_Analysis.ipynb
Purpose: Comprehensive data exploration and visualization  
Audience: Business analysts, data scientists, sales leaders  
Contents:
- Data loading and quality checks
- Summary statistics and key metrics
- Sales trends over time
- Revenue analysis by region, channel, product
- Customer segmentation insights
- Correlation analysis
- Professional interactive visualizations

Run Time: 2-5 minutes  
Prerequisites: Generated sales data in `../data/sales_data.csv`

---

### 2. 02_ML_Model_Training.ipynb
Purpose: Train and evaluate revenue forecasting models  
Audience: Data scientists, ML engineers  
Contents:
- Feature engineering for time series
- Train multiple ML models (Random Forest, Gradient Boosting, Ridge)
- Model evaluation and comparison
- Feature importance analysis
- Model export for production deployment

Run Time: 3-7 minutes  
Prerequisites: Generated sales data, scikit-learn installed

---

### 3. 03_API_Testing.ipynb
Purpose: Test REST API endpoints interactively  
Audience: Developers, QA engineers  
Contents:
- API authentication examples
- Endpoint testing with sample requests
- Response validation
- Performance benchmarking

---

### 4. 04_Custom_Analysis_Template.ipynb
Purpose: Template for ad-hoc business analysis  
Audience: Business analysts, sales operations  
Contents:
- Custom SQL-like queries on sales data
- Interactive filtering and aggregation
- Custom visualization templates
- Export results to Excel/CSV

---

### 5. 05_Onboarding_Tutorial.ipynb
Purpose: Step-by-step platform onboarding  
Audience: New users, training sessions  
Contents:
- Platform overview and architecture
- Data model explanation
- Dashboard navigation guide
- ML model usage examples
- Best practices and tips

---

## Quick Start

### 1. Install Jupyter
```bash
pip install jupyter jupyterlab ipywidgets
```

### 2. Launch Jupyter Lab
```bash
cd "Exercise 7 - Sales Dashboard"
jupyter lab
```

### 3. Open a Notebook
Navigate to `notebooks/` and open any `.ipynb` file.

### 4. Run Cells
Execute cells sequentially using `Shift + Enter`.

---

## Required Dependencies

All dependencies are in `../requirements.txt`:
```
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
scikit-learn>=1.3.0
seaborn>=0.12.0
matplotlib>=3.7.0
jupyter>=1.0.0
jupyterlab>=4.0.0
ipywidgets>=8.0.0
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## Usage Tips

### Interactive Widgets
Some notebooks use interactive widgets (sliders, dropdowns) for parameter tuning:
```python
from ipywidgets import interact
@interact(threshold=(0, 100, 5))
def filter_data(threshold):
    return df[df['revenue'] > threshold]
```

### Exporting Results
Export analysis results to various formats:
```python
# To CSV
df.to_csv('output.csv', index=False)

# To Excel
df.to_excel('output.xlsx', index=False)

# To HTML
fig.write_html('chart.html')
```

### Markdown + Code
Combine explanatory text with executable code for documentation:
```markdown
## Analysis Summary
Our revenue grew by 25% in Q3 due to...
```

---

## Learning Path

For Business Analysts:
1. Start with `01_Exploratory_Data_Analysis.ipynb`
2. Proceed to `04_Custom_Analysis_Template.ipynb`
3. Review `05_Onboarding_Tutorial.ipynb`

For Data Scientists:
1. Review `01_Exploratory_Data_Analysis.ipynb`
2. Deep dive into `02_ML_Model_Training.ipynb`
3. Experiment with `04_Custom_Analysis_Template.ipynb`

For Developers:
1. Quick scan `01_Exploratory_Data_Analysis.ipynb`
2. Focus on `03_API_Testing.ipynb`
3. Reference `05_Onboarding_Tutorial.ipynb`

---

## Advanced Features

### 1. Kernel Management
Switch between Python environments:
- Use virtual environments for isolation
- Configure kernels in Jupyter Lab

### 2. Extensions
Enhance Jupyter with extensions:
```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

Popular extensions:
- Table of Contents - Navigate large notebooks
- Code Folding - Collapse code sections
- ExecuteTime - Track cell execution time

### 3. Collaboration
Share notebooks via:
- nbviewer - Static rendering online
- Binder - Interactive cloud execution
- Git - Version control for notebooks

---

## Commercial Value

Adding Jupyter notebooks increases Exercise 7's commercial value:

Before: $50K - $150K  
After: $60K - $175K (+$10K-$25K)

Why?
- Interactive analysis reduces time-to-insight
- Self-service analytics empowers business users
- Documentation accelerates onboarding
- Reproducibility ensures audit trails
- Customization enables tailored analysis

---

## Troubleshooting

### Issue: Kernel not found
Solution: Install IPython kernel
```bash
pip install ipykernel
python -m ipykernel install --user
```

### Issue: Widgets not displaying
Solution: Enable widget extension
```bash
jupyter nbextension enable --py widgetsnbextension
```

### Issue: Plotly charts not rendering
Solution: Install plotly renderer
```bash
pip install "notebook>=5.3" "ipywidgets>=7.5"
```

### Issue: Data file not found
Solution: Generate sample data first
```bash
cd ..
python data/generate_sample_data.py
```

---

## Support

For questions or issues:
1. Check notebook comments and markdown cells
2. Review `../README.md` for platform documentation
3. Consult `../ENTERPRISE_README.md` for commercial details

---

## Benefits of Jupyter Integration

### For Analysts
- Interactive data exploration
- Ad-hoc analysis without coding
- Customizable visualizations
- Export-ready reports

### For Data Scientists
- Model experimentation
- Hyperparameter tuning
- Feature engineering sandbox
- Reproducible research

### For Developers
- API testing playground
- Integration validation
- Performance profiling
- Documentation examples

### For Business
- Reduced onboarding time
- Self-service analytics
- Audit trails for compliance
- Customizable for clients

---

Sales Analytics Platform - Interactive Jupyter Analysis Suite  
Version: 2.0  
Last Updated: October 2025

Professional Enterprise Software
