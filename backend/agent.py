import os
import json
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

COFFEES = ["Espresso", "Cappuccino", "Latte", "Americano", "Mocha", "Cold Coffee"]
SIZES   = ["Small", "Regular", "Medium", "Large", "Extra Large"]
TIMES   = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "2:00 PM", "4:00 PM", "6:00 PM"]

PRICES = {
    "Espresso":    {"Small":3.0,"Regular":3.5,"Medium":4.0,"Large":4.5,"Extra Large":5.0},
    "Cappuccino":  {"Small":3.5,"Regular":4.0,"Medium":4.5,"Large":5.0,"Extra Large":5.5},
    "Latte":       {"Small":4.0,"Regular":4.5,"Medium":5.0,"Large":5.5,"Extra Large":6.0},
    "Americano":   {"Small":3.0,"Regular":3.5,"Medium":4.0,"Large":4.5,"Extra Large":5.0},
    "Mocha":       {"Small":4.5,"Regular":5.0,"Medium":5.5,"Large":6.0,"Extra Large":6.5},
    "Cold Coffee": {"Small":4.0,"Regular":4.5,"Medium":5.0,"Large":5.5,"Extra Large":6.0},
}

SYSTEM = f"""You are a coffee booking assistant. Collect these 6 fields through conversation:
customer_name, phone, coffee_name, size, quantity, pickup_time.

Valid coffees: {COFFEES}
Valid sizes: {SIZES}
Valid times: {TIMES}
Valid quantity: 1 to 5

- Be friendly. Extract any info user already gave. Only ask for missing fields.
- When all 6 fields are collected, show a summary and ask to confirm.
- After user confirms, set confirmed=true.

Always reply with ONLY this JSON (no extra text):
{{"message":"your reply here","collected":{{"customer_name":null,"phone":null,"coffee_name":null,"size":null,"quantity":null,"pickup_time":null}},"confirmed":false}}"""

sessions = {}

def get_session(sid):
    if sid not in sessions:
        sessions[sid] = {"history": [], "collected": {}, "confirmed": False}
    return sessions[sid]

def reset_session(sid):
    sessions.pop(sid, None)

async def process_message(session_id: str, user_message: str, db) -> str:
    from backend.models import Booking
    from datetime import datetime

    session = get_session(session_id)
    session["history"].append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM}] + session["history"][-8:]

    for attempt in range(3):
        try:
            response = await client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=250,
                temperature=0.3,
            )
            break
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                await asyncio.sleep(7)
                continue
            return "I'm a bit busy right now. Please send your message again! ☕"

    raw = response.choices[0].message.content.strip()

    # parse JSON
    try:
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        data = json.loads(raw)
    except Exception:
        session["history"].append({"role": "assistant", "content": raw})
        return raw

    reply = data.get("message", "Sorry, something went wrong.")
    session["history"].append({"role": "assistant", "content": raw})
    session["collected"] = data.get("collected", session["collected"])
    session["confirmed"] = data.get("confirmed", False)

    if session["confirmed"]:
        c = session["collected"]
        coffee_name = c.get("coffee_name") or "Espresso"
        size        = c.get("size") or "Regular"
        quantity    = int(c.get("quantity") or 1)
        unit_price  = PRICES.get(coffee_name, {}).get(size, 4.0)
        total_price = round(unit_price * quantity, 2)

        booking = Booking(
            customer_name=c.get("customer_name", "Guest"),
            phone=c.get("phone") or "N/A",
            coffee_name=coffee_name,
            size=size,
            quantity=quantity,
            price=total_price,
            pickup_time=c.get("pickup_time", ""),
            booking_time=datetime.utcnow(),
            status="pending",
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        reset_session(session_id)

    return reply