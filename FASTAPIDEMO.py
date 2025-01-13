Installing the Dependencies
pip install fastapi sqlalchemy alembic sqlite3

Defining the DB URL
DATABASE_URL = "sqlite:///./test.db"

Setup the engine.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Create a Model:

from sqlalchemy import Column, Integer, String

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

initialize the alembic
sqlalchemy.url = sqlite:///./test.db

Migrations:
alembic revision --autogenerate -m "Initial migration"

alembic upgrade head

DB Sessions
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.orm import Session
from . import models, schemas

def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(name=cat.name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


from pydantic import BaseModel
from typing import Optional

class CatUpdate(BaseModel):
    name: Optional[str] = None

from sqlalchemy.orm import Session
from . import models, schemas

def update_cat(db: Session, cat_id: int, cat_update: schemas.CatUpdate):
    db_cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if db_cat is None:
        return None
    if cat_update.name is not None:
        db_cat.name = cat_update.name
    db.commit()
    db.refresh(db_cat)
    return db_cat


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas

app = FastAPI()

@app.put("/cats/{cat_id}", response_model=schemas.Cat)
def update_cat(cat_id: int, cat_update: schemas.CatUpdate, db: Session = Depends(get_db)):
    db_cat = crud.update_cat(db=db, cat_id=cat_id, cat_update=cat_update)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat



