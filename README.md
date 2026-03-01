# 🆘 StillAlive-SOS — Backend

![Backend CI](https://github.com/aditya-kumar96/stillalive-sos-backend/actions/workflows/ci.yml/badge.svg)

A **safety check-in backend system** built with **FastAPI**.  
Users periodically confirm they are safe. If a check-in is missed, the system is designed to trigger an **SOS workflow** to notify emergency contacts.

> **Core idea**  
> _“If I don’t confirm I’m okay, my system should act for me.”_

---

## 📌 Table of Contents

- [Why StillAlive-SOS?](#-why-stillalive-sos)
- [Current Status](#-current-status)
- [Architecture Overview](#-architecture-overview)
- [Authentication Design](#-authentication-design)
- [Database Design](#-database-design)
- [Testing & CI](#-testing--ci)
- [Getting Started](#-getting-started)
- [Roadmap](#-roadmap)
- [Design Philosophy](#-design-philosophy)

---

## 🧠 Why StillAlive-SOS?

Many people:
- Live alone
- Travel solo
- Work night shifts
- Have medical conditions

StillAlive-SOS works like a **digital dead-man switch**:

1. User checks in periodically  
2. If a check-in is missed → system escalates automatically  
3. Emergency contacts are notified (planned)

This repository contains the **backend foundation** for that system.

---

## 🏗️ Current Status

### ✅ Backend Foundation
- FastAPI application
- Clean, scalable project structure
- GitHub Actions CI pipeline
- Linting and testing enforced

### ✅ Database Layer
- SQLAlchemy ORM
- SQLite for development & CI
- PostgreSQL-ready architecture
- UUID-based primary keys

### ✅ User Identity
- Minimal `User` model:
  - `id` (server-generated UUID)
  - `phone`
  - `name`
- Identity kept intentionally small and stable

### ✅ Authentication (Phone-based)
- OTP-based login flow (**mocked for learning**)
- JWT access tokens
- Secure token validation
- Dependency-based authentication

### ✅ Protected APIs
- JWT-protected routes
- `get_current_user` dependency
- Secure access control

### ✅ Emergency Contacts (SOS Foundation)
- Emergency contacts linked to authenticated users
- One user → multiple contacts
- Ownership enforced at backend level
- Fully tested endpoints

---

## 🧱 Architecture Overview

```text
app/
├── main.py                  # FastAPI app entry point
│
├── core/
│   ├── database.py          # DB engine, session, Base
│   ├── security.py          # JWT creation & decoding
│   └── dependencies.py     # Auth dependencies
│
├── models/
│   ├── user.py
│   ├── otp.py
│   └── emergency_contact.py
│
├── schemas/
│   ├── user.py
│   ├── auth.py
│   └── emergency_contact.py
│
├── routers/
│   ├── auth.py
│   ├── user.py
│   └── emergency_contact.py
│
tests/
│   ├── test_main.py
│   ├── test_user_api.py
│   ├── test_auth_protected.py
│   └── test_emergency_contacts.py
│
.github/
└── workflows/
    └── ci.yml
```


---

## 🔐 Authentication Design

- Phone number is the **primary identity**
- OTP is:
  - Temporary
  - Time-bound
  - Stored separately from users
- JWT tokens contain:
  - User UUID (`sub`)
  - Expiry timestamp
- No passwords stored

⚠️ **Note:**  
OTP is currently returned in API responses **only for learning purposes**.  
In production, OTP would be delivered via SMS and never exposed.

---

## 🗄️ Database Design

### Users
- Stable identity
- Minimal personal data
- UUID-based primary key

### Emergency Contacts
- Linked via `user_id`
- User-owned data
- Multiple contacts per user

### OTP Requests
- Temporary
- Expiring
- Separate from user identity

This separation ensures:
- Better security
- Easier scaling
- Clean ownership boundaries

---

## 🧪 Testing & CI

- GitHub Actions used for CI
- Runs on every `push` and `pull_request`
- Includes:
  - Dependency installation
  - Linting (`flake8`)
  - Unit & API tests (`pytest`)
- No external database required in CI

CI is treated as a **quality gate**, not a formality.

---

## ▶️ Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/stillalive-sos-backend.git
cd stillalive-sos-backend


2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the server
uvicorn app.main:app --reload

4️⃣ Open API documentation
http://127.0.0.1:8000/docs

```

## 🔮 Roadmap
🚧 Planned Features
- Check-in system
- Missed check-in detection
- SOS event creation
- Location capture
- Notification triggers (SMS / Push)
- React Native frontend
- Real OTP service
- PostgreSQL in production
- Deployment (CD)

### 🎯 Design Philosophy
- Backend-first, contract-driven development
- Minimal identity, layered data models
- Security before convenience
- CI as a first-class citizen
- Built for learning and real-world use

### 👨‍💻 Author
- Aditya Kumar Built it as a learning-focused yet production-minded project to deeply understand:
- Backend engineering
- CI/CD
- Authentication design
- System architecture

