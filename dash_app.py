import time
import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import pycountry
import dash_bootstrap_components as dbc

# ---------------------------
# 📊 Generate Randomized Data
# ---------------------------
np.random.seed(42)

country_region_map = {
    "USA": "North America", "Canada": "North America", "Mexico": "North America",
    "France": "Western Europe", "Germany": "Western Europe", "UK": "Western Europe",
    "Italy": "Southern Europe", "Spain": "Southern Europe", "Greece": "Southern Europe",
    "Serbia": "Balkans", "Romania": "Balkans", "Bulgaria": "Balkans", "Albania": "Balkans",
    "China": "East Asia", "Japan": "East Asia", "South Korea": "East Asia",
    "Saudi Arabia": "Middle East", "UAE": "Middle East", "Israel": "Middle East",
    "Brazil": "South America", "Argentina": "South America", "Chile": "South America"
}

countries = list(country_region_map.keys())
zones = sorted(set(country_region_map.values()))

sectors = [
    "Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples",
    "Healthcare", "Financials", "Information Technology", "Telecommunications", "Utilities", "Real Estate"
]

# Generate mock data for companies
data = pd.DataFrame()
for sector in sectors:
    num_companies = np.random.randint(30, 60)
    sector_data = pd.DataFrame({
        "Company": [f"{sector} Corp {i}" for i in range(1, num_companies + 1)],
        "Country": np.random.choice(countries, num_companies),
        "Sector": [sector] * num_companies,
        "Stock Price": np.random.uniform(50, 500, num_companies),
        "Market Cap ($B)": np.random.uniform(10, 100, num_companies),
        "Revenue ($B)": np.random.uniform(5, 50, num_companies),
        "Employees": np.random.randint(1000, 50000, num_companies)
    })
    data = pd.concat([data, sector_data], ignore_index=True)

# ---------------------------
# 🚀 Dash App Setup
# ---------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([

    # Header section
    dbc.Row([dbc.Col(html.H1("📈 Financial Dashboard by Region & Sector", style={'textAlign': 'center'}), width=12)], style={"marginBottom": "20px"}),

    # Dropdown to select zone
    dbc.Row([dbc.Col(
        html.Div([html.Label("Select Zone:"), 
                  dcc.Dropdown(id="zone-dropdown", options=[{"label": z, "value": z} for z in zones], 
                               value=None, placeholder="Select a world zone...", clearable=False)], 
        style={"width": "30%", 'display': 'inline-block', 'marginRight': '20px'}), width=4)], justify="start"),

    # Container for map and sector dropdown
    dbc.Row([dbc.Col(html.Div(id="zone-map-container"), width=12)], style={"marginBottom": "20px"}),
    dbc.Row([dbc.Col(html.Div(id="sector-dropdown-container"), width=12)], style={"marginBottom": "20px"}),

    # Container for charts
    dbc.Row([dbc.Col(html.Div(id="charts-container"), width=12)]),
])

# ---------------------------
# 🔄 Callbacks
# ---------------------------
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
    df_map["iso_alpha"] = df_map["country"].apply(lambda x: pycountry.countries.get(name=x).alpha_3 if pycountry.countries.get(name=x) else "")
    df_map["hover_text"] = df_map["country"].apply(
        lambda x: f"{x} / {pycountry.countries.get(name=x).alpha_2 if pycountry.countries.get(name=x) else ''} / " +
                  chr(127462 + ord(pycountry.countries.get(name=x).alpha_2[0]) - 65) +
                  chr(127462 + ord(pycountry.countries.get(name=x).alpha_2[1]) - 65)
        if pycountry.countries.get(name=x) and pycountry.countries.get(name=x).alpha_2 else x
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

    return html.Div([html.Label("Select Sector:"), 
                     dcc.Dropdown(id="sector-dropdown", options=sector_options, 
                                  placeholder="Select a sector...", clearable=False)], 
                    style={"width": "30%", 'display': 'inline-block', 'marginBottom': '20px'})

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

    stock_price_fig = px.line(filtered_data, x="Company", y="Stock Price",
                              title=f"Stock Prices in {country_name}", markers=True)

    market_cap_fig = px.bar(filtered_data, x="Company", y="Market Cap ($B)",
                            title=f"Market Capitalization in {country_name}", text_auto=True)

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

        html.Div([html.Button("⬇️ Download Table as CSV", id="download-btn"),
                  dcc.Download(id="download-data")],
                 style={'textAlign': 'center', 'marginTop': '20px'})
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
        return dash.no_update

    country_code = click_data['points'][0]['location']
    country_name = next((c.name for c in pycountry.countries if c.alpha_3 == country_code), None)
    if not country_name:
        return dash.no_update

    filtered = data[(data["Country"] == country_name) & (data["Sector"] == sector)]
    print(f"📀 CSV download prepared in {time.time() - start:.2f} seconds")
    return dcc.send_data_frame(filtered.to_csv, f"{country_name}_{sector}_data.csv")

# ---------------------------
# ▶️ Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)