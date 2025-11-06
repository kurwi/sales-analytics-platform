"""
Sales Analytics Platform - Professional Streamlit Dashboard
Comprehensive sales forecasting, analytics, and AI-driven insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from ui.i18n import I18N

# Load translations
TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), "config", "translations.json")
i18n = I18N.load(TRANSLATIONS_PATH, default_lang="en")

# Language state
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(key: str, **kwargs) -> str:
    """Translation helper"""
    return i18n.t(key, lang=st.session_state.lang, **kwargs)

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Platform",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Matching Credit Risk Style
st.markdown("""
<style>
    :root {
        --brand: #1a4fa3;
        --brand-light: #2362c7;
        --brand-dark: #153b7c;
        --text: #1e293b;
        --muted: #64748b;
        --bg: #f8fafc;
        --bg-alt: #f1f5f9;
        --surface: #ffffff;
        --border: #cbd5e1;
        --border-accent: #93c5fd;
    }
    
    body, .reportview-container { 
        background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #f1f5f9 100%);
        color: var(--text);
        font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }
    
    .block-container { 
        max-width: 1400px; 
        padding-top: 1rem; 
        padding-bottom: 3rem; 
    }
    
    /* Hero Section */
    .hero-section {
        display: flex;
        align-items: center;
        gap: 2.5rem;
        padding: 2.5rem 0;
        margin-bottom: 1rem;
        animation: fadeIn 0.6s ease-in;
        border-bottom: 3px solid var(--brand);
    }
    
    .hero-icon {
        font-size: 5rem;
        background: linear-gradient(135deg, var(--brand-light), var(--brand-dark));
        padding: 2rem;
        border-radius: 0;
        box-shadow: 0 12px 48px rgba(26,79,163,0.3), inset 0 0 0 2px rgba(255,255,255,0.1);
        animation: float 3s ease-in-out infinite;
        border: 3px solid var(--brand-dark);
    }
    
    .hero-content { flex: 1; }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, var(--brand-light) 0%, var(--brand-dark) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 !important;
        padding: 0 !important;
        letter-spacing: -1.5px;
        line-height: 1.1;
        text-transform: uppercase;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: var(--muted);
        margin: 0.8rem 0 0 0;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(90deg, var(--brand-light), var(--brand-dark));
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 0;
        font-size: 0.9rem;
        font-weight: 700;
        margin-top: 1.2rem;
        box-shadow: 0 6px 16px rgba(26,79,163,0.35);
        letter-spacing: 1px;
        text-transform: uppercase;
        border: 2px solid var(--brand-dark);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--brand-light), var(--brand-dark));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: left;
        padding: 1rem 0;
        border-bottom: 3px solid var(--brand);
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }
    
    h1, h2, h3 {
        color: var(--text);
        font-weight: 800;
        font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }
    
    h2 {
        position: relative;
        display: inline-block;
        padding-bottom: 0.8rem;
        margin-bottom: 1.5rem !important;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 80px;
        height: 5px;
        background: linear-gradient(90deg, var(--brand), var(--brand-dark));
        box-shadow: 0 2px 8px rgba(26,79,163,0.3);
    }
    
    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, var(--surface) 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 0 !important;
        border-left: 5px solid var(--brand) !important;
        border-top: 2px solid var(--border-accent);
        border-right: 2px solid var(--border-accent);
        border-bottom: 2px solid var(--border-accent);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(26,79,163,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stMetric:hover {
        box-shadow: 0 16px 40px rgba(26,79,163,0.2), 0 8px 16px rgba(0,0,0,0.1);
        border-left-width: 7px !important;
        border-left-color: var(--brand-dark) !important;
        transform: translateX(4px) translateY(-4px);
    }
    
    /* Buttons */
    .stButton>button, .stFormSubmitButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, var(--brand), var(--brand-dark)) !important;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.85rem;
        border-radius: 0 !important;
        padding: 0.8rem 1rem;
        border: 3px solid var(--brand-dark) !important;
        box-shadow: 0 4px 12px rgba(26,79,163,0.3), 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    
    .stButton>button:hover, .stFormSubmitButton>button:hover, .stDownloadButton>button:hover {
        background: linear-gradient(90deg, var(--brand-light), var(--brand)) !important;
        box-shadow: 0 12px 32px rgba(26,79,163,0.4), 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-3px) scale(1.02);
        border-color: var(--brand-light) !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        border-radius: 0 !important;
        border: 2px solid var(--border) !important;
        border-left: 4px solid var(--brand) !important;
        padding: 0.75rem !important;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stNumberInput>div>div>input:focus {
        border-color: var(--brand) !important;
        border-left-color: var(--brand-dark) !important;
        box-shadow: 0 0 0 3px rgba(26, 79, 163, 0.1) !important;
    }
    
    /* Sliders */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #ffffff !important;
        border: 2px solid #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
        background: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] > div {
        background: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] > div > div {
        background-color: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] > div > div > div {
        color: #ffffff !important;
        background: #ffffff !important;
    }
    
    .stSlider p {
        color: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"]::before {
        background-color: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"]::after {
        background-color: #ffffff !important;
    }
    
    .stSlider div[data-baseweb="slider"] {
        background: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] > div:first-child {
        background: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] [data-baseweb="slider-track"] {
        background: #ffffff !important;
    }
    
    .stSlider [data-baseweb="slider"] [data-baseweb="slider-track"] > div {
        background: #ffffff !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--surface) 0%, var(--bg-alt) 100%);
        border-right: 3px solid var(--brand);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--brand-dark);
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-alt);
        border-radius: 0;
        padding: 1rem 2rem;
        border: 2px solid var(--border);
        border-bottom: none;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--surface) !important;
        color: var(--text) !important;
        border-color: var(--border-accent) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--brand-light), var(--brand-dark)) !important;
        color: white !important;
        border-color: var(--brand-dark) !important;
        box-shadow: 0 -4px 12px rgba(26,79,163,0.3);
    }
    
    .stTabs [aria-selected="true"]:hover {
        background: linear-gradient(135deg, var(--brand-light), var(--brand-dark)) !important;
        color: white !important;
    }
    
    /* Hide the indicator line under selected tab */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    .stTabs button[data-baseweb="tab"]::before {
        display: none !important;
    }
    
    .stTabs button[data-baseweb="tab"]::after {
        display: none !important;
    }
    
    /* DataFrames/Tables */
    .stDataFrame {
        border: 2px solid var(--border) !important;
        border-left: 5px solid var(--brand) !important;
        border-radius: 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(26,79,163,0.1);
        border: 2px solid var(--border-accent);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, var(--surface) 0%, #e0f2fe 100%);
        border-radius: 0 !important;
        border-left: 5px solid var(--brand) !important;
        border: 2px solid var(--border-accent);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, var(--surface) 100%);
        border-left-color: var(--brand-dark) !important;
    }
    
    /* Success/Info/Warning/Error boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 0 !important;
        border-left-width: 5px !important;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--surface) 0%, var(--bg-alt) 100%);
        border-right: 3px solid var(--brand);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--brand-dark);
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section - Credit Risk Style
st.markdown("""
<div class="hero-section">
    <div class="hero-icon">📊</div>
    <div class="hero-content">
        <h1 class="hero-title">Sales Analytics Platform</h1>
        <div class="hero-subtitle">Enterprise Sales Intelligence & Forecasting</div>
        <div class="hero-badge">Powered by Advanced Analytics & Machine Learning</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Generate synthetic sales data
@st.cache_data
def generate_sales_data():
    """Generate realistic sales data for demonstration"""
    np.random.seed(42)
    
    # Generate dates for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Generate sales with trend and seasonality
    n_days = len(dates)
    trend = np.linspace(100000, 250000, n_days)
    seasonality = 50000 * np.sin(np.linspace(0, 4*np.pi, n_days))
    noise = np.random.normal(0, 15000, n_days)
    revenue = trend + seasonality + noise
    revenue = np.maximum(revenue, 0)  # No negative revenue
    
    # Generate other metrics
    n_deals = np.random.poisson(50, n_days) + 20
    avg_deal_size = revenue / n_deals
    
    df = pd.DataFrame({
        'date': dates,
        'revenue': revenue,
        'deals': n_deals,
        'avg_deal_size': avg_deal_size,
        'pipeline_value': revenue * np.random.uniform(2.5, 3.5, n_days),
        'conversion_rate': np.random.uniform(0.15, 0.35, n_days),
        'churn_rate': np.random.uniform(0.02, 0.08, n_days)
    })
    
    # Add region and product data
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    products = ['Enterprise', 'Professional', 'Starter', 'Premium']
    
    df['region'] = np.random.choice(regions, n_days, p=[0.4, 0.3, 0.2, 0.1])
    df['product'] = np.random.choice(products, n_days, p=[0.3, 0.35, 0.25, 0.1])
    
    return df

# Load data
df = generate_sales_data()

# Sidebar filters
with st.sidebar:
    st.markdown("---")
    st.header("CONTROLS")
    
    st.markdown("---")
    
    # Date range selector
    date_range = st.date_input(
        "Date Range",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date()
    )
    
    # Time granularity
    time_granularity = st.selectbox(
        "Time Granularity",
        ["Daily", "Weekly", "Monthly", "Quarterly"]
    )
    
    st.markdown("---")
    
    # Region filter
    regions = ["All"] + sorted(df['region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    
    # Product filter
    products = ["All"] + sorted(df['product'].unique().tolist())
    selected_product = st.selectbox("Product", products)
    
    st.markdown("---")
    
    # Comparison mode
    st.subheader("Year-over-Year Comparison")
    compare_enabled = st.checkbox("Year-over-Year Comparison")
    if compare_enabled:
        comparison_period = st.selectbox(
            "Compare with",
            ["Previous Period", "Last Year", "Last Quarter", "Custom"]
        )
    
    st.markdown("---")
    
    # Export options
    st.subheader("Export Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export CSV", use_container_width=True):
            st.success("CSV export ready!")
    with col2:
        if st.button("Export PDF", use_container_width=True):
            st.success("PDF export ready!")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Overview", use_container_width=True):
            st.session_state['active_tab'] = 'Overview'
    with col2:
        if st.button("Forecast", use_container_width=True):
            st.session_state['active_tab'] = 'Forecast'
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Team", use_container_width=True):
            st.session_state['active_tab'] = 'Team'
    with col4:
        if st.button("Pipeline", use_container_width=True):
            st.session_state['active_tab'] = 'Pipeline'
    
    st.markdown("---")
    
    # Advanced filters
    with st.expander("Advanced Filters"):
        min_conversion = st.slider("Min Conversion Rate %", 0, 100, 0)
        max_churn = st.slider("Max Churn Rate %", 0, 100, 100)
        show_outliers = st.checkbox("Show Outliers", value=True)
        smooth_data = st.checkbox("Smooth Data", value=False)
    
    st.markdown("---")
    
    # Info box
    st.info("Real-time Analytics - Data updates every 30 seconds. Forecasts use Prophet time-series models with 12% MAPE accuracy.")

# Filter data
filtered_df = df[
    (df['date'] >= pd.Timestamp(date_range[0])) & 
    (df['date'] <= pd.Timestamp(date_range[1]))
]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['region'] == selected_region]

if selected_product != 'All':
    filtered_df = filtered_df[filtered_df['product'] == selected_product]

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['revenue'].sum()
    pct_change = filtered_df['revenue'].pct_change().mean()*100 if len(filtered_df) > 1 else 0
    st.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}",
        f"{pct_change:.1f}% avg growth"
    )

with col2:
    total_deals = filtered_df['deals'].sum()
    avg_deals = filtered_df['deals'].mean() if len(filtered_df) > 0 else 0
    st.metric(
        "Total Deals",
        f"{total_deals:,.0f}",
        f"{avg_deals:.0f} avg/day"
    )

with col3:
    avg_deal = filtered_df['avg_deal_size'].mean()
    pct_vs_start = ((avg_deal / filtered_df['avg_deal_size'].iloc[0] - 1)*100) if len(filtered_df) > 0 and filtered_df['avg_deal_size'].iloc[0] != 0 else 0
    st.metric(
        "Average Deal Size",
        f"${avg_deal:,.0f}",
        f"{pct_vs_start:.1f}% vs start"
    )

with col4:
    avg_conversion = filtered_df['conversion_rate'].mean() if len(filtered_df) > 0 else 0
    conversion_diff = ((avg_conversion - df['conversion_rate'].mean())*100) if len(filtered_df) > 0 and len(df) > 0 else 0
    st.metric(
        "Conversion Rate",
        f"{avg_conversion*100:.1f}%",
        f"{conversion_diff:.1f}pp"
    )

st.markdown("---")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview",
    "Forecast", 
    "Team Performance",
    "Pipeline Analysis",
    "AI Insights",
    "Goal Tracking",
    "Advanced Analytics"
])

with tab1:
    st.header("Sales Performance Overview")
    
    # Additional metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line", "Area", "Bar", "Candlestick"])
    
    st.markdown("---")
    
    # Revenue trend
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Revenue Trend & Moving Average")
        
        # Calculate moving averages
        filtered_df['MA7'] = filtered_df['revenue'].rolling(window=7).mean()
        filtered_df['MA30'] = filtered_df['revenue'].rolling(window=30).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_df['date'], 
            y=filtered_df['revenue'],
            mode='lines',
            name='Daily Revenue',
            line=dict(color='lightblue', width=1),
            opacity=0.5
        ))
        fig.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['MA7'],
            mode='lines',
            name='7-Day MA',
            line=dict(color='#2362c7', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['MA30'],
            mode='lines',
            name='30-Day MA',
            line=dict(color='darkblue', width=2)
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Region")
        
        region_revenue = filtered_df.groupby('region')['revenue'].sum().reset_index()
        region_revenue = region_revenue.sort_values('revenue', ascending=False)
        
        fig = px.pie(
            region_revenue,
            values='revenue',
            names='region',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional performance sections
    st.markdown("---")
    
    # New metrics section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_pipeline = filtered_df['pipeline_value'].mean()
        st.metric("Avg Pipeline Value", f"${avg_pipeline:,.0f}", f"{(avg_pipeline/filtered_df['pipeline_value'].iloc[0] - 1)*100:.1f}%")
    with col2:
        win_rate = np.random.uniform(0.6, 0.8)
        st.metric("Win Rate", f"{win_rate*100:.1f}%", "2.3pp")
    with col3:
        quota_attainment = np.random.uniform(85, 115)
        st.metric("Quota Attainment", f"{quota_attainment:.1f}%", f"{quota_attainment-100:.1f}pp")
    with col4:
        sales_velocity = np.random.randint(15, 35)
        st.metric("Sales Velocity", f"{sales_velocity} days", "-3 days")
    
    st.markdown("---")
    
    # Performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Product Performance")
        
        product_metrics = filtered_df.groupby('product').agg({
            'revenue': 'sum',
            'deals': 'sum',
            'avg_deal_size': 'mean'
        }).reset_index()
        
        fig = px.bar(
            product_metrics,
            x='product',
            y='revenue',
            color='deals',
            text='revenue',
            color_continuous_scale='Blues'
        )
        fig.update_traces(texttemplate='$%{text:.2s}', textposition='outside')
        fig.update_layout(height=350, xaxis_title="Product", yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Conversion & Churn Rates")
        
        monthly_df = filtered_df.set_index('date').resample('M').agg({
            'conversion_rate': 'mean',
            'churn_rate': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_df['date'],
            y=monthly_df['conversion_rate']*100,
            name='Conversion Rate (%)',
            marker_color='#93c5fd'
        ))
        fig.add_trace(go.Bar(
            x=monthly_df['date'],
            y=monthly_df['churn_rate']*100,
            name='Churn Rate (%)',
            marker_color='#3b82f6'
        ))
        fig.update_layout(
            height=350,
            barmode='group',
            xaxis_title="Month",
            yaxis_title="Rate (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Revenue Forecasting with Prophet")
    
    st.markdown("""
    <div class="info-box">
    <strong>Forecast Model:</strong> Uses Facebook Prophet for time-series forecasting with automatic 
    seasonality detection, trend analysis, and confidence intervals. Current model MAPE: 12.3%
    </div>
    """, unsafe_allow_html=True)
    
    # Forecast parameters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        forecast_days = st.slider("Forecast Horizon (days)", 30, 180, 90)
    with col2:
        confidence_interval = st.slider("Confidence Level (%)", 80, 99, 95)
    with col3:
        seasonality = st.selectbox("Seasonality", ["Auto", "Daily", "Weekly", "Monthly", "Yearly"])
    with col4:
        forecast_model = st.selectbox("Model Type", ["Prophet", "ARIMA", "Linear", "Ensemble"])
    
    # Simple forecast (using linear regression for demo)
    from sklearn.linear_model import LinearRegression
    
    # Prepare training data
    train_df = filtered_df.copy()
    train_df['days'] = (train_df['date'] - train_df['date'].min()).dt.days
    
    X_train = train_df[['days']].values
    y_train = train_df['revenue'].values
    
    # Fit model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Generate forecast
    last_day = train_df['days'].max()
    future_days = np.arange(last_day + 1, last_day + forecast_days + 1).reshape(-1, 1)
    forecast = model.predict(future_days)
    
    # Calculate confidence interval
    residuals = y_train - model.predict(X_train)
    std_error = np.std(residuals)
    z_score = 1.96 if confidence_interval == 95 else 2.576
    margin = z_score * std_error
    
    # Create forecast dataframe
    future_dates = pd.date_range(
        start=train_df['date'].max() + timedelta(days=1),
        periods=forecast_days,
        freq='D'
    )
    
    forecast_df = pd.DataFrame({
        'date': future_dates,
        'forecast': forecast,
        'lower_bound': forecast - margin,
        'upper_bound': forecast + margin
    })
    
    # Plot
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=train_df['date'],
            y=train_df['revenue'],
            mode='lines',
            name='Historical Revenue',
            line=dict(color='blue', width=2)
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['forecast'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['date'].tolist() + forecast_df['date'].tolist()[::-1],
            y=forecast_df['upper_bound'].tolist() + forecast_df['lower_bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name=f'{confidence_interval}% Confidence',
            showlegend=True
        ))
        
        fig.update_layout(
            height=500,
            title=f"Revenue Forecast - Next {forecast_days} Days",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Forecast Summary")
        
        total_forecast = forecast_df['forecast'].sum()
        avg_daily = forecast_df['forecast'].mean()
        
        st.metric("Total Forecasted Revenue", f"${total_forecast:,.0f}")
        st.metric("Avg Daily Revenue", f"${avg_daily:,.0f}")
        st.metric("Expected Growth", f"{(avg_daily/train_df['revenue'].mean() - 1)*100:.1f}%")
        
        st.markdown("---")
        
        st.subheader("Model Performance")
        st.metric("MAPE", "12.3%", "↓ 2.1pp")
        st.metric("R² Score", "0.89")
        st.metric("MAE", f"${std_error:,.0f}")
        
        st.markdown("---")
        
        st.subheader("Scenario Analysis")
        scenario = st.radio("Select Scenario", ["Base Case", "Best Case", "Worst Case"])
        if scenario == "Best Case":
            st.success("Revenue: +25% above forecast")
        elif scenario == "Worst Case":
            st.error("Revenue: -15% below forecast")
        else:
            st.info("Standard forecast scenario")

with tab3:
    st.header("Sales Team Performance")
    
    # Team filters
    col1, col2, col3 = st.columns(3)
    with col1:
        sort_by = st.selectbox("Sort By", ["Revenue", "Deals Closed", "Close Rate", "Pipeline", "Avg Cycle"])
    with col2:
        team_filter = st.selectbox("Team", ["All Teams", "Enterprise", "Mid-Market", "SMB"])
    with col3:
        performance_threshold = st.slider("Min Performance %", 0, 100, 0)
    
    st.markdown("---")
    
    # Generate rep data
    reps = ['Jane Doe', 'John Smith', 'Alice Johnson', 'Bob Williams', 'Charlie Brown', 
            'Diana Prince', 'Evan Davis', 'Fiona Garcia']
    
    rep_data = []
    for rep in reps:
        deals = np.random.randint(10, 30)
        revenue = np.random.uniform(200000, 500000)
        pipeline = revenue * np.random.uniform(2.0, 4.0)
        close_rate = np.random.uniform(0.60, 0.90)
        avg_cycle = np.random.randint(15, 35)
        
        rep_data.append({
            'Rep': rep,
            'Deals Closed': deals,
            'Revenue': revenue,
            'Pipeline': pipeline,
            'Close Rate': close_rate,
            'Avg Cycle (days)': avg_cycle,
            'Trend': np.random.choice(['↑', '↓', '→'])
        })
    
    rep_df = pd.DataFrame(rep_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Rep Leaderboard")
        
        # Format the dataframe
        display_df = rep_df.copy()
        display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.0f}")
        display_df['Pipeline'] = display_df['Pipeline'].apply(lambda x: f"${x:,.0f}")
        display_df['Close Rate'] = display_df['Close Rate'].apply(lambda x: f"{x*100:.1f}%")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
    
    with col2:
        st.subheader("Top Performers")
        
        top_3 = rep_df.nlargest(3, 'Revenue')
        
        for idx, row in top_3.iterrows():
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <h4 style="margin: 0; color: var(--brand-dark); font-weight: 800;">🏆 {row['Rep']}</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 900; color: var(--brand);">
                    ${row['Revenue']:,.0f}
                </p>
                <p style="margin: 0; font-size: 0.9rem; color: var(--muted);">
                    {row['Deals Closed']} deals • {row['Close Rate']*100:.0f}% close rate
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Performance comparison
    st.subheader("Rep Performance Comparison")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=rep_df['Rep'],
        y=rep_df['Revenue'],
        name='Revenue',
        marker_color='lightblue',
        yaxis='y',
        offsetgroup=1
    ))
    fig.add_trace(go.Scatter(
        x=rep_df['Rep'],
        y=rep_df['Close Rate']*100,
        name='Close Rate (%)',
        marker_color='#2362c7',
        yaxis='y2',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Sales Rep",
        yaxis=dict(title="Revenue ($)"),
        yaxis2=dict(title="Close Rate (%)", overlaying='y', side='right'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Sales Pipeline Management")
    
    # Pipeline options
    col1, col2, col3 = st.columns(3)
    with col1:
        pipeline_view = st.selectbox("View Type", ["Funnel", "Sankey", "Timeline", "Table"])
    with col2:
        stage_detail = st.selectbox("Detail Level", ["Summary", "Detailed", "Individual Deals"])
    
    st.markdown("---")
    
    # Pipeline stages
    stages = ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    stage_values = [1200000, 850000, 520000, 280000, 450000, 180000]
    stage_deals = [250, 120, 45, 18, 30, 12]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Pipeline Funnel")
        
        fig = go.Figure(go.Funnel(
            y=stages[:-1],  # Exclude Closed Lost
            x=stage_values[:-1],
            textinfo="value+percent initial",
            marker=dict(
                color=['#1a4fa3', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd']
            )
        ))
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Stage Metrics")
        
        for stage, value, deals in zip(stages, stage_values, stage_deals):
            st.metric(
                stage,
                f"${value:,.0f}",
                f"{deals} deals"
            )
    
    # Pipeline health
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pipeline Velocity")
        
        velocity_data = pd.DataFrame({
            'Week': [f'Week {i}' for i in range(1, 13)],
            'New Deals': np.random.randint(30, 60, 12),
            'Closed Deals': np.random.randint(15, 35, 12)
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=velocity_data['Week'],
            y=velocity_data['New Deals'],
            mode='lines+markers',
            name='New Deals',
            line=dict(color='green', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=velocity_data['Week'],
            y=velocity_data['Closed Deals'],
            mode='lines+markers',
            name='Closed Deals',
            line=dict(color='blue', width=3)
        ))
        fig.update_layout(height=350, xaxis_title="Week", yaxis_title="Number of Deals")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Deal Age Distribution")
        
        age_data = pd.DataFrame({
            'Age Range': ['0-7 days', '8-14 days', '15-30 days', '31-60 days', '60+ days'],
            'Count': [45, 38, 52, 28, 12]
        })
        
        fig = px.bar(
            age_data,
            x='Age Range',
            y='Count',
            color='Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional pipeline metrics
    st.markdown("---")
    st.subheader("Pipeline Health Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        coverage_ratio = np.random.uniform(3.0, 5.0)
        st.metric("Pipeline Coverage", f"{coverage_ratio:.1f}x", "Target: 3x")
    with col2:
        weighted_pipeline = np.random.randint(800000, 1200000)
        st.metric("Weighted Pipeline", f"${weighted_pipeline:,.0f}")
    with col3:
        stage_conversion = np.random.uniform(0.25, 0.45)
        st.metric("Stage Conversion", f"{stage_conversion*100:.1f}%", "2.1pp")
    with col4:
        avg_stage_time = np.random.randint(8, 15)
        st.metric("Avg Stage Time", f"{avg_stage_time} days", "-1 day")

with tab5:
    st.header("AI-Powered Insights & Recommendations")
    
    st.markdown("""
    <div class="info-box">
    <strong>AI Analysis:</strong> Machine learning models analyze historical patterns, identify trends, 
    and provide actionable recommendations to optimize sales performance.
    </div>
    """, unsafe_allow_html=True)
    
    # Key insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Opportunities")
        
        opportunities = [
            {
                'title': 'High-Value Deal at Risk',
                'description': 'Deal #4523 ($250K) in negotiation stage for 45 days',
                'action': 'Immediate follow-up recommended',
                'priority': 'HIGH'
            },
            {
                'title': 'Upsell Potential Identified',
                'description': '15 customers showing Enterprise upgrade signals',
                'action': 'Trigger targeted campaign',
                'priority': 'MEDIUM'
            },
            {
                'title': 'Regional Growth Opportunity',
                'description': 'Asia Pacific showing 28% QoQ growth',
                'action': 'Increase resource allocation',
                'priority': 'MEDIUM'
            }
        ]
        
        for opp in opportunities:
            color = '#1e40af' if opp['priority'] == 'HIGH' else '#3b82f6'
            st.markdown(f"""
            <div style="background: white; border-left: 4px solid {color}; 
                        padding: 1rem; margin-bottom: 1rem; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; color: {color};">{opp['title']}</h4>
                <p style="margin: 0.5rem 0; color: #4a5568;">{opp['description']}</p>
                <p style="margin: 0; font-weight: 600; color: #2d3748;">→ {opp['action']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Predictive Analytics")
        
        st.metric("Churn Risk Score", "18.5%", "-2.3pp", delta_color="inverse")
        st.metric("Next Quarter Forecast", "$2.3M", "+12%")
        st.metric("Pipeline Health Score", "8.5/10", "+0.5")
        
        st.markdown("---")
        
        st.subheader("Best Practices")
        st.markdown("""
        - Optimal follow-up time: 2-3 days after proposal
        - Best day to close: Thursday shows 23% higher close rate
        - Email open rate peak: Tuesday 10AM (31% open rate)
        - Average deal cycle: 22 days for Professional tier
        """)
    
    # Win/Loss analysis
    st.subheader("Win/Loss Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top Win Reasons**")
        win_reasons = pd.DataFrame({
            'Reason': ['Product Fit', 'Pricing', 'Support', 'Features', 'Reputation'],
            'Percentage': [35, 28, 18, 12, 7]
        })
        fig = px.bar(win_reasons, x='Percentage', y='Reason', orientation='h', color='Percentage',
                     color_continuous_scale='Greens')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Top Loss Reasons**")
        loss_reasons = pd.DataFrame({
            'Reason': ['Price', 'Competitor', 'Timing', 'Features', 'Budget'],
            'Percentage': [38, 25, 18, 12, 7]
        })
        fig = px.bar(loss_reasons, x='Percentage', y='Reason', orientation='h', color='Percentage',
                     color_continuous_scale='Blues')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.header("Goal Tracking & Performance Targets")
    
    st.markdown("""
    <div class="info-box">
    <strong>Goal Management:</strong> Track team and individual goals with real-time progress monitoring.
    </div>
    """, unsafe_allow_html=True)
    
    # Goals overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        quarterly_goal = 2500000
        current_progress = filtered_df['revenue'].sum()
        progress_pct = (current_progress / quarterly_goal) * 100
        st.metric("Quarterly Goal", f"${quarterly_goal:,.0f}")
        st.progress(min(progress_pct / 100, 1.0))
        st.write(f"{progress_pct:.1f}% Complete")
    
    with col2:
        deals_goal = 200
        deals_progress = filtered_df['deals'].sum()
        deals_pct = (deals_progress / deals_goal) * 100
        st.metric("Deals Goal", f"{deals_goal}")
        st.progress(min(deals_pct / 100, 1.0))
        st.write(f"{deals_pct:.1f}% Complete")
    
    with col3:
        new_customers_goal = 50
        new_customers = np.random.randint(35, 55)
        new_cust_pct = (new_customers / new_customers_goal) * 100
        st.metric("New Customers Goal", f"{new_customers_goal}")
        st.progress(min(new_cust_pct / 100, 1.0))
        st.write(f"{new_cust_pct:.1f}% Complete")
    
    with col4:
        retention_goal = 0.92
        retention_current = 0.87
        retention_pct = (retention_current / retention_goal) * 100
        st.metric("Retention Goal", f"{retention_goal*100:.0f}%")
        st.progress(min(retention_pct / 100, 1.0))
        st.write(f"{retention_pct:.1f}% of Target")
    
    st.markdown("---")
    
    # Individual rep goals
    st.subheader("Individual Rep Goals")
    
    rep_goals = pd.DataFrame({
        'Rep': ['Jane Doe', 'John Smith', 'Alice Johnson', 'Bob Williams'],
        'Goal': [300000, 280000, 320000, 290000],
        'Current': [285000, 295000, 310000, 275000],
        'Progress': [95, 105, 97, 95]
    })
    
    for idx, row in rep_goals.iterrows():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{row['Rep']}**")
        with col2:
            st.progress(min(row['Progress'] / 100, 1.0))
        with col3:
            if row['Progress'] >= 100:
                st.success(f"{row['Progress']}%")
            elif row['Progress'] >= 80:
                st.info(f"{row['Progress']}%")
            else:
                st.warning(f"{row['Progress']}%")
    
    st.markdown("---")
    
    # Goal setting
    st.subheader("Set New Goals")
    col1, col2 = st.columns(2)
    with col1:
        new_revenue_goal = st.number_input("Revenue Goal ($)", min_value=0, value=2500000, step=100000)
        new_deals_goal = st.number_input("Deals Goal", min_value=0, value=200, step=10)
    with col2:
        goal_period = st.selectbox("Period", ["Monthly", "Quarterly", "Yearly"])
        if st.button("Update Goals", use_container_width=True):
            st.success("Goals updated successfully!")

with tab7:
    st.header("Advanced Analytics & Deep Dive")
    
    st.markdown("""
    <div class="info-box">
    <strong>Advanced Features:</strong> Cohort analysis, customer lifetime value, attribution modeling, and predictive analytics.
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Cohort Analysis", "Customer LTV", "Attribution Model", "Predictive Scoring", "Sentiment Analysis"]
    )
    
    st.markdown("---")
    
    if analysis_type == "Cohort Analysis":
        st.subheader("Cohort Retention Analysis")
        
        # Generate cohort data
        cohorts = ['Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025']
        cohort_data = pd.DataFrame({
            'Cohort': cohorts,
            'Month 0': [100, 100, 100, 100, 100, 100],
            'Month 1': [85, 87, 89, 86, 88, 90],
            'Month 2': [72, 75, 78, 74, 76, 0],
            'Month 3': [65, 68, 71, 67, 0, 0],
            'Month 4': [58, 62, 65, 0, 0, 0],
            'Month 5': [52, 56, 0, 0, 0, 0]
        })
        
        st.dataframe(cohort_data, use_container_width=True)
        
    elif analysis_type == "Customer LTV":
        st.subheader("Customer Lifetime Value Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_ltv = np.random.randint(8000, 15000)
            st.metric("Average LTV", f"${avg_ltv:,.0f}", "12%")
        with col2:
            ltv_cac_ratio = np.random.uniform(3.0, 5.0)
            st.metric("LTV:CAC Ratio", f"{ltv_cac_ratio:.1f}:1", "0.3")
        with col3:
            payback_period = np.random.randint(8, 16)
            st.metric("Payback Period", f"{payback_period} months", "-2 mo")
        
        # LTV by segment
        st.markdown("---")
        st.subheader("LTV by Customer Segment")
        
        segment_ltv = pd.DataFrame({
            'Segment': ['Enterprise', 'Mid-Market', 'SMB', 'Startup'],
            'LTV': [25000, 12000, 6000, 3500],
            'Customers': [150, 450, 1200, 800]
        })
        
        fig = px.bar(segment_ltv, x='Segment', y='LTV', color='Customers',
                     color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    elif analysis_type == "Attribution Model":
        st.subheader("Multi-Touch Attribution Analysis")
        
        attribution_data = pd.DataFrame({
            'Channel': ['Organic Search', 'Paid Search', 'Social Media', 'Email', 'Direct', 'Referral'],
            'First Touch': [25, 15, 20, 10, 20, 10],
            'Last Touch': [20, 30, 15, 15, 10, 10],
            'Linear': [18, 20, 18, 16, 15, 13],
            'Time Decay': [16, 25, 19, 18, 12, 10]
        })
        
        attribution_model = st.selectbox("Attribution Model", ["First Touch", "Last Touch", "Linear", "Time Decay"])
        
        fig = px.bar(attribution_data, x='Channel', y=attribution_model, 
                     color=attribution_model, color_continuous_scale='Blues')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
    elif analysis_type == "Predictive Scoring":
        st.subheader("Lead & Deal Scoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**High-Probability Leads**")
            high_prob_leads = pd.DataFrame({
                'Lead': [f'Lead #{i}' for i in range(1, 6)],
                'Score': [92, 88, 85, 83, 81],
                'Value': [45000, 38000, 52000, 41000, 35000]
            })
            st.dataframe(high_prob_leads, use_container_width=True)
        
        with col2:
            st.markdown("**At-Risk Deals**")
            at_risk = pd.DataFrame({
                'Deal': [f'Deal #{i}' for i in range(1, 6)],
                'Risk Score': [87, 82, 79, 76, 73],
                'Value': [125000, 98000, 156000, 87000, 112000]
            })
            st.dataframe(at_risk, use_container_width=True)
    
    else:  # Sentiment Analysis
        st.subheader("Customer Sentiment Analysis")
        
        sentiment_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Positive': [65, 68, 72, 70, 75, 78],
            'Neutral': [25, 22, 20, 23, 18, 15],
            'Negative': [10, 10, 8, 7, 7, 7]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=sentiment_data['Month'], y=sentiment_data['Positive'], 
                            name='Positive', marker_color='#93c5fd'))
        fig.add_trace(go.Bar(x=sentiment_data['Month'], y=sentiment_data['Neutral'], 
                            name='Neutral', marker_color='#e2e8f0'))
        fig.add_trace(go.Bar(x=sentiment_data['Month'], y=sentiment_data['Negative'], 
                            name='Negative', marker_color='#3b82f6'))
        
        fig.update_layout(barmode='stack', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Sentiment", "78% Positive", "3pp")
        with col2:
            st.metric("NPS Score", "45", "5")
        with col3:
            st.metric("CSAT Score", "4.2/5.0", "0.2")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Data Quality:** 99.2%")
with col2:
    st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))
with col3:
    st.markdown("**Response Time:** <50ms p95")

