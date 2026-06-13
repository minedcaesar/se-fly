import os


class Config:
    SECRET_KEY = "fly-dev-secret-2026"
    DATABASE = os.path.join(os.path.dirname(__file__), "database", "fly.db")
    ENVIRONMENT = "development"
    AIRPORT_IATA_CODE = "TN"
