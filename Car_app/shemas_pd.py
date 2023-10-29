from typing import Union, Optional
from pydantic import BaseModel, Field


class UserCheck(BaseModel):
    id: int
    name: str
    surname: str
    location: str

    class Config:
        orm_mode = True

class UserReg(BaseModel):
    location: str
    name: str
    surname: str
    class Config:
        orm_mode = True

class CarReg(BaseModel):
    fuel_type: str
    num_of_cylinders: int
    num_of_doors: int
    engine_power: int
    price: int
    class Config:
        orm_mode = True

class CarPrice(BaseModel):
    fuel_type: str
    num_of_cylinders: int
    num_of_doors: int
    engine_power: int
    class Config:
        orm_mode = True
