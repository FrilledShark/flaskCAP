import json
import os
from datetime import datetime, timedelta

import jwt
from flask import Flask, abort, jsonify, request
from peewee import IntegrityError, PeeweeException

from database import Coin, Domain, User
from passlib_context import pwd_context

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)


app = Flask(__name__)


jwt_secret = config["secret"]
dt_format = "%Y-%m-%d %H:%M:%S"

# if domain control:
if config.get("domain_control"):
    def update():
        rqst_domain = request.headers['Host'].lower()
        jwt_token = request.headers['bearer']
        req_coin = request.json["coin"]
        req_address = request.json["address"]
        try:
            jwt_decoded = jwt.decode(jwt_token, key=jwt_secret)
            username = jwt_decoded["u"]
            dt_jwt = datetime.strptime(jwt_decoded["d"], dt_format)
            if dt_jwt > datetime.now() - timedelta(minutes=5):
                user = User.get(User.username == username and User.domain.domain_name == rqst_domain)
                coin_instance, created = Coin.get_or_create(user=user, coin=req_coin)
                coin_instance.address = req_address
                coin_instance.save()
                return jsonify(success=True)
            else:
                abort(401)
        except jwt.InvalidSignatureError:
            abort(401)


    def address(username, coin):
        rqst_domain = request.headers['Host'].lower()
        try:
            # cAsE iNSnSeTivE username and coin.
            user = User.get(User.username == username.lower() and User.domain.domain_name == rqst_domain)
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


    def auth():
        rqst_domain = request.headers['Host'].lower()
        username = request.json['username'].lower()
        password = request.json['password']
        try:
            user = User.get(User.username == username and User.domain.domain_name == rqst_domain)
            if pwd_context.verify(password, user.password):
                encoded = jwt.encode({'u': username, 'd': datetime.now().strftime(dt_format)}, key=jwt_secret)
                return jsonify(jwt=encoded.decode())
            else:  # Wrong password
                abort(404)  # Do not tell it is wrong password
        except (PeeweeException, User.DoesNotExist):
            abort(404)


    #
    # Not CCAP, but domain control
    #

    def private_user():
        jwt_token = request.headers['bearer']
        username = request.json["username"]
        password = request.json["password"]
        try:
            jwt_decoded = jwt.decode(jwt_token, key=jwt_secret)
            domain_name = jwt_decoded["u"]
            dt_jwt = datetime.strptime(jwt_decoded["d"], dt_format)
            if dt_jwt > datetime.now() - timedelta(minutes=5):
                domain = Domain.get(Domain.domain_name == domain_name)
                User.create(username=username, password=pwd_context.hash(password), domain=domain)
                return jsonify(success=True)
            else:
                abort(401)
        except jwt.InvalidSignatureError:
            abort(401)
        except IntegrityError:
            abort(409)


    def private_auth():
        domain = request.json["domain"]
        secret = request.json['secret']
        try:
            domain = Domain.get(Domain.domain_name == domain)
            if pwd_context.verify(secret, domain.password):
                encoded = jwt.encode({'u': domain.domain_name, 'd': datetime.now().strftime(dt_format)}, key=jwt_secret)
                return jsonify(jwt=encoded.decode())
            else:  # Wrong password
                abort(404)
        except (PeeweeException, User.DoesNotExist):
            abort(404)


else:
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


    def auth():
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


@app.route('/ccap/address', methods=['POST'])
def flask_update():
    return update()


@app.route('/ccap/address/<username>/<coin>', methods=['GET'])
def flask_address(username, coin):
    return address(username, coin)


@app.route('/ccap/auth', methods=['POST'])
def flask_auth():
    return auth()


if config.get("domain_control"):
    # Not CCAP, but domain control

    @app.route('/ccap/private/user', methods=['POST'])
    def flask_private_user():
        return private_user()


    @app.route('/ccap/auth/user', methods=['POST'])
    def flask_private_auth():
        return private_auth()

if __name__ == "__main__":
    app.run()
