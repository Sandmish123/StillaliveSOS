from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError  # type: ignore
from uuid import UUID


SECRET_KEY = "super-secret-change-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# create access token
def create_access_token(
    *,
    subject: str,
    user_id: UUID,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    payload = {
        "sub": subject,  # phone
        "user_id": str(user_id),  # UUID → string
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# decode access token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
