# flaskCCAP server

[openCAP](https://github.com/opencap/protocol) implementation in Python Flask.

Note: flaskCAP breaks the protocol specs by allowing updates with POST /ccap/address for all aliases. Discussed in: https://github.com/opencap/protocol/issues/2. This breaks the Nano specific protocol.

This server allows multi domain redirection. This means it is possible to redirect domains to one server and letting the server handle the request. To setup the domains, run domain.py and configure tls/ssl certificates and redirect requests to the server with the domain passed in the host header.


# Setting up

Install requirements from requirement.txt. If the test folder wants to be used, install "requests" as well.

## Security

To secure the JWT tokens, a new secret key should be generated and input in config. Can be done by using os.urandom, but not required.

As per openCAP specs, it is also required to setup ssl certificates for the server, which flaskCCAP doesn't do.

## Create database

The server uses sqlite, but can easily be configured for something else if needed. Run database.py to create the nesseary database and tables.

## Add domain

Run test/domain.py and input the domain name. Write down the secret key.

## Add user

In the test folder run user.py. Input username and password.

Note: It is possible to use own database if structured like database.py, but the password has to hashed with argon2 to avoid plaintext password storage.


## Start server

Run the flask app with your preferred configuration.

Gunicorn + supervisor and nginx is an example setup. For more inspiration see Flask website: http://flask.pocoo.org/docs/1.0/deploying/

## Private Endpoints:

Private endpoints are used for creating users and getting auth keys associated with the domains.

### POST /private/user

Authorization: bearer {secret}

Creates a new user on domain.

| Parameters | Description | Required | Sample Value |
| ---------- | ----------- | -------- | ------------ |
| username | The username to create | Yes | "alice"
| password | The password of the username | Yes | "taRx64tZ"



