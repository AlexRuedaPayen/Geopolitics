from app import app
from config import get_config

cfg = get_config()

if __name__ == "__main__":
    app.run(debug=cfg.DEBUG, host="0.0.0.0", port=cfg.PORT)
