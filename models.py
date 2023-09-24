from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func


engine = create_engine("postgresql://postgres:1375@127.0.0.1:5432/flask_hw")
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Advertisement(Base):
    __tablename__ = "list_of_ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article = Column(String, nullable=False)
    description = Column(String)
    create_date = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all()