from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id            = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone         = Column(String(20),  nullable=False)
    coffee_name   = Column(String(50),  nullable=False)
    size          = Column(String(20),  nullable=False)
    quantity      = Column(Integer,     nullable=False, default=1)
    price         = Column(Float,       nullable=False)
    booking_time  = Column(DateTime,    default=datetime.utcnow)
    pickup_time   = Column(String(20),  nullable=False)
    status        = Column(String(20),  nullable=False, default="pending")