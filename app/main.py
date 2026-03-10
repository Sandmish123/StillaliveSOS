import os
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from app.core import config  # noqa: F401
from app.core.database import Base, engine
from app.models.user import User  # noqa
from app.models.checkin import Check_In  # noqa
from app.models.emergency_contact import EmergencyContacts  # noqa
from app.models.otp import OTPRequest  # noqa
from app.models.safety_setting import SafetySetting  # noqa
from app.models.sos_event import SOSEvent  # noqa
from app.models.location import UserLocation  # noqa
from app.routers import location
from app.routers import legal
from app.routers import user, auth, emergency_contact, checkin, safety_setting, admin,sos
from fastapi.staticfiles import StaticFiles
from app.core.logging_config import setup_logging


app = FastAPI(title="StillAlive-SOS Backend")
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(emergency_contact.router)
app.include_router(checkin.router)
app.include_router(safety_setting.router)
app.include_router(admin.router)
app.include_router(location.router)
app.include_router(sos.router)
app.include_router(legal.router, prefix="/legal", tags=["Legal"])
setup_logging()

# -----------------------------
# Startup Event (Table Creation)
# -----------------------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# -----------------------------
# First Page
# -----------------------------
templates = Jinja2Templates(directory="app/templates")
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health_check")
def health_check():
    return {"status": "alive"}


# -----------------------------
# Static Files
# -----------------------------
app.mount("/media", StaticFiles(directory="app/media"), name="media")


# -----------------------------
# Dynamic Pattern URL (No Hardcoded localhost)
# -----------------------------
@app.get("/pattern/{name}")
def get_pattern(name: str, request: Request):
    base_url = str(request.base_url).rstrip("/")

    return {
        "partId": "slide",
        "type": "pattern",
        "url": f"{base_url}/media/{name}.png"
    }

# -----------------------------
# logs
# -----------------------------

@app.get("/logs")
def get_logs():
    log_file = "logs/app.log"

    if not os.path.exists(log_file):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(log_file, "r") as f:
        logs = f.readlines()

    return {"logs": logs[-100:]}  # return last 100 lines