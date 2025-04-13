import os
from dotenv import load_dotenv
import dash
import dash_bootstrap_components as dbc
from config import get_config
from app.layout import layout
from app.callbacks import register_callbacks


env_name = os.getenv("APP_ENV", "development")
env_file = f".env.{env_name}"
load_dotenv(env_file)



config = get_config()
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server 

# ---------------------------
app.layout = layout
register_callbacks(app)



if __name__ == "__main__":
    print(f"🚧 Starting app in {config.ENV} mode on port {config.PORT}")
    app.run_server(debug=config.DEBUG, host=config.HOST, port=config.PORT)
