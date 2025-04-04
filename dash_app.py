import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry

# ---------------------------
# 📊 Generate Randomized Data
# ---------------------------
np.random.seed(42)

# Expanded countries per region
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

# Create a DataFrame with dummy data
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
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📈 Financial Dashboard by Region & Sector", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Select Zone:"),
            dcc.Dropdown(
                id="zone-dropdown",
                options=[{"label": z, "value": z} for z in zones],
                value=zones[0],
                clearable=False
            )
        ], style={"width": "30%", 'display': 'inline-block', 'marginRight': '20px'}),

        html.Div([
            html.Label("Select Country:"),
            dcc.Dropdown(
                id="country-dropdown",
                clearable=False
            )
        ], style={"width": "30%", 'display': 'inline-block', 'marginRight': '20px'}),

        html.Div([
            html.Label("Select Sector:"),
            dcc.Dropdown(
                id="sector-dropdown",
                options=[{"label": s, "value": s} for s in sectors],
                value=sectors[0],
                clearable=False
            )
        ], style={"width": "30%", 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),

    dcc.Graph(id="zone-map"),

    html.Div([
        dcc.Graph(id="stock-price-chart", style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id="market-cap-chart", style={'width': '48%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.H3("Company Data", style={'textAlign': 'center'}),
    dash_table.DataTable(
        id="company-table",
        columns=[{"name": col, "id": col} for col in data.columns],
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

# ---------------------------
# 🔄 Callbacks
# ---------------------------
@app.callback(
    Output("country-dropdown", "options"),
    Output("country-dropdown", "value"),
    Input("zone-dropdown", "value")
)
def update_countries(zone):
    available = [c for c, z in country_region_map.items() if z == zone]

    print(f'zone selected :{zone}')
    print([{"label": c, "value": c} for c in available], available[0] if available else None)
    
    return [{"label": c, "value": c} for c in available], available[0] if available else None

@app.callback(
    Output("zone-map", "figure"),
    Input("zone-dropdown", "value")
)
def update_map(selected_zone):
    countries_in_zone = [c for c, z in country_region_map.items() if z == selected_zone]
    df_map = pd.DataFrame({"country": countries_in_zone})
    df_map["dummy"] = 1
    df_map["iso_alpha"] = df_map["country"].apply(lambda x: pycountry.countries.get(name=x).alpha_3 if pycountry.countries.get(name=x) else "")
    df_map["hover_text"] = df_map["country"].apply(lambda x: f"{x} / {pycountry.countries.get(name=x).alpha_2 if pycountry.countries.get(name=x) else ''} / " + chr(127462 + ord(pycountry.countries.get(name=x).alpha_2[0]) - 65) + chr(127462 + ord(pycountry.countries.get(name=x).alpha_2[1]) - 65) if pycountry.countries.get(name=x) and pycountry.countries.get(name=x).alpha_2 else x)

    fig = px.choropleth(
        df_map, locations="iso_alpha", color="dummy",
        hover_name="hover_text",
        title=f"Countries in {selected_zone}",
        color_continuous_scale="Blues"
    )
    fig.update_layout(clickmode='event+select', coloraxis_showscale=False)
    return fig

@app.callback(
    Output("country-dropdown", "value"),
    Input("zone-map", "clickData"),
    prevent_initial_call=True
)
def update_country_from_map(click_data):
    if click_data and 'points' in click_data:
        country_code = click_data['points'][0]['location']
        country_name = next((c.name for c in pycountry.countries if c.alpha_3 == country_code), None)
        if country_name in countries:
            return country_name
    return dash.no_update

@app.callback(
    Output("company-table", "data"),
    Output("stock-price-chart", "figure"),
    Output("market-cap-chart", "figure"),
    Input("country-dropdown", "value"),
    Input("sector-dropdown", "value")
)
def update_dashboard(selected_country, selected_sector):
    filtered_data = data[(data["Country"] == selected_country) & (data["Sector"] == selected_sector)]

    stock_price_fig = px.line(
        filtered_data, x="Company", y="Stock Price",
        title="Stock Prices", markers=True
    )

    market_cap_fig = px.bar(
        filtered_data, x="Company", y="Market Cap ($B)",
        title="Market Capitalization", text_auto=True
    )

    return filtered_data.to_dict("records"), stock_price_fig, market_cap_fig

@app.callback(
    Output("download-data", "data"),
    Input("download-btn", "n_clicks"),
    State("country-dropdown", "value"),
    State("sector-dropdown", "value"),
    prevent_initial_call=True
)
def download_csv(n_clicks, country, sector):
    filtered = data[(data["Country"] == country) & (data["Sector"] == sector)]
    return dcc.send_data_frame(filtered.to_csv, f"{country}_{sector}_data.csv")

# ---------------------------
# ▶️ Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
