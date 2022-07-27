import json
from flask import Flask, request, make_response, jsonify, Response
from server.response import fulfillment_response
from server.weather import weather
import datetime


app = Flask(__name__)
config_file = '../config/config.json'
with open(config_file, 'r') as config_file_pointer:
    config_data = json.load(config_file_pointer)
    if 'port' in config_data.keys():
        port = int(config_data['port'])
    else:
        port = 80
    api_key = config_data['key']


@app.route('/')
def index():
    pass


@app.route('/weather', methods=['GET', 'POST'])
def check_weather():
    request_body = json.loads(request.data)
    date_dict = request_body['sessionInfo']['parameters']['date']
    session_name = request_body['sessionInfo']['session']
    date = datetime.date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))
    location_list = request_body['sessionInfo']['parameters']['location']
    if type(location_list) is list:
        location = ', '.join(location_list)
    else:
        location = location_list
    day_weather = weather(location, date, api_key)
    if day_weather.location_found and day_weather.date_available:
        response = fulfillment_response(
            f"""You asked for the weather on {date.day}/{date.month}/{date.year} in the location:
{day_weather.location}. \nThe lowest temperature is {day_weather.low_temp} C, the highest temperature is 
{day_weather.high_temp} C. Is this the right location you are looking for?""",
            parameters={'location_validated': True}, session=session_name
        )
    elif day_weather.location_found and not day_weather.date_available:
        response = fulfillment_response(
            f"""Sorry, we don't have the forecast on this day for this location, can you try an earlier date?""",
            parameters={'location_validated': True, 'date_validated': False, 'date': None}, session=session_name
        )
    elif not day_weather.location_found:
        response = fulfillment_response(
            f"""We couldn't find this location "{location}".""",
            parameters={'location_validated': False, 'location': None}, session=session_name
        )
    else:
        response = fulfillment_response(
            f"""Sorry, something went wrong. {day_weather.error_message}.""",
            parameters={'location_validated': False}, session=session_name
        )

    return make_response(jsonify(response))


@app.route('/date', methods=['GET', 'POST'])
def check_date():
    request_body = json.loads(request.data)
    date_dict = request_body['sessionInfo']['parameters']['date']
    session_name = request_body['sessionInfo']['session']
    print(request_body['sessionInfo'])

    date = datetime.date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))
    current_date = datetime.date.today()

    if date - current_date > datetime.timedelta(days=10):
        response = fulfillment_response(
            """Sorry, we can only provide forecast for the next 10 days.""",
            parameters={'date_validated': False, 'date': None}, session=session_name
        )
    elif date < datetime.date.today():
        response = fulfillment_response(
            """Sorry, we don't have record for historical weather.""",
            parameters={'date_validated': False, 'date': None}, session=session_name
        )
    else:
        response = fulfillment_response(parameters={'date_validated': True}, session=session_name)

    print(response)
    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run(host='localhost', port=port, debug=True)
