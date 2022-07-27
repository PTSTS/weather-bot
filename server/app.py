import json
from flask import Flask, request, make_response, jsonify, Response
import server.weather
from server.response import fulfillment_response
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


@app.route('/webhook', methods=['GET', 'POST'])
def hook():
    request_body = json.loads(request.data)
    print(request_body)
    return make_response(jsonify({
        'fulfillmentText': 'This is a response from webhook.'
    } ))


@app.route('/date', methods=['GET', 'POST'])
def check_date():
    request_body = json.loads(request.data)
    date_dict = request_body['sessionInfo']['parameters']['date']
    session_name = request_body['sessionInfo']['session']
    print(request_body['sessionInfo'])

    date = datetime.date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))
    current_date = datetime.date.today()

    if date - current_date > datetime.timedelta(days=13):
        response = fulfillment_response(
            """Sorry, we can only provide forecast for the next 14 days.""",
            parameters={'date_validated': False, 'date': None}, session=session_name
        )
    elif date < datetime.date(2010, 1, 1):
        response = fulfillment_response(
            """Sorry, we don't have record before Jan 1 2010.""",
            parameters={'date_validated': False, 'date': None}, session=session_name
        )
    else:
        response = fulfillment_response(parameters={'date_validated': True}, session=session_name)

    print(response)
    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run(host='localhost', port=port, debug=True)
