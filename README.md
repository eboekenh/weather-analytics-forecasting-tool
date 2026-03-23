# 🌦️ Weather Analytics & Forecasting Tool

Python data collection pipeline that fetches real-time weather conditions and 5-day forecasts for multiple cities using the OpenWeatherMap API, with CSV export and formatted terminal output.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![API](https://img.shields.io/badge/API-OpenWeatherMap-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Real-time weather data** — Temperature, feels-like, humidity, wind speed, conditions
- **5-day forecast** — Daily high/low temperatures, conditions, rain probability
- **Multi-city support** — Query multiple cities in a single run
- **Dual output** — Formatted terminal tables + timestamped CSV files
- **Secure API handling** — API key loaded from `.env` file via python-dotenv

## Output Files

| File | Contents |
|------|----------|
| `weather_data_YYYY-MM-DD.csv` | Current conditions: timestamp, city, temperature, feels_like, humidity, wind_speed, condition |
| `forecast_data_YYYY-MM-DD.csv` | Forecast: city, date, high_temp, low_temp, condition, rain_probability |

## Tech Stack

- **Python 3.8+** — Core language
- **Requests** — HTTP client for OpenWeatherMap API
- **Pandas** — DataFrame creation and CSV export
- **python-dotenv** — Secure environment variable loading

## Getting Started

```bash
git clone https://github.com/eboekenh/weather-analytics-forecasting-tool.git
cd weather-analytics-forecasting-tool
pip install -r requirements.txt
```

### API Key Setup

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Add your API key to `.env`:
   ```
   WEATHER_API_KEY=your_actual_api_key
   ```

### Run

```bash
python data_collector.py
```

Enter comma-separated city names when prompted (e.g., `Berlin, Istanbul, London`).

## Example Output

```
City          | Temp (°C) | Feels Like | Humidity | Wind (km/h) | Condition
---------------------------------------------------------------------------
Berlin        |     12.3  |      10.1  |     67%  |       15.2  | Clouds
Istanbul      |     18.7  |      17.5  |     55%  |       11.8  | Clear
London        |     10.5  |       8.2  |     78%  |       20.4  | Rain
```

## License

MIT
