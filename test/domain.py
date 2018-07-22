import datetime
import string
from random import SystemRandom

from database import Domain
from passlib_context import pwd_context

if __name__ == "__main__":
    domain = input("Domain: ").lower()

    secret_pass = "".join(SystemRandom().choice(string.digits + string.ascii_letters + string.punctuation)
                          for _ in range(36))
    print(f'{secret_pass}')
    print("Write down above password. Used for user creation for domain.")
    pass_hash = pwd_context.hash(secret_pass)
    print(Domain.create(domain_name=domain, password=pass_hash, date=datetime.datetime.now()))
