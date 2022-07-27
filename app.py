from flask import Flask, request, make_response, jsonify
app = Flask(__name__)


@app.route('/webhook')
def hook():
    pass



if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)

