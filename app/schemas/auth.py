from pydantic import BaseModel


class OTPRequestIn(BaseModel):
    phone: str


class OTPVerifyIn(BaseModel):
    phone: str
    otp: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
