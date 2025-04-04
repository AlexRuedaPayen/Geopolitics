import dash
from dash import dcc, html, dash_table
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------
# 📊 Generate Randomized Data
# ---------------------------
np.random.seed(42)
countries = ["USA", "France", "Germany", "China", "Japan"]
sectors = ["Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples",
           "Healthcare", "Financials", "Information Technology", "Telecommunications", "Utilities", "Real Estate"]

# Create an empty DataFrame
data = pd.DataFrame()

# Generate a different number of companies for each sector
for sector in sectors:
    num_companies = np.random.randint(30, 100)  # Random count per sector
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
    
    html.H1("📈 Financial Dashboard by Country & Sector", style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Dropdowns in a horizontal row
    html.Div([
        html.Div([
            html.Label("Select Country:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": c, "value": c} for c in countries],
                value=countries[0],  # Default
                clearable=False,
                style={'width': '200px'}
            )
        ], style={'display': 'inline-block', 'marginRight': '20px'}),

        html.Div([
            html.Label("Select Sector:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="sector-dropdown",
                options=[{"label": s, "value": s} for s in sectors],
                value=sectors[0],  # Default
                clearable=False,
                style={'width': '250px'}
            )
        ], style={'display': 'inline-block'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),

    # Charts
    html.Div([
        dcc.Graph(id="stock-price-chart", style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id="market-cap-chart", style={'width': '48%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    # Table
    html.H3("Company Data", style={'textAlign': 'center', 'marginTop': '20px'}),
    dash_table.DataTable(
        id="company-table",
        columns=[{"name": col, "id": col} for col in data.columns],
        page_size=10,
        style_table={'width': '90%', 'margin': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#f4f4f4'}
    )
])

# ---------------------------
# 🔄 Callbacks for Dynamic Updates
# ---------------------------
@app.callback(
    [dash.Output("company-table", "data"),
     dash.Output("stock-price-chart", "figure"),
     dash.Output("market-cap-chart", "figure")],
    [dash.Input("country-dropdown", "value"),
     dash.Input("sector-dropdown", "value")]
)
def update_dashboard(selected_country, selected_sector):
    print(f"Selected Country: {selected_country}, Selected Sector: {selected_sector}")
    filtered_data = data[(data["Country"] == selected_country) & (data["Sector"] == selected_sector)]
    print(f"Filtered Data Count: {len(filtered_data)}")

    # Stock Price Chart
    stock_price_fig = px.line(
        filtered_data,
        x="Company",
        y="Stock Price",
        title="Stock Prices",
        markers=True
    )

    # Market Cap Chart
    market_cap_fig = px.bar(
        filtered_data,
        x="Company",
        y="Market Cap ($B)",
        title="Market Cap",
        text_auto=True
    )

    return filtered_data.to_dict("records"), stock_price_fig, market_cap_fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
