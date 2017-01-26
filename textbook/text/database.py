from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask.ext.login import UserMixin

from text import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    author = Column(Text)
    subject = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    
    owner_id = Column(Integer, ForeignKey('users.id'))
    
# User table for Flask-Login
# Inherits from UserMixin, which adds default methods

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))    
    # One-to-many relationship with posts
    books = relationship("Book", backref="owner")    


Base.metadata.create_all(engine)
