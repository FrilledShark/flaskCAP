from database import User
from passlib_context import pwd_context


if __name__ == "__main__":
    username = input("Username: ").lower()
    non_pass = input("Password: ")
    pass_hash = pwd_context.hash(non_pass)
    print(User.create(username=username, password=pass_hash))
