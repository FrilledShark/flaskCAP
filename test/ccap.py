import json

import requests

main_url = "https://cap.nanoalias.io"  # Remember to use https


def get_jwt(username, password):

    url = f'{main_url}/auth'

    rqst = requests.post(url, json=dict(username=username, password=password))
    try:
        return rqst.json()
    except json.JSONDecodeError:
        return rqst.status_code


def update_coin(coin, address, jwt):
    url = f'{main_url}/address'

    rqst = requests.post(url, json=dict(coin=coin, address=address), headers=dict(bearer=jwt))
    try:
        return rqst.json()
    except json.JSONDecodeError:
        return rqst.status_code, rqst.content


def create_user(secret, username, password):
    url = f'{main_url}/private/user'

    rqst = requests.post(url, json=dict(username=username, password=password), headers=dict(bearer=secret))
    try:
        return rqst.json()
    except json.JSONDecodeError:
        return rqst.status_code, rqst.content


if __name__ == "__main__":
    username = "frilledshark"
    password = "1QPYO0iNh"

    # secret = "EAT/cLspqKuZQVhRpWf5vF0jRYlI+PReKg=="
    #
    # print(create_user(secret, username, password))

    jwt = get_jwt(username, password)
    print(jwt)
    coin = "nano"
    address = "xrb_3ukjmojipeiam6wd54bqgr195r81wuyfk6c8nieixxx4hnwpa1x7z8qxcxu3"
    up_co = update_coin(coin, address, jwt["jwt"])
    print(up_co)
