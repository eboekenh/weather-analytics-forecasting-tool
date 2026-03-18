"""
THE APP:
Weather data collector that fetches current weather and 7-day forecasts
for multiple cities and saves data to CSV files for analysis.
"""

#1. IMPORTS
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# 2. LOAD API KEY 
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')

# 3. HEADER
print("=" * 55)
print("       WEATHER DATA COLLECTOR")
print("=" * 55)

# 4. GET CITIES FROM USER 
user_input = input("\nEnter city names separated by commas: ")
cities = [city.strip() for city in user_input.split(",")]

# 5. STATUS MESSAGE 
print(f"\nFetching weather data for {len(cities)} city/cities...\n")

# 6. EMPTY LISTS FOR DATA STORAGE 
current_weather_data = []
forecast_data = []

# 7. CURRENT WEATHER HEADER 
print(f"{'City':<15} {'Temp (°C)':>10} {'Feels Like':>12} {'Humidity':>10} {'Description':<20}")
print("-" * 70)

# ── 8. LOOP: CURRENT WEATHER ─────────────────────────────────
for city in cities:

    # Build API URL for current weather
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    # Fetch data
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract weather data
        temp        = data["main"]["temp"]
        feels_like  = data["main"]["feels_like"]
        humidity    = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed  = data["wind"]["speed"]
        city_name   = data["name"]
        country     = data["sys"]["country"]

        # Print formatted row
        print(f"{city_name:<15} {temp:>9.1f}° {feels_like:>10.1f}° {humidity:>9}% {description:<20}")

        # Store data in list
        current_weather_data.append({
            "city":        city_name,
            "country":     country,
            "temp_c":      temp,
            "feels_like_c": feels_like,
            "humidity_pct": humidity,
            "wind_speed_ms": wind_speed,
            "description": description,
        })

    else:
        print(f"{city:<15} ❌ Not found (status {response.status_code})")

# ── 9. SEPARATOR ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("       5-DAY FORECAST (daily highs & lows)")
print("=" * 55)

# ── 10. LOOP: FORECAST DATA ──────────────────────────────────
for city in cities:

    # Build forecast API URL
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    # Fetch forecast data
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Print forecast header for this city
        city_name = data["city"]["name"]
        country   = data["city"]["country"]
        print(f"\n📍 {city_name}, {country}")
        print(f"{'Date':<12} {'High (°C)':>10} {'Low (°C)':>10} {'Humidity':>10} {'Description':<20}")
        print("-" * 65)

        # Create dictionary to group forecast items by date
        # key = "YYYY-MM-DD", value = dict with lists of values
        daily = {}

        # Loop through forecast items (3-hour intervals, 40 total)
        for item in data["list"]:

            # Extract date (first 10 chars of "2024-01-15 12:00:00")
            dt_text     = item["dt_txt"]
            date        = dt_text[:10]
            temp        = item["main"]["temp"]
            humidity    = item["main"]["humidity"]
            description = item["weather"][0]["description"]

            # Group by date — if date not seen yet, create entry
            if date not in daily:
                daily[date] = {
                    "temps":        [],
                    "humidities":   [],
                    "descriptions": [],
                }

            # Append this 3-hour snapshot to the day's lists
            daily[date]["temps"].append(temp)
            daily[date]["humidities"].append(humidity)
            daily[date]["descriptions"].append(description)

        # Display daily forecasts (up to 5 days, API limit)
        for date, values in list(daily.items())[:5]:

            # Calculate high and low from all temps recorded that day
            high = max(values["temps"])
            low  = min(values["temps"])

            # Most common description for the day
            avg_humidity  = round(sum(values["humidities"]) / len(values["humidities"]))
            main_desc     = max(set(values["descriptions"]), key=values["descriptions"].count)

            # Print row
            print(f"{date:<12} {high:>9.1f}° {low:>9.1f}° {avg_humidity:>9}% {main_desc:<20}")

            # Store forecast data
            forecast_data.append({
                "city":           city_name,
                "country":        country,
                "date":           date,
                "high_c":         high,
                "low_c":          low,
                "avg_humidity_pct": avg_humidity,
                "description":    main_desc,
            })

# ── 11. TIMESTAMP FOR FILENAMES ──────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ── 12. SAVE CURRENT WEATHER TO CSV ─────────────────────────
df_current = pd.DataFrame(current_weather_data)
current_file = f"current_weather_{timestamp}.csv"
df_current.to_csv(current_file, index=False)

# ── 13. SAVE FORECAST DATA TO CSV ────────────────────────────
df_forecast = pd.DataFrame(forecast_data)
forecast_file = f"forecast_{timestamp}.csv"
df_forecast.to_csv(forecast_file, index=False)

# ── 14. COMPLETION MESSAGE ───────────────────────────────────
print(f"\n{'=' * 55}")
print(f"✅ Data saved:")
print(f"   • {current_file}  ({len(current_weather_data)} cities)")
print(f"   • {forecast_file}  ({len(forecast_data)} daily entries)")
print(f"{'=' * 55}\n")