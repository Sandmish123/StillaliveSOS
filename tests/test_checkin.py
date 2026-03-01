from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# test the auth first and update
def get_auth_headers(phone: str):
    otp_resp = client.post("/auth/request_otp",
                           json={"phone": phone})
    otp = otp_resp.json()["otp"]

    token_resp = client.post("auth/verify_otp",
                             json={"phone": phone, "otp": otp})
    token = token_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
