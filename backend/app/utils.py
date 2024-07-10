from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hash the password using bcrypt
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Compare the hashed and plain password
    """
    return pwd_context.verify(plain_password, hashed_password)
