from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    bid_id = Column(Integer, ForeignKey("bid.id"), nullable = False)
    

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    item = relationship("Item", backref = "user")
    bid = relationship("Bid", backref = "user")
    
    

class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    item = relationship("Item", backref = "bid")

def reset_db():
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

def main():
    
    reset_db()
    
    Reed = User(username='reed', password='reed')
    Matt = User(username='matt', password='matt')
    Griff = User(username='griff', password='griff')
    
    baseball = Item(name='Baseball', description='Legit Baseball', user=Reed)
    Matt_bid = Bid(price=10000.00, item=baseball, user=Matt)
    Griff_bid = Bid(price=10000.99, item=baseball, user=Griff)
    
    session.add_all([Reed, Matt, Griff, baseball, Matt_bid, Griff_bid])
    session.commit()
    
    row = session.query(User.username, Item.name).join(Bid, Item).filter(Item.name == "Baseball").order_by(Bid.price).all()
    highest_bidder = row[-1].username
    print(highest_bidder)

if __name__ == "__main__":
    main()




