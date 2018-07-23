from database import Domain, User
from passlib_context import pwd_context

main_url = "127.0.0.1:5000"

if __name__ == "__main__":
    username = input("Username: ").lower()
    non_pass = input("Password: ")
    domain = Domain.get(Domain.domain == input("Domain: "))
    pass_hash = pwd_context.hash(non_pass)
    print(User.create(username=username, password=pass_hash, domain=domain))
