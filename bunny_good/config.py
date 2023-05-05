import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base config, uses staging database server."""

    TESTING = True
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_USER = ""
    DB_PASSWORD = ""
    DB_DATABASE = ""
    SHIOAJI_API_KEY = ""
    SHIOAJI_SECRET = ""


class ProductionConfig(BaseConfig):
    """Uses production database server."""

    TESTING = False
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = int(os.environ.get("DB_PORT")) if os.environ.get("DB_PORT") else 0
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    SHIOAJI_API_KEY = os.environ.get("SHIOAJI_API_KEY")
    SHIOAJI_SECRET = os.environ.get("SHIOAJI_SECRET")


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = int(os.environ.get("DB_PORT")) if os.environ.get("DB_PORT") else 0
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    SHIOAJI_API_KEY = os.environ.get("SHIOAJI_API_KEY")
    SHIOAJI_SECRET = os.environ.get("SHIOAJI_SECRET")

if os.environ.get("ENV", "dev") == "dev":
    Config = DevelopmentConfig()

elif os.environ.get("ENV") == "prod":
    Config = ProductionConfig()
    
else:
    Config = BaseConfig()
