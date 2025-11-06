"""
Dashboard callbacks and interactivity
"""
from dash import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.features.features import compute_all_kpis

# Load data globally
try:
    DF = pd.read_csv('data/processed/sales_transformed.csv', parse_dates=['date'])
except:
    DF = pd.DataFrame()

def filter_data(df, date_range, regions, channels):
    """Filter dataframe based on selections"""
    df_filtered = df.copy()
    
    if date_range:
        start, end = date_range
        df_filtered = df_filtered[(df_filtered['date'] >= start) & (df_filtered['date'] <= end)]
    
    if regions:
        df_filtered = df_filtered[df_filtered['region'].isin(regions)]
    
    if channels:
        df_filtered = df_filtered[df_filtered['channel'].isin(channels)]
    
    return df_filtered

def register_callbacks(app):
    """Register all dashboard callbacks"""
    
    # Populate filter options
    @app.callback(
        [Output('region-filter', 'options'),
         Output('channel-filter', 'options')],
        Input('date-range', 'start_date')
    )
    def update_filters(_):
        if DF.empty:
            return [], []
        
        regions = [{'label': r, 'value': r} for r in sorted(DF['region'].unique())]
        channels = [{'label': c, 'value': c} for c in sorted(DF['channel'].unique())]
        
        return regions, channels
    
    # Update all KPIs
    @app.callback(
        [Output('kpi-total-revenue', 'children'),
         Output('kpi-total-orders', 'children'),
         Output('kpi-avg-order-value', 'children'),
         Output('kpi-customers', 'children')],
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('region-filter', 'value'),
         Input('channel-filter', 'value')]
    )
    def update_kpis(start_date, end_date, regions, channels):
        if DF.empty:
            return "$0", "0", "$0", "0"
        
        df_filtered = filter_data(DF, [start_date, end_date], regions, channels)
        kpis = compute_all_kpis(df_filtered)
        
        return (
            f"${kpis['total_revenue']:,.0f}",
            f"{kpis['total_orders']:,}",
            f"${kpis['aov']:,.0f}",
            f"{kpis['total_customers']:,}"
        )
    
    # Daily sales chart
    @app.callback(
        Output('daily-sales-chart', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('region-filter', 'value'),
         Input('channel-filter', 'value')]
    )
    def update_daily_sales(start_date, end_date, regions, channels):
        if DF.empty:
            return go.Figure()
        
        df_filtered = filter_data(DF, [start_date, end_date], regions, channels)
        daily = df_filtered.groupby(df_filtered['date'].dt.date).agg({'revenue': 'sum'}).reset_index()
        
        fig = px.line(daily, x='date', y='revenue', title='')
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig.update_traces(line_color='#0d6efd')
        
        return fig
    
    # Region chart
    @app.callback(
        Output('region-chart', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('region-filter', 'value'),
         Input('channel-filter', 'value')]
    )
    def update_region_chart(start_date, end_date, regions, channels):
        if DF.empty:
            return go.Figure()
        
        df_filtered = filter_data(DF, [start_date, end_date], regions, channels)
        region_data = df_filtered.groupby('region').agg({'revenue': 'sum'}).reset_index()
        
        fig = px.bar(region_data, x='region', y='revenue', title='')
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Revenue ($)",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig.update_traces(marker_color='#0dcaf0')
        
        return fig
    
    # Top products chart
    @app.callback(
        Output('top-products-chart', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('region-filter', 'value'),
         Input('channel-filter', 'value')]
    )
    def update_top_products(start_date, end_date, regions, channels):
        if DF.empty:
            return go.Figure()
        
        df_filtered = filter_data(DF, [start_date, end_date], regions, channels)
        top_products = df_filtered.groupby('product_id').agg({'revenue': 'sum'}).nlargest(10, 'revenue').reset_index()
        
        fig = px.bar(top_products, x='revenue', y='product_id', orientation='h', title='')
        fig.update_layout(
            xaxis_title="Revenue ($)",
            yaxis_title="Product",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig.update_traces(marker_color='#198754')
        
        return fig
    
    # Top customers chart
    @app.callback(
        Output('top-customers-chart', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('region-filter', 'value'),
         Input('channel-filter', 'value')]
    )
    def update_top_customers(start_date, end_date, regions, channels):
        if DF.empty:
            return go.Figure()
        
        df_filtered = filter_data(DF, [start_date, end_date], regions, channels)
        top_customers = df_filtered.groupby('customer_id').agg({'revenue': 'sum'}).nlargest(10, 'revenue').reset_index()
        
        fig = px.bar(top_customers, x='revenue', y='customer_id', orientation='h', title='')
        fig.update_layout(
            xaxis_title="Revenue ($)",
            yaxis_title="Customer",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig.update_traces(marker_color='#ffc107')
        
        return fig
    
    # Channel performance chart
    @app.callback(
        Output('channel-chart', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('region-filter', 'value'),
         Input('channel-filter', 'value')]
    )
    def update_channel_chart(start_date, end_date, regions, channels):
        if DF.empty:
            return go.Figure()
        
        df_filtered = filter_data(DF, [start_date, end_date], regions, channels)
        channel_data = df_filtered.groupby('channel').agg({
            'revenue': 'sum',
            'order_id': 'nunique'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue', x=channel_data['channel'], y=channel_data['revenue'], yaxis='y'))
        fig.add_trace(go.Scatter(name='Orders', x=channel_data['channel'], y=channel_data['order_id'], yaxis='y2', mode='lines+markers'))
        
        fig.update_layout(
            xaxis_title="Channel",
            yaxis=dict(title="Revenue ($)"),
            yaxis2=dict(title="Orders", overlaying='y', side='right'),
            hovermode='x unified',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        return fig
