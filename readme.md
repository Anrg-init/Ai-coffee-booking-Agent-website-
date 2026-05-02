# Brûlée Coffee ☕

AI-powered coffee booking website with a conversational agent and manual booking form.

![alt text](<Screenshot from 2026-05-02 16-07-12.png>) 

![alt text](<Screenshot from 2026-05-02 16-07-31.png>) 

![alt text](<Screenshot from 2026-05-02 16-07-51.png>)

---

## Stack

- **Frontend** — HTML, CSS, Bootstrap
- **Backend** — FastAPI
- **Database** — PostgreSQL
- **AI Agent** — Groq API (Llama 3.1 8B)

---

## Project Structure

```
coffee-crud/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI routes
│   ├── models.py        # Database model
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # PostgreSQL connection
│   ├── agent.py         # AI booking agent
│   ├── requirements.txt
│   ├── .env             # API keys 
│   └── .gitignore
└── frontend/
    ├── index.html       # Main café site + AI chat
    └── admin.html       # Manual booking + all bookings
```

---

## Setup

### 1. Clone & create virtual environment
```bash
git clone <your-repo>
cd coffee-crud
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Create PostgreSQL database
```bash
psql -U postgres
```
```sql
CREATE DATABASE coffee_db;
GRANT ALL ON SCHEMA public TO postgres;
\q
```

### 4. Configure `.env`
```bash
# backend/.env
GROQ_API_KEY=your_groq_key_here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/coffee_db
```
Get a free Groq key at → https://console.groq.com

### 5. Update `database.py`
```python
DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/coffee_db"
```

### 6. Run the backend
```bash
cd coffee-crud
uvicorn backend.main:app --reload
```
API runs at → http://localhost:8000
API docs at → http://localhost:8000/docs

### 7. Open the frontend
Open `frontend/index.html` directly in your browser.

---

## Features

### index.html — Customer Site
- Landing page with menu loaded live from DB
- **Book via AI Agent** — chat with Llama 3.1 to place a booking
- **Book Manually** — redirects to admin form

### admin.html — Admin Panel
- **New Booking tab** — manual form with auto price calculation
- **All Bookings tab** — view, update status, delete bookings

### AI Agent Flow
```
Name → Phone → Coffee → Size → Quantity → Pickup Time → Confirm → Saved to DB
```
Understands natural language — user can say "large latte for 2" and agent extracts all fields at once.

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/bookings` | Create booking |
| `GET` | `/bookings` | Get all bookings |
| `PATCH` | `/bookings/{id}/status` | Update status |
| `DELETE` | `/bookings/{id}` | Delete booking |
| `POST` | `/chat` | AI agent message |

---

