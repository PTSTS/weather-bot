import json
import datetime


api_key = json.load(open('config.json', 'r'))['key']  # this config file is not on the Github repo


def check_weather(location: str, date):
    current_date = datetime.datetime.now().date()
    request_body = {
        'key': api_key,
        'q': location,

    }