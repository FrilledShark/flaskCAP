import datetime
from base64 import b64encode
from os import urandom

from database import Domain
from passlib_context import pwd_context

if __name__ == "__main__":
    domain = input("Domain: ").lower()

    secret_pass = b64encode(urandom(36)).decode()
    print(f'{secret_pass}')
    print("Write down above password. Used for user creation for domain.")
    pass_hash = pwd_context.hash(secret_pass)
    print(Domain.create(domain_name=domain, password=pass_hash, date=datetime.datetime.now()))
