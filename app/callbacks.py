from dash import Input, Output, State, dcc, html, dash_table, no_update
import pandas as pd
import numpy as np
import plotly.express as px
import pycountry
import time

from .utils import country_region_map, data

zones = sorted(set(country_region_map.values()))
countries = list(country_region_map.keys())


def register_callbacks(app):
    @app.callback(
        Output("zone-map-container", "children"),
        Input("zone-dropdown", "value")
    )
    def show_map(selected_zone):
        if not selected_zone:
            return None
        return dcc.Graph(id="zone-map")

    @app.callback(
        Output("zone-map", "figure"),
        Input("zone-dropdown", "value")
    )
    def update_map(selected_zone):
        start = time.time()
        countries_in_zone = [c for c, z in country_region_map.items() if z == selected_zone]
        df_map = pd.DataFrame({"country": countries_in_zone})
        df_map["dummy"] = 1
        df_map["iso_alpha"] = df_map["country"].apply(
            lambda x: pycountry.countries.get(name=x).alpha_3 if pycountry.countries.get(name=x) else ""
        )
        df_map["hover_text"] = df_map["country"].apply(
            lambda x: f"{x} / {pycountry.countries.get(name=x).alpha_2 if pycountry.countries.get(name=x) else ''}"
            if pycountry.countries.get(name=x) else x
        )

        fig = px.choropleth(
            df_map, locations="iso_alpha", color="dummy",
            hover_name="hover_text",
            title=f"Countries in {selected_zone}",
            color_continuous_scale="Blues"
        )
        fig.update_layout(clickmode='event+select', coloraxis_showscale=False)
        print(f"🗺️ Map generated in {time.time() - start:.2f} sec")
        return fig

    @app.callback(
        Output("sector-dropdown-container", "children"),
        Input("zone-map", "clickData")
    )
    def show_sector_dropdown(click_data):
        if not click_data:
            return None

        country_code = click_data['points'][0]['location']
        country_name = next((c.name for c in pycountry.countries if c.alpha_3 == country_code), None)
        if not country_name:
            return None

        available_sectors = data[data["Country"] == country_name]["Sector"].unique()
        sector_options = [{"label": s, "value": s} for s in sorted(available_sectors)]

        return html.Div([
            html.Label("Select Sector:"),
            dcc.Dropdown(
                id="sector-dropdown",
                options=sector_options,
                placeholder="Select a sector...",
                clearable=False
            )
        ], style={"width": "30%", 'display': 'inline-block', 'marginBottom': '20px'})

    @app.callback(
        Output("charts-container", "children"),
        Input("zone-map", "clickData"),
        Input("sector-dropdown", "value"),
        prevent_initial_call=True
    )
    def update_dashboard(click_data, selected_sector):
        start = time.time()
        if not click_data or not selected_sector:
            return None

        country_code = click_data['points'][0]['location']
        country_name = next((c.name for c in pycountry.countries if c.alpha_3 == country_code), None)
        if country_name not in countries:
            return None

        filtered_data = data[(data["Country"] == country_name) & (data["Sector"] == selected_sector)]

        stock_price_fig = px.line(
            filtered_data, x="Company", y="Stock Price",
            title=f"Stock Prices in {country_name}", markers=True
        )

        market_cap_fig = px.bar(
            filtered_data, x="Company", y="Market Cap ($B)",
            title=f"Market Capitalization in {country_name}", text_auto=True
        )

        print(f"📊 Dashboard updated in {time.time() - start:.2f} sec")

        return html.Div([
            html.Div([
                dcc.Graph(figure=stock_price_fig, style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(figure=market_cap_fig, style={'width': '48%', 'display': 'inline-block'})
            ], style={'display': 'flex', 'justifyContent': 'center'}),

            html.H3("Company Data", style={'textAlign': 'center'}),

            dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in data.columns],
                data=filtered_data.to_dict("records"),
                page_size=10,
                style_table={'width': '90%', 'margin': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f4f4f4'}
            ),

            html.Div([
                html.Button("⬇️ Download Table as CSV", id="download-btn"),
                dcc.Download(id="download-data")
            ], style={'textAlign': 'center', 'marginTop': '20px'})
        ])

    @app.callback(
        Output("download-data", "data"),
        Input("download-btn", "n_clicks"),
        State("zone-map", "clickData"),
        State("sector-dropdown", "value"),
        prevent_initial_call=True
    )
    def download_csv(n_clicks, click_data, sector):
        start = time.time()
        if not click_data or not sector:
            return no_update

        country_code = click_data['points'][0]['location']
        country_name = next((c.name for c in pycountry.countries if c.alpha_3 == country_code), None)
        if not country_name:
            return no_update

        filtered = data[(data["Country"] == country_name) & (data["Sector"] == sector)]
        print(f"📀 CSV download prepared in {time.time() - start:.2f} seconds")
        return dcc.send_data_frame(filtered.to_csv, f"{country_name}_{sector}_data.csv")
