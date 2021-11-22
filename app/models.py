from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import settings

user, password, server, db = (
    settings.POSTGRES_USER,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_SERVER,
    settings.POSTGRES_DB,
)

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{server}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    state_abbreviation = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    ruca = Column(Float, nullable=False)
    procedure_code = Column(String, nullable=False)
