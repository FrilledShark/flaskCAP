import json
import os

from flask import Flask, request

from modules.ccap import RESTaddress, RESTauth, RESTupdate, private_user

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)

app = Flask(__name__)


@app.route('/ccap/address', methods=['POST'])
def flask_update():
    return RESTupdate(request)


@app.route('/ccap/address/<username>/<coin>', methods=['GET'])
def flask_address(username, coin):
    return RESTaddress(request, username, coin)


@app.route('/ccap/auth', methods=['POST'])
def flask_auth():
    return RESTauth(request)


@app.route('/ccap/private/user', methods=['POST'])
def flask_private_user():
    return private_user(request)


if __name__ == "__main__":
    app.run()
