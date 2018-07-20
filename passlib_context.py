from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    # Automatically mark all but first hash in list as deprecated.
    deprecated="auto",
    )
