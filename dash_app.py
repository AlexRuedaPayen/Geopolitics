import dash
from dash import dcc, html, dash_table
import pandas as pd
import numpy as np
import plotly.express as px

# Mock Data
np.random.seed(42)
data = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
    "Stock Price": np.random.uniform(100, 200, 30),
    "Volume": np.random.randint(1000, 5000, 30)
})

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📈 Financial Dashboard"),
    
    dcc.Graph(
        id="stock-price-chart",
        figure=px.line(data, x="Date", y="Stock Price", title="Stock Price Over Time")
    ),
    
    dcc.Graph(
        id="volume-chart",
        figure=px.bar(data, x="Date", y="Volume", title="Trading Volume")
    ),
    
    html.H3("Raw Data"),
    dash_table.DataTable(  
        columns=[{"name": col, "id": col} for col in data.columns],
        data=data.to_dict("records"),
        page_size=10
    )
])

# Run the app with the updated method
if __name__ == "__main__":
    app.run(debug=True)
