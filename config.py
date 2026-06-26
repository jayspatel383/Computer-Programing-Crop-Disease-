"""
Configuration file for Crop Disease Early Warning System
"""

# API Configuration
OPENWEATHER_API_KEY = "you api key"  # 1957925618b635c26a59793ae2d0755d  this is the api key please add in #
AGROMONITORING_API_KEY = "your api key"   #c1ecb930ebbc8ad836130d33c7bc9dbc this api key for agro monitering #

# Application Settings
APP_NAME = "Crop Disease Early Warning System"
APP_VERSION = "1.0.0"

# Data refresh settings (in seconds)
DATA_REFRESH_INTERVAL = 300

# Default locations - India + Europe
DEFAULT_LOCATIONS = [
    {"name": "Punjab, IN", "city": "Ludhiana", "lat": 30.90, "lon": 75.85},
    {"name": "Maharashtra, IN", "city": "Pune", "lat": 18.52, "lon": 73.85},
    {"name": "West Bengal, IN", "city": "Kolkata", "lat": 22.57, "lon": 88.36},
    {"name": "Germany", "city": "Berlin", "lat": 52.52, "lon": 13.40},
    {"name": "France", "city": "Paris", "lat": 48.85, "lon": 2.35},
    {"name": "Italy", "city": "Rome", "lat": 41.90, "lon": 12.49},
    {"name": "Spain", "city": "Madrid", "lat": 40.41, "lon": -3.70},
    {"name": "Netherlands", "city": "Amsterdam", "lat": 52.37, "lon": 4.89},
]

# Color scheme for risk levels
RISK_COLORS = {
    'CRITICAL': '#FF0000',
    'HIGH': '#FF6600',
    'MODERATE': '#FFCC00',
    'LOW': '#33CC33',
    'MINIMAL': '#009933'
}
