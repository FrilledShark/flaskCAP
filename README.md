# NanoAlias
CCAP implementation in Python Flask.

# Create database
The server uses sqlite, but can easily be configured for something else if needed. Run database.py to create the nesseary database and tables.

# Add user
In the test folder run user.py. Input username and password.
Note: It is possbile to use own database if structured like database.py, but the password has to hashed with argon2 to avoid plaintext password storage.

# Start server
Install requirements.txt and run the flask app (app_ccap) with your prefered configuration. 
  For inspiration see Flask website: http://flask.pocoo.org/docs/1.0/deploying/


