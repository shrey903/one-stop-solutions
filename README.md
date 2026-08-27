# One Stop Solutions — Website

Paperwork & travel-booking business site. Backend: **FastAPI**.
Frontend: **Bootstrap 5**, multi-page, light navy-and-gold design system.
Database: **MySQL**. Every contact-form submission is saved to MySQL, then
emailed and WhatsApp'd to the business owner automatically (backend
notification only — there is no customer-facing WhatsApp button on the site).

## Site map

- `/` — Home: compact hero, 3 service KPI cards, live testimonials bar
- `/services/accounting.html` — Accounting Services (intro + listing + scoped enquiry form)
- `/services/pan-card.html` — PAN Card & Other Services (intro + listing + scoped enquiry form)
- `/services/travel.html` — Travel Booking Services (intro + listing + scoped enquiry form with journey fields)
- `/feedback.html` — Feedback form with a tab per service; feeds the homepage testimonials bar
- `/contact.html` — General enquiry form (all services)

## Feedback / testimonials system

- `POST /api/feedback` — saves a feedback entry (`name`, `service`, `rating` 1-5, `message`)
- `GET /api/feedback/top` — top 5 by rating (ties broken by newest) — used by the homepage bar
- `GET /api/feedback` — all feedback, newest first (simple admin view)
- The homepage polls `/api/feedback/top` every 8s so new submissions appear within seconds,
  and auto-advances the visible testimonial once every 60 seconds.
- Run `schema.sql` (or let the app auto-create tables on first start) to add the `feedback` table.

## 1. Install

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env      # then edit .env with real values (see below)
```

## 2. Create the database

MySQL must be running. Either let the app create the table automatically
(it does, on first start), or run it yourself:

```bash
mysql -u root -p < ../schema.sql
```

## 3. Configure `.env`

| Variable | What it's for |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | MySQL connection |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`, `EMAIL_TO` | Sends the lead notification email. For Gmail: turn on 2FA, then create an **App Password** at myaccount.google.com/apppasswords and use that as `SMTP_PASSWORD`. `EMAIL_TO` is Kinjal's inbox. |
| `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_TO_NUMBER` | Sends the lead as a WhatsApp message via Meta's **WhatsApp Cloud API**. Create a free app at developers.facebook.com → WhatsApp product, get a permanent access token + the sender number's `phone_number_id`. `WHATSAPP_TO_NUMBER` is Kinjal's number as `919998883276` (country code, no `+`). |

If SMTP or WhatsApp variables are left blank, the form still saves to MySQL
and shows success to the visitor — it just skips that one notification and
logs a warning, so a missing API key never breaks the website.

## 4. Run

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000** — the FastAPI app serves both the API and the
website (no separate frontend server needed).

## 5. What happens on submit

1. Form data is validated and saved to the `contact_submissions` table.
2. The visitor immediately sees a success message.
3. In the background: an email is sent to `EMAIL_TO`, and a WhatsApp text is
   sent to `WHATSAPP_TO_NUMBER` — both with the enquirer's name, phone,
   email, chosen service, and message.
4. `GET /api/contacts` lists all captured leads (add real auth before
   exposing this publicly in production).

## Project structure

```
one-stop-solutions/
├── backend/
│   ├── main.py            FastAPI app + routes, serves the frontend
│   ├── config.py          reads .env
│   ├── database.py        MySQL/SQLAlchemy engine
│   ├── models.py          contact_submissions table
│   ├── schemas.py         request/response validation
│   ├── email_service.py   SMTP notification
│   ├── whatsapp_service.py WhatsApp Cloud API notification
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   └── static/
│       ├── css/style.css
│       └── js/script.js
└── schema.sql              optional manual DB setup
```
