import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

logger = logging.getLogger("email_service")


def send_lead_email(data: dict) -> bool:
    """Emails the new enquiry to the business owner. Returns True on success.
    Never raises — a failure here must not break the contact form."""
    if not (settings.SMTP_USER and settings.SMTP_PASSWORD and settings.EMAIL_TO):
        logger.warning("SMTP not configured — skipping email notification.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"New Enquiry — {data['service']} ({data['name']})"
        msg["From"] = settings.EMAIL_FROM or settings.SMTP_USER
        msg["To"] = settings.EMAIL_TO

        travel_block = ""
        if data.get("from_station"):
            travel_block = f"""
            <hr style="border:none;border-top:1px solid #eee;margin:14px 0">
            <p><strong>From:</strong> {data.get('from_station')} &nbsp; <strong>To:</strong> {data.get('to_station')}</p>
            <p><strong>Journey date:</strong> {data.get('journey_date')} &nbsp; <strong>Return date:</strong> {data.get('return_date')}</p>
            <p><strong>Passengers:</strong> {data.get('passengers')}</p>
            """

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;
                    border:1px solid #ddd;border-radius:8px;overflow:hidden">
          <div style="background:#3B1E7A;color:#FBFAFF;padding:16px 20px">
            <h2 style="margin:0;font-size:18px">New website enquiry</h2>
          </div>
          <div style="padding:20px;color:#222">
            <p><strong>Name:</strong> {data['name']}</p>
            <p><strong>Phone:</strong> {data['phone']}</p>
            <p><strong>Email:</strong> {data.get('email') or '—'}</p>
            <p><strong>Service interested:</strong> {data['service']}</p>
            <p><strong>Message:</strong><br>{data.get('message') or '—'}</p>
            {travel_block}
          </div>
        </div>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(msg["From"], [settings.EMAIL_TO], msg.as_string())

        return True
    except Exception as exc:
        logger.error(f"Email send failed: {exc}")
        return False
