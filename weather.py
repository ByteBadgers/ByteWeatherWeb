# weather.py
import os, requests
from dotenv import load_dotenv
from datetime import datetime
import datetime

# load .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path, override=True)
API_KEY = os.getenv("OPENWEATHER_KEY")

def get_weather(city="Austin"):
    if not API_KEY:
        return {"city_name": "Unknown", "main": "Clear", "temp": "—", 
                "temp_min": "—", "temp_max": "—", "feels_like": "—", 
                "humidity": "—", "icon": "01d"}
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},US&units=imperial&appid={API_KEY}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
        return {
            "city_name": raw.get("name", "Unknown"),
            "main": raw["weather"][0]["main"],
            "temp": round(raw["main"]["temp"]),
            "temp_min": round(raw["main"]["temp_min"]),
            "temp_max": round(raw["main"]["temp_max"]),
            "feels_like": round(raw["main"]["feels_like"]),
            "humidity": raw["main"]["humidity"],
            "icon": raw["weather"][0]["icon"]
        }
    except Exception as e:
        print("API error:", e)
        return {"city_name": city, "main": "Error", "temp": "—", 
                "temp_min": "—", "temp_max": "—", "feels_like": "—", 
                "humidity": "—", "icon": "01d"}

def get_forecast(city="Austin"):
    if not API_KEY:
        return []

    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},US&units=imperial&appid={API_KEY}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()

        forecast_data = []
        # Take forecast at ~12:00 PM for each of the next 3 days
        for i in range(0, len(raw["list"]), 8):  # every 24h (8 * 3h intervals)
            entry = raw["list"][i]

            # Convert to weekday name
            date_str = entry["dt_txt"].split(" ")[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            weekday = date_obj.strftime("%A")

            day = {
                "date": weekday,
                "temp": round(entry["main"]["temp"]),
                "main": entry["weather"][0]["main"],
                "icon": entry["weather"][0]["icon"]
            }
            forecast_data.append(day)
            if len(forecast_data) == 3:  # only keep 3 days
                break

        return forecast_data
    except Exception as e:
        print("Forecast API error:", e)
        return []


