from flask import Flask, request, jsonify, abort
from peewee import PeeweeException
from database import User, Coin
from passlib_context import pwd_context
from datetime import datetime, timedelta
import jwt

import os, json  # Reading config file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)


app = Flask(__name__)


jwt_secret = config["secret"]
dt_format = "%Y-%m-%d %H:%M:%S"


@app.route('/ccap/address', methods=['POST'])
def update():
    jwt_token = request.headers['bearer']
    req_coin = request.json["coin"]
    req_address = request.json["address"]
    try:
        jwt_decoded = jwt.decode(jwt_token, key=jwt_secret)
        username = jwt_decoded["u"]
        dt_jwt = datetime.strptime(jwt_decoded["d"], dt_format)
        if dt_jwt > datetime.now() - timedelta(minutes=5):
            user = User.get(User.username == username)
            coin_instance, created = Coin.get_or_create(user=user, coin=req_coin)
            coin_instance.address = req_address
            coin_instance.save()
            return jsonify(success=True)
        else:
            abort(401)
    except jwt.InvalidSignatureError:
        abort(401)


@app.route('/ccap/address/<username>/<coin>', methods=['GET'])
def address(username, coin):
    try:
        # cAsE iNSnSeTivE username and coin.
        user = User.get(User.username == username.lower())
        address = ""
        for coin_instance in user.coins:
            if coin_instance.coin == coin.lower():
                address = coin_instance.address
                break
        if address:
            return jsonify(address=address)
        else:
            abort(404)
    except PeeweeException:
        abort(404)


@app.route('/ccap/auth', methods=['POST'])
def auth():
    print(request.json)
    username = request.json['username'].lower()
    password = request.json['password']
    try:
        user = User.get(User.username == username)
        if pwd_context.verify(password, user.password):
            encoded = jwt.encode({'u': username, 'd': datetime.now().strftime(dt_format)}, key=jwt_secret)
            return jsonify(jwt=encoded.decode())
        else:  # Wrong password
            abort(401)
    except (PeeweeException, User.DoesNotExist):
        abort(404)


if __name__ == "__main__":
    app.run()
