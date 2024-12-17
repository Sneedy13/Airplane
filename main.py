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

@app.get("/flights/{flight_id}/bookings/", response_model=list[Booking])
def read_bookings_for_flight(flight_id: int):
    with Session(engine) as session:
        statement = select(Booking).where(Booking.flight_id == flight_id)
        results = session.exec(statement)
        return results.all()

@app.delete("/flights/{flight_id}", response_model=dict)
def delete_flight(flight_id: int):
    with Session(engine) as session:
        flight = session.get(Flight, flight_id)
        if flight is None:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        session.delete(flight)
        session.commit()
        return {"detail": "Flight deleted successfully"}
        
# Проверка запроса:
# curl -X PUT "http://127.0.0.1:8000/flights/1" -H "Content-Type: application/json" -d '{"status": "Delayed"}'
@app.patch("/flights/{flight_id}", response_model=Flight)
def partial_update_flight(flight_id: int, flight_update: Flight):
    with Session(engine) as session:
        flight = session.get(Flight, flight_id)
        if flight is None:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        flight_data = flight_update.dict(exclude_unset=True)
        for key, value in flight_data.items():
            setattr(flight, key, value)
        
        session.add(flight)
        session.commit()
        session.refresh(flight)
        return flight

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


# Проверка запроса:
# curl -X DELETE "http://127.0.0.1:8000/bookings/1"
@app.delete("/bookings/{booking_id}", response_model=dict)
def delete_booking(booking_id: int):
    with Session(engine) as session:
        booking = session.get(Booking, booking_id)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        session.delete(booking)
        session.commit()
        return {"detail": "Booking deleted successfully"}
