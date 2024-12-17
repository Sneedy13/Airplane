# requests/requests.py
from sqlmodel import Session, select
from models.models import Airplane, Flight, Passenger, Booking, Staff

def get_all_flights(session: Session):
    statement = select(Flight)
    results = session.exec(statement)
    return results.all()

def get_passenger_by_id(session: Session, passenger_id: int):
    statement = select(Passenger).where(Passenger.id == passenger_id)
    result = session.exec(statement).one_or_none()
    return result

def get_bookings_for_passenger(session: Session, passenger_id: int):
    statement = select(Booking).where(Booking.passenger_id == passenger_id)
    results = session.exec(statement)
    return results.all()

def get_airplanes(session: Session):
    statement = select(Airplane)
    results = session.exec(statement)
    return results.all()