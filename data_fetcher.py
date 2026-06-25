"""
Data Fetcher Module - API Integration
Fetches real weather data from OpenWeatherMap and Agromonitoring APIs
"""

import requests
from datetime import datetime, timedelta
import time

try:
    from config import OPENWEATHER_API_KEY, AGROMONITORING_API_KEY, DATA_REFRESH_INTERVAL
except ImportError:
    OPENWEATHER_API_KEY = "your_key"
    AGROMONITORING_API_KEY = "your_key"
    DATA_REFRESH_INTERVAL = 300


class DataFetcher:
    """Main data fetcher that combines all data sources"""
    
    def __init__(self):
        self.cache = {}
        self.last_fetch_time = {}
    
    def fetch_current_weather(self, city="Berlin", country=None):
        """Fetch current weather from OpenWeatherMap"""
        # Auto-detect country from city name
        if country is None:
            country = self._get_country(city)
        
        cache_key = f"{city}_{country}"
        
        # Check cache
        if cache_key in self.last_fetch_time:
            if time.time() - self.last_fetch_time[cache_key] < DATA_REFRESH_INTERVAL:
                if cache_key in self.cache:
                    print(f"📦 Using cached weather for {city}")
                    return self.cache[cache_key]
        
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{city},{country}",
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        try:
            print(f"📡 Fetching weather for {city}, {country}...")
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code != 200:
                print(f"⚠️ API error for {city}: {data.get('message', 'Unknown')}")
                return self._demo_weather(city)
            
            weather_data = {
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'cloud_cover': data['clouds']['all'],
                'weather_description': data['weather'][0]['description'],
                'city_name': data['name'],
                'country': data['sys']['country'],
                'rainfall_1h': data.get('rain', {}).get('1h', 0),
                'rainfall_3h': data.get('rain', {}).get('3h', 0),
                'timestamp': datetime.now().isoformat(),
                'demo_data': False
            }
            
            # Cache the data
            self.cache[cache_key] = weather_data
            self.last_fetch_time[cache_key] = time.time()
            
            print(f"✅ {city}: {weather_data['temperature']}°C, Humidity: {weather_data['humidity']}%, "
                  f"Rain: {weather_data['rainfall_3h']}mm")
            return weather_data
            
        except Exception as e:
            print(f"❌ Weather fetch error for {city}: {e}")
            return self._demo_weather(city)
    
    def fetch_forecast(self, city="Berlin", country=None):
        """Fetch 5-day forecast for consecutive condition analysis"""
        if country is None:
            country = self._get_country(city)
        
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': f"{city},{country}",
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        try:
            print(f"📡 Fetching forecast for {city}...")
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code != 200:
                print(f"⚠️ Forecast API error: {data.get('message', 'Unknown')}")
                return self._demo_forecast()
            
            # Count consecutive favorable hours (humidity >= 75%)
            consecutive_75 = 0
            max_consecutive_75 = 0
            total_rainfall = 0
            
            for item in data['list']:
                humidity = item['main']['humidity']
                rainfall = item.get('rain', {}).get('3h', 0)
                total_rainfall += rainfall
                
                if humidity >= 75:
                    consecutive_75 += 3  # Each forecast interval is 3 hours
                    max_consecutive_75 = max(max_consecutive_75, consecutive_75)
                else:
                    consecutive_75 = 0
            
            result = {
                'consecutive_hours_humidity_75': max_consecutive_75,
                'consecutive_days': round(max_consecutive_75 / 24, 1),
                'total_rainfall_5day': round(total_rainfall, 1),
                'demo_data': False
            }
            
            print(f"✅ Forecast: {max_consecutive_75}h consecutive humidity, "
                  f"Total rain: {total_rainfall:.1f}mm")
            return result
            
        except Exception as e:
            print(f"❌ Forecast error for {city}: {e}")
            return self._demo_forecast()
    
    def quick_fetch(self, crop, location):
        """Quick fetch for disease prediction - returns essential data"""
        city = location.get('city', 'Berlin')
        
        # Fetch data
        weather = self.fetch_current_weather(city)
        forecast = self.fetch_forecast(city)
        
        # Calculate daily rainfall from 3-hour data
        rainfall_24h = weather.get('rainfall_3h', 0) * 8  # Approximate
        
        # Build the data dictionary needed by disease engine
        result = {
            'temperature': weather['temperature'],
            'humidity': weather['humidity'],
            'rainfall_24h': round(rainfall_24h, 1),
            'wind_speed': weather['wind_speed'],
            'cloud_cover': weather['cloud_cover'],
            'consecutive_favorable_hours': forecast.get('consecutive_hours_humidity_75', 0),
            'consecutive_condition_days': forecast.get('consecutive_days', 0),
            'total_rainfall_5day': forecast.get('total_rainfall_5day', 0),
            'timestamp': datetime.now().isoformat(),
            'demo_data': weather.get('demo_data', False) or forecast.get('demo_data', False)
        }
        
        return result
    
    def _get_country(self, city):
        """Auto-detect country code from city name"""
        city_country_map = {
            'Berlin': 'DE', 'Paris': 'FR', 'Rome': 'IT', 'Madrid': 'ES',
            'Amsterdam': 'NL', 'Warsaw': 'PL', 'London': 'GB',
            'Ludhiana': 'IN', 'Pune': 'IN', 'Kolkata': 'IN',
            'Karnal': 'IN', 'Meerut': 'IN',
        }
        return city_country_map.get(city, 'DE')  # Default to Germany
    
    def _demo_weather(self, city="Demo"):
        """Demo data when API fails"""
        print(f"📦 Using demo weather data for {city}")
        return {
            'temperature': 22.5,
            'feels_like': 21.0,
            'humidity': 85,
            'pressure': 1012,
            'wind_speed': 8.5,
            'cloud_cover': 75,
            'weather_description': 'overcast clouds',
            'city_name': city,
            'country': 'DE',
            'rainfall_1h': 0.5,
            'rainfall_3h': 1.2,
            'timestamp': datetime.now().isoformat(),
            'demo_data': True
        }
    
    def _demo_forecast(self):
        """Demo forecast data"""
        print("📦 Using demo forecast data")
        return {
            'consecutive_hours_humidity_75': 48,
            'consecutive_days': 2.0,
            'total_rainfall_5day': 5.5,
            'demo_data': True
        }