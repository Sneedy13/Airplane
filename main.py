# main.py
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, create_engine, SQLModel
from models.models import Airplane, Flight, Passenger, Booking, Staff
from requests.requests import get_all_flights, get_passenger_by_id, get_bookings_for_passenger, get_airplanes

DATABASE_URL = "sqlite:///aviacompany.db"
engine = create_engine(DATABASE_URL)
app = FastAPI()


# Создание таблиц
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Проверка запроса:
# curl -X GET "http://127.0.0.1:8000/flights/"
@app.get("/flights/", response_model=list[Flight])
def read_flights():
    with Session(engine) as session:
        flights = get_all_flights(session)
        return flights

# Проверка запроса:
# curl -X GET "http://127.0.0.1:8000/passengers/1"
@app.get("/passengers/{passenger_id}", response_model=Passenger)
def read_passenger(passenger_id: int):
    with Session(engine) as session:
        passenger = get_passenger_by_id(session, passenger_id)
        if passenger is None:
            raise HTTPException(status_code=404, detail="Passenger not found")
        return passenger

# Проверка запроса:
# curl -X GET "http://127.0.0.1:8000/passengers/1/bookings/"
@app.get("/passengers/{passenger_id}/bookings/", response_model=list[Booking])
def read_passenger_bookings(passenger_id: int):
    with Session(engine) as session:
        bookings = get_bookings_for_passenger(session, passenger_id)
        return bookings

# Проверка запроса:
# curl -X GET "http://127.0.0.1:8000/airplanes/"
@app.get("/airplanes/", response_model=list[Airplane])
def read_airplanes():
    with Session(engine) as session:
        airplanes = get_airplanes(session)
        return airplanes