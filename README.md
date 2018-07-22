# NanoAlias
CCAP implementation in Python Flask.

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
Install requirements.txt and run the flask app (app_ccap) with your prefered configuration.

  For inspiration see Flask website: http://flask.pocoo.org/docs/1.0/deploying/

# Domain Control
It is possible to enable domain control in the config. This allows the server to handle multiple different domains at the same time. 

Note: The server does not handle forwarding the different domain requests, which has to be done seperately and the server doesn't handle ssl certificates for other domains.
