import os
import requests
from fastapi import HTTPException

NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY")


def verify_phone_number(phone: str):
    url = "http://apilayer.net/api/validate"
    
    params = {
        "access_key": NUMVERIFY_API_KEY,
        "number": phone,
        "country_code": "IN",
        "format": 1
    }

    response = requests.get(url, params=params)
    data = response.json()
    print("datattatattatta",data)
    if not data.get("valid"):
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number"
        )

    if data.get("line_type") != "mobile":
        raise HTTPException(
            status_code=400,
            detail="Only mobile numbers allowed"
        )

    return True