import requests, json

main_url = "http://127.0.0.1:5000"


def get_jwt(username, password):

    url = f'{main_url}/ccap/auth'

    rqst = requests.post(url, json=dict(username=username, password=password))
    try:
        return rqst.json()
    except json.JSONDecodeError:
        return rqst.status_code


def update_coin(coin, address, jwt):
    url = f'{main_url}/ccap/address'

    rqst = requests.post(url, json=dict(coin=coin, address=address), headers=dict(bearer=jwt))
    try:
        return rqst.json()
    except json.JSONDecodeError:
        return rqst.status_code, rqst.content


if __name__ == "__main__":
    username = "username"
    password = "qwerty"
    jwt = get_jwt(username, password)
    print(jwt)
    coin = "nano"
    address = "xrb_17h1imjes17gr8fantofykyztfe7g3ag1yqgp1qtjdhs3dfnwds5bzzp6u81"
    up_co = update_coin(coin, address, jwt["jwt"])
    print(up_co)
