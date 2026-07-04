#import engine
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, echo=settings.app_debug)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#get_db session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
