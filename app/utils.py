from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the password
def hash(password:str):
    return passwd_context.hash(password)

# Compare two hashed to validate
def verify(palain_password, hashed_password):
    return passwd_context.verify(palain_password, hashed_password)
