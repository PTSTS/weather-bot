import json
from flask import Flask, request, make_response, jsonify, Response
import server.weather

app = Flask(__name__)


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
    return make_response(jsonify({
        'fulfillmentText': 'This is a response from webhook.'
    } ))


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
