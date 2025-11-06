"""
Dashboard layout and UI components for Sales Analytics Platform.

This module defines the visual structure and components of the analytics dashboard,
including KPI cards, filters, charts, and tabbed navigation.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

def create_kpi_card(title, value, icon, color="primary"):
    """
    Create a KPI display card component.
    
    Args:
        title (str): Display name of the KPI
        value (str): Initial value to display
        icon (str): Font Awesome icon name (without 'fa-' prefix)
        color (str): Bootstrap color theme (primary, success, info, warning, danger)
    
    Returns:
        dbc.Card: Styled KPI card component
    """
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas fa-{icon} fa-2x", style={'color': f'var(--bs-{color})'}),
                html.H3(value, id=f'kpi-{title.lower().replace(" ", "-")}', className="mt-2"),
                html.P(title, className="text-muted")
            ], className="text-center")
        ])
    ], className="shadow-sm")

def create_layout():
    """
    Create the main dashboard layout structure.
    
    Returns:
        dbc.Container: Complete dashboard layout with all components
    """
    return dbc.Container([
        # Application header
        dbc.Row([
            dbc.Col([
                html.H1("Sales Analytics Platform", className="text-primary"),
                html.P("Enterprise business intelligence and forecasting system", className="text-muted")
            ])
        ], className="mb-4 mt-3"),

        # Tabs
        dcc.Tabs(id="main-tabs", value="tab-analytics", children=[
            dcc.Tab(label="Analytics", value="tab-analytics", children=[
                # Filters
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label("Date Range"),
                                dcc.DatePickerRange(
                                    id='date-range',
                                    start_date=(datetime.now() - timedelta(days=90)).date(),
                                    end_date=datetime.now().date(),
                                    display_format='YYYY-MM-DD',
                                    style={'width': '100%'}
                                )
                            ])
                        ])
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label("Region"),
                                dcc.Dropdown(
                                    id='region-filter',
                                    options=[],
                                    multi=True,
                                    placeholder="All Regions"
                                )
                            ])
                        ])
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label("Channel"),
                                dcc.Dropdown(
                                    id='channel-filter',
                                    options=[],
                                    multi=True,
                                    placeholder="All Channels"
                                )
                            ])
                        ])
                    ], md=4)
                ], className="mb-4"),

                # KPI Cards
                dbc.Row([
                    dbc.Col(create_kpi_card("Total Revenue", "$0", "dollar-sign", "success"), md=3),
                    dbc.Col(create_kpi_card("Total Orders", "0", "shopping-cart", "primary"), md=3),
                    dbc.Col(create_kpi_card("Avg Order Value", "$0", "chart-line", "info"), md=3),
                    dbc.Col(create_kpi_card("Customers", "0", "users", "warning"), md=3)
                ], className="mb-4"),

                # Charts Row 1
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Daily Sales Trend")),
                            dbc.CardBody([
                                dcc.Graph(id='daily-sales-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ], md=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Sales by Region")),
                            dbc.CardBody([
                                dcc.Graph(id='region-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ], md=4)
                ], className="mb-4"),

                # Charts Row 2
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Top 10 Products")),
                            dbc.CardBody([
                                dcc.Graph(id='top-products-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Top 10 Customers")),
                            dbc.CardBody([
                                dcc.Graph(id='top-customers-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ], md=6)
                ], className="mb-4"),

                # Additional Metrics
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Channel Performance")),
                            dbc.CardBody([
                                dcc.Graph(id='channel-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ], md=12)
                ], className="mb-4"),

                # Data storage component
                dcc.Store(id='data-store')
            ]),
            dcc.Tab(label="AI Insights", value="tab-ai-insights", children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("AI-Powered Sales Insights")),
                            dbc.CardBody([
                                html.Div(id='ai-sales-insights', style={'whiteSpace': 'pre-line', 'fontSize': '1.1em'})
                            ])
                        ])
                    ], md=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Opportunity Scoring")),
                            dbc.CardBody([
                                html.Div(id='ai-opportunity-scores')
                            ])
                        ])
                    ], md=4)
                ], className="mb-4"),
            ]),
        ]),
    ], fluid=True, className="p-4")

