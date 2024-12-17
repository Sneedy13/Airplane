# populate_db.py
from sqlmodel import Session, create_engine
from models.models import Airplane, Flight, Passenger, Booking, Staff

DATABASE_URL = "sqlite:///aviacompany.db"  # Используем SQLite для простоты
engine = create_engine(DATABASE_URL)

def populate_database():
    with Session(engine) as session:
        airplane = Airplane(model="Boeing 737", registration_number="N12345", capacity=180, range=3000)
        flight = Flight(flight_number="AB123", departure_time="2024-12-17 10:00", arrival_time="2024-12-17 12:00", origin="NYC", destination="LAX", status="Scheduled")
        passenger = Passenger(first_name="John", last_name="Doe", passport_number="A12345678", contact_info="john.doe@example.com")
        booking = Booking(booking_number="BKG123", booking_date="2024-12-01", status="Confirmed", passenger_id=1, flight_id=1)
        staff = Staff(first_name="Jane", last_name="Smith", position="Pilot", qualifications="ATPL")

        session.add(airplane)
        session.add(flight)
        session.add(passenger)
        session.add(booking)
        session.add(staff)
        session.commit()

if __name__ == "__main__":
    populate_database()