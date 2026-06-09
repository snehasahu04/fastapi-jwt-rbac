from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

# CONFIG

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Use ONE consistent hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PASSWORD FUNCTIONS

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# CREATE JWT TOKEN

def create_token(data: dict, expires_minutes: int = 30):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



# DECODE JWT TOKEN (REQUIRED FOR RBAC)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return {
            "email": payload.get("sub"),
            "role": payload.get("role")
        }

    except Exception:
        return None