from fastapi import FastAPI
from app.db.database import engine
from app.db.database import engine
from app.models.base import Base
from app.models import user
from app.db.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session


app = FastAPI(title="Sales SaaS API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "API running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def test_db():
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        return {"db": "connected", "result": 1}
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    new_user = user.User(email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
