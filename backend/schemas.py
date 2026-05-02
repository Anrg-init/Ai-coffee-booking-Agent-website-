from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookingCreate(BaseModel):
    customer_name: str   = Field(..., min_length=1, max_length=100)
    phone:         str   = Field(..., min_length=1, max_length=20)
    coffee_name:   str   = Field(..., pattern="^(Espresso|Cappuccino|Latte|Americano|Mocha|Cold Coffee)$")
    size:          str   = Field(..., pattern="^(Small|Regular|Medium|Large|Extra Large)$")
    quantity:      int   = Field(..., ge=1, le=10)
    price:         float = Field(..., gt=0)
    pickup_time:   str   = Field(..., min_length=1)


class BookingResponse(BaseModel):
    id:            int
    customer_name: str
    phone:         str
    coffee_name:   str
    size:          str
    quantity:      int
    price:         float
    booking_time:  datetime
    pickup_time:   str
    status:        str

    class Config:
        from_attributes = True


class BookingStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|completed)$")


class ChatMessage(BaseModel):
    message:    str
    session_id: str = Field(..., min_length=1)