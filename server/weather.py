import json
import datetime
import requests


# api_key = json.load(open('../config/config.json', 'r'))['key']  # this config file is not on the Github repo
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
    current_date = datetime.date.today()
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
    print(request_url)

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
    # elif len(response_body["forecast"]['forecastday']) < data['days']:
    #     print(response_body)
    #     weather_data.location_found = True
    #     weather_data.date_available = False
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
            print(response_body)
            weather_data.location_found = True
            weather_data.date_available = False

    return weather_data


def extract_temp(data, date):
    date_id = f'{date.year}-{date.month}-{date.day}'
    forecast_date = data['forecast']['forecastday']
    for day in forecast_date:
        if day['date'] == str(date):
            high_temp = day['day']['maxtemp_c']
            low_temp = day['day']['mintemp_c']
            return high_temp, low_temp
    return False


"""https://api.weatherapi.com/v1/forecast.json?key=99ad5d86dfef45649f3135458222607 &q=LA&days=10&aqi=no&alerts=no"""
if __name__ == '__main__':
    weather('London', datetime.date(2022, 7, 29), "99ad5d86dfef45649f3135458222607 ")