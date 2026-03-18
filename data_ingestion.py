import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')

print("Weather Data Collector")
print("======================\n")

cities_input = input("Enter cities (comma-separated): ")
cities = [city.strip() for city in cities_input.split(',')]

print("\nFetching weather data...\n")

current_weather_data = []
forecast_data = []

print("CURRENT WEATHER")
print("─" * 80)
print(f"{'City':<15} {'Temp':<8} {'Feels':<8} {'Humidity':<10} {'Wind':<12} {'Condition'}")
print("─" * 80)

for city in cities:
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(current_url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed'] * 3.6
            condition = data['weather'][0]['main']
            description = data['weather'][0]['description']
            
            print(f"{city:<15} {temp:.0f}°C    {feels_like:.0f}°C    {humidity}%        {wind_speed:.0f} km/h    {description.capitalize()}")
            
            current_weather_data.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city': city,
                'temperature': temp,
                'feels_like': feels_like,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'condition': condition,
                'description': description
            })
        else:
            print(f"{city:<15} Error: City not found")
    
    except Exception as e:
        print(f"{city:<15} Error: {e}")

print("─" * 80)
print()

for city in cities:
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(forecast_url)
        data = response.json()
        
        if response.status_code == 200:
            print(f"7-DAY FORECAST - {city}")
            print("─" * 80)
            print(f"{'Date':<15} {'High':<8} {'Low':<8} {'Condition':<20} {'Rain%'}")
            print("─" * 80)
            
            daily_forecasts = {}
            
            for item in data['list']:
                date = item['dt_txt'].split(' ')[0]
                temp = item['main']['temp']
                condition = item['weather'][0]['description']
                rain_prob = item.get('pop', 0) * 100
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'temps': [],
                        'condition': condition,
                        'rain_prob': rain_prob
                    }
                
                daily_forecasts[date]['temps'].append(temp)
            
            count = 0
            for date, info in sorted(daily_forecasts.items())[:7]:
                high = max(info['temps'])
                low = min(info['temps'])
                
                print(f"{date:<15} {high:.0f}°C    {low:.0f}°C    {info['condition'].capitalize():<20} {info['rain_prob']:.0f}%")
                
                forecast_data.append({
                    'city': city,
                    'date': date,
                    'high_temp': high,
                    'low_temp': low,
                    'condition': info['condition'],
                    'rain_probability': info['rain_prob']
                })
                
                count += 1
                if count >= 7:
                    break
            
            print("─" * 80)
            print()
    
    except Exception as e:
        print(f"Error fetching forecast for {city}: {e}\n")

timestamp_str = datetime.now().strftime('%Y-%m-%d')

if current_weather_data:
    df_current = pd.DataFrame(current_weather_data)
    current_filename = f"weather_data_{timestamp_str}.csv"
    df_current.to_csv(current_filename, index=False)
    print(f"✓ Data saved to {current_filename}")

if forecast_data:
    df_forecast = pd.DataFrame(forecast_data)
    forecast_filename = f"forecast_data_{timestamp_str}.csv"
    df_forecast.to_csv(forecast_filename, index=False)
    print(f"✓ Forecast data saved to {forecast_filename}")

print("\nData collection complete!")
print("Files ready for analysis.")
