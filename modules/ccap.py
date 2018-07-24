import json
import os
from datetime import datetime, timedelta

import jwt
from flask import abort, jsonify
from peewee import IntegrityError, PeeweeException

from .database import Coin, Domain, User
from .passlib_context import pwd_context

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../config.json')
with open(filename, 'r') as file:
    config = json.load(file)

jwt_secret = config["secret"]
dt_format = "%Y-%m-%d %H:%M:%S"


def RESTupdate(request):
    rqst_domain = request.headers['Host'].lower()
    jwt_token = request.headers['bearer']
    req_coin = request.json["coin"]
    req_address = request.json["address"]
    try:
        jwt_decoded = jwt.decode(jwt_token, key=jwt_secret)
        username = jwt_decoded["u"]
        dt_jwt = datetime.strptime(jwt_decoded["d"], dt_format)
        if dt_jwt > datetime.now() - timedelta(minutes=5):
            user = User.select().join(Domain).where(User.username == username and Domain.domain == rqst_domain).get()
            coin_instance, created = Coin.get_or_create(user=user, coin=req_coin)
            coin_instance.address = req_address
            coin_instance.save()
            return jsonify(success=True)
        else:
            abort(401)
    except jwt.InvalidSignatureError:
        abort(401)


def RESTaddress(request, username, coin):
    rqst_domain = request.headers['Host'].lower()
    try:
        # cAsE iNSnSeTivE username and coin.
        user = User.select().join(Domain).where(
                User.username == username.lower() and Domain.domain == rqst_domain).get()
        address = ""
        for coin_instance in user.coins:
            if coin_instance.coin == coin.lower():
                address = coin_instance.address
                break
        if address:
            return jsonify(address=address)
        else:
            abort(404)
    except (PeeweeException, User.DoesNotExist):
        abort(404)


def RESTauth(request):
    rqst_domain = request.headers['Host'].lower()
    username = request.json['username'].lower()
    password = request.json['password']
    try:
        user = User.select().join(Domain).where(User.username == username and Domain.domain == rqst_domain).get()
        if pwd_context.verify(password, user.password):
            encoded = jwt.encode({'u': username, 'd': datetime.now().strftime(dt_format)}, key=jwt_secret)
            return jsonify(jwt=encoded.decode())
        else:  # Wrong password
            abort(401)
    except (PeeweeException, User.DoesNotExist):
        abort(404)


#
# Not CCAP, but domain control
#

def private_user(request):
    secret = request.headers['bearer']
    domain_name = request.headers["Host"]
    username = request.json["username"]
    password = request.json["password"]
    try:
        domain = Domain.get(Domain.domain == domain_name)
        if pwd_context.verify(secret, domain.password):
            User.create(username=username, password=pwd_context.hash(password), domain=domain)
            return jsonify(success=True)
        else:
            abort(401)
    except IntegrityError:
        abort(409)
