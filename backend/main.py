import logging
from pathlib import Path

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from config import settings
from database import engine, Base, get_db
from models import ContactSubmission, Feedback
from schemas import ContactCreate, ContactOut, FeedbackCreate, FeedbackOut
from email_service import send_lead_email
from whatsapp_service import send_lead_whatsapp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="One Stop Solutions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS] if settings.ALLOWED_ORIGINS != "*" else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def notify(data: dict, submission_id: int, db_url_hint=None):
    """Runs after the HTTP response is sent — sends email + WhatsApp."""
    email_ok = send_lead_email(data)
    wa_ok = send_lead_whatsapp(data)
    # Update the row with what actually went out, in a fresh session.
    from database import SessionLocal
    db = SessionLocal()
    try:
        row = db.query(ContactSubmission).get(submission_id)
        if row:
            row.email_sent = "yes" if email_ok else "no"
            row.whatsapp_sent = "yes" if wa_ok else "no"
            db.commit()
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/contact", response_model=ContactOut)
def create_contact(payload: ContactCreate, background: BackgroundTasks, db: Session = Depends(get_db)):
    row = ContactSubmission(
        name=payload.name.strip(),
        phone=payload.phone,
        email=str(payload.email),
        service=payload.service,
        message=(payload.message or "").strip() or None,
        from_station=payload.from_station,
        to_station=payload.to_station,
        journey_date=payload.journey_date,
        return_date=payload.return_date,
        passengers=payload.passengers,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    background.add_task(notify, payload.model_dump(), row.id)

    return row


@app.get("/api/contacts", response_model=list[ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    """Simple admin endpoint to view captured leads."""
    return db.query(ContactSubmission).order_by(ContactSubmission.created_at.desc()).all()


@app.post("/api/feedback", response_model=FeedbackOut)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    row = Feedback(
        name=payload.name.strip(),
        service=payload.service,
        rating=payload.rating,
        message=payload.message.strip(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.get("/api/feedback/top", response_model=list[FeedbackOut])
def top_feedback(db: Session = Depends(get_db)):
    """Top 5 rated feedback (highest rating first, most recent as tiebreaker)
    — powers the homepage testimonials bar."""
    return (
        db.query(Feedback)
        .order_by(Feedback.rating.desc(), Feedback.created_at.desc())
        .limit(5)
        .all()
    )


@app.get("/api/feedback", response_model=list[FeedbackOut])
def list_feedback(db: Session = Depends(get_db)):
    """All feedback, most recent first — simple admin view."""
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()


# ---- Serve the frontend ----
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


@app.get("/")
def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/contact.html")
def serve_contact():
    return FileResponse(str(FRONTEND_DIR / "contact.html"))


@app.get("/feedback.html")
def serve_feedback():
    return FileResponse(str(FRONTEND_DIR / "feedback.html"))


@app.get("/services/{page_name}.html")
def serve_service_page(page_name: str):
    file_path = FRONTEND_DIR / "services" / f"{page_name}.html"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(str(file_path))
