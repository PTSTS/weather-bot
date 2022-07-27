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
    location = ', '.join(location_list)
    print(request_body)
    day_weather = weather(location, date, api_key)
    if day_weather.location_found:
        response = fulfillment_response(
            f"""You aksed for the weather on {date.day}/{date.month}/{date.year} in the location 
{day_weather.location}. The lowest temperature is {day_weather.low_temp} C, the highest temperature is 
{day_weather.high_temp}. Is this the right location you are looking for?""",
            parameters={'location_validated': True}, session=session_name
        )
        


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
            """Sorry, we can only provide forecast for the next 14 days.""",
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
