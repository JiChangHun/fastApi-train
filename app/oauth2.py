from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "j5g234kg321uki5g2k3u4g32k15jg23k4jh235iu234k15i1v442oip24jko3jkqf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt