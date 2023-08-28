import datetime
import requests
from django.shortcuts import render


# Create your views here.
def index(request):
    # Read the API key from a file
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        # Get city names from the form
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        # Fetch weather data and daily forecasts for city1
        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        # Fetch weather data and daily forecasts for city2 if provided
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetch current weather data
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']

    # Fetch daily forecast data
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    # Extract relevant weather data
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    # Extract daily forecasts
    daily_forecasts = []
    for daily_data in forecast_response.get('daily', [])[:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
            "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })

    return weather_data, daily_forecasts
