## @file config.py
#  @brief Application configuration.

import os


## @brief Flask configuration values loaded via app.config.from_object.
class Config:
    ## Secret key used to sign session cookies.
    SECRET_KEY = "fly-dev-secret-2026"
    ## Absolute path to the SQLite database file.
    DATABASE = os.path.join(os.path.dirname(__file__), "database", "fly.db")
    ## Current runtime environment.
    ENVIRONMENT = "development"
    ## IATA code of this airport (used to split the flight board).
    AIRPORT_IATA_CODE = "TN"
