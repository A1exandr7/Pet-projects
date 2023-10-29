from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from cars_app.db import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    location = Column(String)


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    fuel_type = Column(String)
    num_of_cylinders = Column(Integer)
    num_of_doors = Column(Integer)
    engine_power = Column(Integer)
    price = Column(Float)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

