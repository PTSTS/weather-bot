import json


api_key = json.load(open('config.json'))

def check_weather(location: str, date):
    request_body = {
        'key': '',
        'q': location,

    }
