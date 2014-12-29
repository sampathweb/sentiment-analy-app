from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from app import Base


class Dataset(Base):
    '''Table to hold listing of uploaded datasets'''
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    source_file = Column(String(100), nullable=False)
    train_file = Column(String(100), nullable=True)
    test_file = Column(String(100), nullable=True)
    protected = Column(Boolean, default=False)
    test_score = Column(Float(precision=2))
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
