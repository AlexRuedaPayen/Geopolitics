from dash import html, dcc
import dash_bootstrap_components as dbc

from .utils import zones

layout = dbc.Container([
    html.H1("📈 Financial Dashboard by Region & Sector", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Select Zone:"),
            dcc.Dropdown(
                id="zone-dropdown",
                options=[{"label": z, "value": z} for z in zones],
                value=None,
                placeholder="Select a world zone...",
                clearable=False
            )
        ], style={"width": "30%", 'display': 'inline-block', 'marginRight': '20px'}),
    ], style={'marginBottom': '20px'}),

    html.Div(id="zone-map-container"),
    html.Div(id="sector-dropdown-container"),
    html.Div(id="charts-container"),
], fluid=True)
