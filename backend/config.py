"""
Central configuration. All values are read from environment variables
(or a .env file in the backend/ folder). Nothing sensitive is hard-coded.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- MySQL ----
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "one_stop_solutions"

    # ---- SMTP (email notifications) ----
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""          # sending mailbox, e.g. yourbusiness@gmail.com
    SMTP_PASSWORD: str = ""      # app password (not your normal password)
    EMAIL_FROM: str = ""         # usually same as SMTP_USER
    EMAIL_TO: str = ""           # Kinjal Shah's email — where leads land

    # ---- WhatsApp Cloud API (Meta) ----
    WHATSAPP_TOKEN: str = ""            # permanent/system-user access token
    WHATSAPP_PHONE_NUMBER_ID: str = ""  # sender's WhatsApp Business phone number id
    WHATSAPP_TO_NUMBER: str = "919998883276"  # Kinjal Shah, country code + number, no '+'

    # ---- App ----
    ALLOWED_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
