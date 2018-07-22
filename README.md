# NanoAlias
[CCAP](https://github.com/lane-c-wagner/ccap) implementation in Python Flask.

Note: This breaks the CCAP specs by allowing updates with POST /ccap/address for all aliases. Discussed in: https://github.com/lane-c-wagner/ccap/issues/2. This breaks the Nano specefic protocol.

# Setting up
Install requirements from requirement.txt. If the test folder wants to be used, install "requests" as well.

## Security
To secure the JWT tokens, a new secret key should be generated and input in config. Can be done by using os.urandom, but not required.

As per CCAP specs, it is also required to setup ssl certificates for the server, which flaskCCAP doesn't do.

## Create database
The server uses sqlite, but can easily be configured for something else if needed. Run database.py to create the nesseary database and tables.


## Add user
In the test folder run user.py. Input username and password.

Note: It is possbile to use own database if structured like database.py, but the password has to hashed with argon2 to avoid plaintext password storage.


## Start server
Run the flask app (app_ccap) with your prefered configuration. 

Gunicorn + supervisor and nginx is an example setup. For more inspiration see Flask website: http://flask.pocoo.org/docs/1.0/deploying/

# Domain Control
It is possible to enable domain control in the config. This allows the server to handle multiple different domains at the same time. 

Note: The server does not handle forwarding the different domain requests, which has to be done seperately and the server doesn't handle ssl certificates for any domains.

## Private Endpoints:

### POST /ccap/private/user

Authorization: Bearer {jwt}

Creates a new user on domain.

| Parameters | Description | Required | Sample Value |
| ---------- | ----------- | -------- | ------------ |
| username | The username to create | Yes | "alice"
| username | The password of the username | Yes | "taRx64tZ"

### POST /ccap/private/auth

No Authorization (Public method)

Gets a new JWT for given domain. Lasts 5 minutes

| Parameters | Description | Required | Sample Value |
| ---------- | ----------- | -------- | ------------ |
| domain | The domain | Yes | "excample.com"
| secret | The secret of the domain | Yes | "0ZWVAhwGBxvRtTjFG1mPCuRCCFSdFLCo6c3xLz6ZYfKLuivO"


