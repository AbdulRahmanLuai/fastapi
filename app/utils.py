import bcrypt  # ensures the C backend is loaded
from passlib.context import CryptContext

from passlib.hash import bcrypt
print("HELLO")
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    )



def hash(password: str):
    return pwd_context.hash(password)

def verify(given_password, actual_password):
    return pwd_context.verify(given_password, actual_password)
    