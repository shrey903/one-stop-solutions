import logging
import requests
from config import settings

logger = logging.getLogger("whatsapp_service")

GRAPH_API_URL = "https://graph.facebook.com/v20.0/{phone_id}/messages"


def send_lead_whatsapp(data: dict) -> bool:
    """Sends the new enquiry to Kinjal Shah's WhatsApp via Meta's WhatsApp
    Cloud API. Returns True on success. Never raises.

    Requires a WhatsApp Business Platform app (Meta for Developers) with:
      WHATSAPP_TOKEN            - permanent access token
      WHATSAPP_PHONE_NUMBER_ID  - the sending number's phone_number_id
      WHATSAPP_TO_NUMBER        - receiving number, country code + number, no '+'
    """
    if not (settings.WHATSAPP_TOKEN and settings.WHATSAPP_PHONE_NUMBER_ID):
        logger.warning("WhatsApp API not configured — skipping WhatsApp notification.")
        return False

    text = (
        f"*New website enquiry — One Stop Solutions*\n"
        f"Name: {data['name']}\n"
        f"Phone: {data['phone']}\n"
        f"Email: {data.get('email') or '-'}\n"
        f"Service: {data['service']}\n"
        f"Message: {data.get('message') or '-'}"
    )

    if data.get("from_station"):
        text += (
            f"\n\n*Journey Details*\n"
            f"From: {data.get('from_station')}\n"
            f"To: {data.get('to_station')}\n"
            f"Journey date: {data.get('journey_date')}\n"
            f"Return date: {data.get('return_date')}\n"
            f"Passengers: {data.get('passengers')}"
        )

    url = GRAPH_API_URL.format(phone_id=settings.WHATSAPP_PHONE_NUMBER_ID)
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": settings.WHATSAPP_TO_NUMBER,
        "type": "text",
        "text": {"body": text},
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            return True
        logger.error(f"WhatsApp send failed: {resp.status_code} {resp.text}")
        return False
    except Exception as exc:
        logger.error(f"WhatsApp send failed: {exc}")
        return False
