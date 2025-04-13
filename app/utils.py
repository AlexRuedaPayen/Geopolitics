import pandas as pd
import numpy as np

# ---------------------------
# 🌍 Country / Region Mapping
# ---------------------------
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

# ---------------------------
# 🏭 Sector Simulation
# ---------------------------
sectors = [
    "Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples",
    "Healthcare", "Financials", "Information Technology", "Telecommunications", "Utilities", "Real Estate"
]

# ---------------------------
# 📊 Random Data Generation
# ---------------------------
np.random.seed(42)
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
