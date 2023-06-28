import os
from dotenv import load_dotenv

if not os.path.exists(".env"):
    raise Exception("please provide .env")
load_dotenv()


class BaseConfig:
    """Base config, uses staging database server."""

    TESTING = True
    DB_QUOTE_HOST = "localhost"
    DB_QUOTE_PORT = 5432
    DB_QUOTE_USER = ""
    DB_QUOTE_PASSWORD = ""
    DB_QUOTE_DATABASE = ""
    SHIOAJI_API_KEY = ""
    SHIOAJI_SECRET = ""
    DB_PREFECT_HOST = "127.0.0.1"
    DB_PREFECT_PORT = 5432
    DB_PREFECT_USER = ""
    DB_PREFECT_PASSWORD = ""
    DB_PREFECT_DATABASE = ""
    GMAIL_MAIL = ""
    GMAIL_API_KEY = ""
    GMAIL_ALERT_TO = ""


class ProductionConfig(BaseConfig):
    """Uses production database server."""

    TESTING = False
    DB_QUOTE_HOST = os.environ.get("DB_QUOTE_HOST")
    DB_QUOTE_PORT = (
        int(os.environ.get("DB_QUOTE_PORT")) if os.environ.get("DB_QUOTE_PORT") else 0
    )
    DB_QUOTE_USER = os.environ.get("DB_QUOTE_USER")
    DB_QUOTE_PASSWORD = os.environ.get("DB_QUOTE_PASSWORD")
    DB_QUOTE_DATABASE = os.environ.get("DB_QUOTE_DATABASE")
    SHIOAJI_API_KEY = os.environ.get("SHIOAJI_API_KEY")
    SHIOAJI_SECRET = os.environ.get("SHIOAJI_SECRET")
    DB_PREFECT_HOST = os.environ.get("DB_PREFECT_HOST")
    DB_PREFECT_PORT = (
        int(os.environ.get("DB_PREFECT_PORT"))
        if os.environ.get("DB_PREFECT_PORT")
        else 0
    )
    DB_PREFECT_USER = os.environ.get("DB_PREFECT_USER")
    DB_PREFECT_PASSWORD = os.environ.get("DB_PREFECT_PASSWORD")
    DB_PREFECT_DATABASE = os.environ.get("DB_PREFECT_DATABASE")
    GMAIL_MAIL = os.environ.get("GMAIL_MAIL")
    GMAIL_API_KEY = os.environ.get("GMAIL_API_KEY")
    GMAIL_ALERT_TO = os.environ.get("GMAIL_ALERT_TO")


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DB_QUOTE_HOST = os.environ.get("DB_QUOTE_HOST")
    DB_QUOTE_PORT = (
        int(os.environ.get("DB_QUOTE_PORT")) if os.environ.get("DB_QUOTE_PORT") else 0
    )
    DB_QUOTE_USER = os.environ.get("DB_QUOTE_USER")
    DB_QUOTE_PASSWORD = os.environ.get("DB_QUOTE_PASSWORD")
    DB_QUOTE_DATABASE = os.environ.get("DB_QUOTE_DATABASE")
    SHIOAJI_API_KEY = os.environ.get("SHIOAJI_API_KEY")
    SHIOAJI_SECRET = os.environ.get("SHIOAJI_SECRET")
    DB_PREFECT_HOST = os.environ.get("DB_PREFECT_HOST")
    DB_PREFECT_PORT = (
        int(os.environ.get("DB_PREFECT_PORT"))
        if os.environ.get("DB_PREFECT_PORT")
        else 0
    )
    DB_PREFECT_USER = os.environ.get("DB_PREFECT_USER")
    DB_PREFECT_PASSWORD = os.environ.get("DB_PREFECT_PASSWORD")
    DB_PREFECT_DATABASE = os.environ.get("DB_PREFECT_DATABASE")
    GMAIL_MAIL = os.environ.get("GMAIL_MAIL")
    GMAIL_API_KEY = os.environ.get("GMAIL_API_KEY")
    GMAIL_ALERT_TO = os.environ.get("GMAIL_ALERT_TO")


if os.environ.get("ENV", "dev") == "dev":
    Config = DevelopmentConfig()

elif os.environ.get("ENV") == "prod":
    Config = ProductionConfig()

else:
    Config = BaseConfig()
