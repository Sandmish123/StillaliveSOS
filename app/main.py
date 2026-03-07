import os

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
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
security = HTTPBasic()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
app = FastAPI(
    title="StillAlive-SOS Backend",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
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



PUBLIC_PATHS = [
    "/health_check",
    "/media",
    "/pattern",
    "/legal"
]

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise RuntimeError("ADMIN_USERNAME or ADMIN_PASSWORD not set")

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)

    return True

@app.middleware("http")
async def restrict_access(request: Request, call_next):

    path = request.url.path

    # Allow homepage
    if path == "/":
        return await call_next(request)

    # Allow public routes
    if any(path.startswith(p) for p in PUBLIC_PATHS):
        return await call_next(request)

    # Check Basic Auth
    auth = request.headers.get("authorization")

    if not auth or not auth.startswith("Basic "):
        return JSONResponse(
            status_code=401,
            headers={"WWW-Authenticate": "Basic realm='StillAliveSOS'"},
            content={"message": "Authentication required"}
        )

    import base64

    try:
        encoded = auth.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":")

        if not (
            secrets.compare_digest(username, ADMIN_USERNAME) and
            secrets.compare_digest(password, ADMIN_PASSWORD)
        ):
            raise ValueError

    except Exception:
        return JSONResponse(
            status_code=401,
            headers={"WWW-Authenticate": "Basic realm='StillAliveSOS'"},
            content={"message": "Invalid credentials"}
        )

    return await call_next(request)

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