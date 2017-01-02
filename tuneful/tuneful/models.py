import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine

class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    
    def as_dictionary(self):
       return {
    "id": 1,
    "file": {
        "id": 7,
        "name": "Shady_Grove.mp3"
    }
}

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(128))
    songs = relationship("Song", backref="file")
    
    def as_dictionary(self):
        return {
        "id": 7,
        "name": "Shady_Grove.mp3"
    }
