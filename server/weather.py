import json
import datetime
import requests


url = 'https://api.weatherapi.com/v1/'

class Weather:
    def __init__(self):
        self.location_found = False
        self.date_available = False
        self.high_temp = -273
        self.low_temp = -273
        self.error = False
        self.error_message = ''
        self.location = ''


def weather(location: str, date, api_key):
    """
    Communicate with weather API
    :param str location: location string, can be as long as the GET URL allows
    :param datetime.date date: date for the weather
    :param str api_key: weather API key
    :return: a Weather object
    """
    location = location.replace('&', '')

    data = {
        'key': api_key,
        'q': location,
        'days': 10,
        'aqi': 'no',
        'alerts': 'no',
    }

    request_url = url + 'forecast.json?' + '&'.join(f"{key}={value}" for key, value in data.items())
    response = requests.get(request_url)
    response_body = json.loads(response.text)

    weather_data = Weather()

    if response.status_code == 400 and response_body['error']['code'] == 1006:
        weather_data.location_found = False
    elif response.status_code != 200:
        if 'error' in response_body.keys():
            if 'message' in response_body['error'].keys():
                weather_data.error_message = response_body['error']['message']
            else:
                weather_data.error_message = 'Weather API error.'
        else:
                weather_data.error_message = 'Weather API error.'
    else:
        try:
            high_temp, low_temp = extract_temp(response_body, date)
            weather_data.location_found = True
            weather_data.date_available = True
            weather_data.high_temp = high_temp
            weather_data.low_temp = low_temp
            weather_data.location = ', '.join([
                response_body['location']['name'],
                response_body['location']['region'],
                response_body['location']['country'],
            ])
        except TypeError:
            weather_data.location_found = True
            weather_data.date_available = False

    return weather_data


def extract_temp(data, date):
    """
    Extract high and low temperature from the response data
    :param dict data: Response data for a single day, must be under "forecastday"
    :param datetime.date date: date to extract
    :return: if successful, (high, low) temp (always celsius)
    """
    forecast_date = data['forecast']['forecastday']
    for day in forecast_date:
        if day['date'] == str(date):
            high_temp = day['day']['maxtemp_c']
            low_temp = day['day']['mintemp_c']
            return high_temp, low_temp
    return False
