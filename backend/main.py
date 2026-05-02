from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend import models, schemas
from backend.database import engine, get_db
from backend.agent import process_message

# Auto-create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brûlée Coffee API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ════════════════════════════════
#  BOOKINGS
# ════════════════════════════════

@app.post("/bookings", response_model=schemas.BookingResponse, status_code=201)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    new_booking = models.Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@app.get("/bookings", response_model=List[schemas.BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).order_by(models.Booking.booking_time.desc()).all()


@app.patch("/bookings/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(booking_id: int, payload: schemas.BookingStatusUpdate, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = payload.status
    db.commit()
    db.refresh(booking)
    return booking


@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()


# ════════════════════════════════
#  CHAT
# ════════════════════════════════

@app.post("/chat")
async def chat(msg: schemas.ChatMessage, db: Session = Depends(get_db)):
    reply = await process_message(
        session_id=msg.session_id,
        user_message=msg.message,
        db=db,
    )
    return {"reply": reply}