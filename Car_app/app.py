from fastapi import FastAPI, Depends
from cars_app.db import SessionLocal
from cars_app.models import User, Car
from sqlalchemy.orm import Session
from cars_app.shemas_pd import UserCheck, UserReg, CarReg, CarPrice
from fastapi.exceptions import HTTPException
from typing import List, Optional
import joblib

app = FastAPI()

@app.get('/')
def description():
    return "Hello, it's about Machine Learning"

@app.get('/project_info')
def description_company():
    return {
        "message": "Our company is engaged in determining the price of old cars "
                   "according to the following parameters fuel type: gas or diesel, "
                   "number of cylinders, number of doors, power(horsepower)"
            }

def get_db():
    with SessionLocal() as db:
        return db

@app.post("/user/add", response_model=UserReg)
def add_user(user: UserReg, db: Session = Depends(get_db)):
    user = User(name=user.name,
                surname=user.surname,
                location=user.location)
    db.add(user)
    db.commit()
    return user


@app.post("/car/add/{user_id}", response_model=CarReg)
def add_car(user_id, car_data: CarReg, db: Session = Depends(get_db)):
    if not bool(db.query(User.id).filter(User.id == user_id).first()):
        raise HTTPException(404, detail='User not found')

    if car_data.fuel_type.lower() not in ('gas', 'diesel'):
        raise HTTPException(400, detail="Invalid fuel type")

    new_car = Car(fuel_type=car_data.fuel_type,
                 num_of_cylinders=car_data.num_of_doors,
                 num_of_doors=car_data.num_of_doors,
                 engine_power=car_data.engine_power,
                 price=car_data.price,
                 user_id=user_id)
    db.add(new_car)
    db.commit()
    return new_car

@app.get('/user/cars/{user_id}', response_model=List[CarReg])
def get_car(user_id: int, db: Session = Depends(get_db)):
    if not bool(db.query(Car.id).filter(Car.user_id == user_id).first()):
        raise HTTPException(404, detail='User not found')

    return db.query(Car.fuel_type,
                   Car.num_of_cylinders,
                   Car.num_of_doors,
                   Car.engine_power,
                   Car.price).filter(Car.user_id==user_id).all()


@app.get("/user/all", response_model=List[UserCheck])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/car/prediction/")
def get_price(car: CarPrice):
    if car.fuel_type.lower() not in ('gas', 'diesel'):
        raise HTTPException(400, detail="Invalid fuel type")

    fuel_type = int(car.fuel_type.lower().replace('gas', '1').replace('diesel', '0'))
    num_of_cylinders = car.num_of_cylinders
    num_of_doors = car.num_of_doors
    engine_power = car.engine_power
    vector = [[fuel_type, num_of_cylinders,
               num_of_doors, engine_power]]
    model = joblib.load('cars_app/rf_model_total.pkl')
    price = model.predict(vector)
    return {f'Reccommended price: {int(price[0])}'}

@app.get("/car/update_price/{user_id}/{car_id}/{new_price}")
def update_price(user_id: int,
                 car_id: int,
                 new_price: int,
                 db: Session = Depends(get_db)):
    db.query(Car).filter(Car.id==car_id).filter(Car.user_id==user_id).update({Car.price: new_price},
                                                                                 synchronize_session = False)
    db.commit()
    return {f"Price update to {new_price}"}


