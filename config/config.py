import os
from dotenv import load_dotenv

env_name = os.getenv("APP_ENV", "development")
env_file = f".env.{env_name}"
load_dotenv(env_file)

class Config:
    ENV = env_name
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8050))
    DEBUG = os.getenv("DEBUG", "False") == "True"
    ALLOWED_IPS = os.getenv("ALLOWED_IPS", "").split()

config = Config()
