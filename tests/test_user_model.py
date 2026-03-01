from app.core.database import SessionLocal, engine, Base
from app.models.user import User


def test__create_user():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = User(phone="8273182366", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.phone == "8273182366"

    db.close()
