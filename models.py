# models/models.py
from sqlmodel import SQLModel, Field

class Airplane(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    model: str
    registration_number: str
    capacity: int
    range: float

class Flight(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    flight_number: str
    departure_time: str
    arrival_time: str
    origin: str
    destination: str
    status: str

class Passenger(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    passport_number: str
    contact_info: str

class Booking(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    booking_number: str
    booking_date: str
    status: str
    passenger_id: int = Field(foreign_key="passenger.id")
    flight_id: int = Field(foreign_key="flight.id")

class Staff(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    position: str
    qualifications: str