

import requests

def get_weather_data(location):
    api_key = '018ee17c36044d5fb01141237240904'  # Replace 'YOUR_API_KEY' with your actual API key from WeatherAPI
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no'

    try:
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            print(f"Error: {data['error']['message']}")
            return None
        else:
           weather_info = {
                'Temperature': {
                    'value': data['current']['temp_c'],
                    'unit': '°C',
                    'info': 'The current temperature in Celsius.'
                },
                'Description': {
                    'value': data['current']['condition']['text'],
                    'info': 'A brief description of the weather condition.'
                },
                'Humidity': {
                    'value': data['current']['humidity'],
                    'unit': '%',
                    'info': 'The relative humidity percentage.'
                },
                'Wind Speed': {
                    'value': data['current']['wind_kph'],
                    'unit': 'km/h',
                    'info': 'The wind speed in kilometers per hour.'
                }
           }              
           return weather_info
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

