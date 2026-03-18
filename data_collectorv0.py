"""
THE APP:
Weather data collector that fetches current weather and 7-day forecasts
for multiple cities and saves data to CSV files for analysis.

WHAT TO FIGURE OUT:
- How do you fetch weather data from an API?
- How do you handle multiple cities in one session?
- How do you process forecast data (multiple timestamps per day)?
- How do you aggregate daily highs and lows from hourly data?
- How do you save data to CSV with pandas?

START HERE:
First, get city names from user.
Then fetch current weather for each city.
Then fetch 7-day forecasts and aggregate by day.
Finally, save all data to CSV files.

KEY CONCEPT:
OpenWeatherMap returns current weather in one API call.
Forecast API returns 3-hour intervals for 5 days (40 data points).
Group forecast data by date to get daily highs/lows.
Use pandas DataFrame to organize and save data.
Store timestamp for tracking when data was collected.
"""

#---------------------------------------------
# THE CODE SKELETON

# Import necessary libraries
# (requests for API, pandas for data handling, datetime for timestamps)
from datetime import datetime
import os

import pandas as pd
import requests
from dotenv import load_dotenv



# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError(
        "API key not found. Add OPENWEATHER_API_KEY or WEATHER_API_KEY to your .env file."
    )


# Print header
print("=" * 72)
print("Weather Data Collector")
print("Collecting current weather and forecast data for selected cities")
print("=" * 72)


# Get cities from user
cities_input = input("Enter city names separated by commas: ").strip()
cities = [city.strip() for city in cities_input.split(",") if city.strip()]

if not cities:
    raise ValueError("No valid cities provided. Please enter at least one city.")


# Print status message
print(f"\nStarting data collection for {len(cities)} city/cities...")


# Create empty lists for data storage
current_weather_data = []
forecast_data = []



# Print current weather header
print("\n" + "-" * 72)
print("Current Weather")
print("-" * 72)


# Loop through each city

    # Build API URL for current weather
    
    
    # Fetch data
    
    
    
        # Extract weather data
        
        
        
        
        
        
        
        
        # Print formatted row
        
        
        # Store data in list
        
        
        
        
        
        
        
        
        

# Print separator


# Loop through cities for forecast data

    # Build forecast API URL
    
    
    # Fetch forecast data
    
    
    
        # Print forecast header
        
        
        
        # Create dictionary to group by date
        
        
        # Loop through forecast items (3-hour intervals)
        
            # Extract date and data
            
            
            
            
            
            # Group by date
            
            
            
            
            
            
        
        # Display daily forecasts (first 7 days)
        
        
            
            # Calculate high and low from temps list
            
            
            
            # Print row
            
            
            # Store forecast data
            
            
            
            
            
            
            
            

# Get timestamp for filenames


# Save current weather data to CSV


# Save forecast data to CSV


# Print completion message


