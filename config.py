import os

class BaseConfig:
    DEBUG = False
    PORT = 8050

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    PORT = 8050

class StagingConfig(BaseConfig):
    DEBUG = True
    PORT = 8051

class ProductionConfig(BaseConfig):
    DEBUG = False
    PORT = 8052

config_map = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}

def get_config():
    env = os.getenv("APP_ENV", "development")
    return config_map.get(env, DevelopmentConfig)()
