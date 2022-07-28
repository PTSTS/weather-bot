import json
from flask import Flask, request, make_response, jsonify, Response
from server.weather import weather
from server.availability import *
import datetime


app = Flask(__name__)
config_file = '../config/config.json'
""" Config file should be json and contains "key", an API key to www.weatherapi.com, also optionally "port", 
the port number."""

with open(config_file, 'r') as config_file_pointer:
    config_data = json.load(config_file_pointer)
    if 'port' in config_data.keys():
        port = int(config_data['port'])
    else:
        port = 80
    api_key = config_data['key']


@app.route('/weather', methods=['GET', 'POST'])
def check_weather():
    request_body = json.loads(request.data)
    date_dict = request_body['sessionInfo']['parameters']['date']
    session_name = request_body['sessionInfo']['session']
    date = datetime.date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))
    try:
        location_list = request_body['sessionInfo']['parameters']['location']
    except:
        location_list = None

    if type(location_list) is list:
        location = ', '.join(location_list)
    else:
        location = location_list

    if location is None:
        return check_date(date, session_name)

    if 'date_validated' in request_body['sessionInfo']['parameters'].keys():
        if not request_body['sessionInfo']['parameters']['date_validated']:
            return check_date(date, session_name)

    if 'display' in request_body['sessionInfo']['parameters'].keys():
        if not request_body['sessionInfo']['parameters']['display']:
            return check_date(date, session_name)

    day_weather = weather(location, date, api_key)

    return check_availability(date, day_weather, session_name, location)


if __name__ == '__main__':
    app.run(host='localhost', port=port, debug=True)
