from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional

TRAVEL_SERVICES = {"Flight Tickets", "Bus Tickets", "Train Tickets"}


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    phone: str = Field(..., min_length=8, max_length=20)
    email: EmailStr
    service: str = Field(..., min_length=2, max_length=120)
    message: Optional[str] = Field(None, max_length=1000)

    from_station: Optional[str] = Field(None, max_length=120)
    to_station: Optional[str] = Field(None, max_length=120)
    journey_date: Optional[str] = Field(None, max_length=20)
    return_date: Optional[str] = Field(None, max_length=20)
    passengers: Optional[str] = Field(None, max_length=10)

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, v: str) -> str:
        digits = "".join(ch for ch in v if ch.isdigit())
        if len(digits) < 8:
            raise ValueError("Enter a valid phone number")
        return digits

    @model_validator(mode="after")
    def require_travel_details(self):
        if self.service in TRAVEL_SERVICES:
            required = {
                "from_station": self.from_station,
                "to_station": self.to_station,
                "journey_date": self.journey_date,
                "return_date": self.return_date,
                "passengers": self.passengers,
            }
            missing = [k for k, v in required.items() if not v or not v.strip()]
            if missing:
                raise ValueError(f"Missing journey details for travel booking: {', '.join(missing)}")
        return self


FEEDBACK_SERVICES = {
    "Accounting Services",
    "PAN Card and Other Services",
    "Travel Booking Services",
}


class FeedbackCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    service: str = Field(..., min_length=2, max_length=60)
    rating: int = Field(..., ge=1, le=5)
    message: str = Field(..., min_length=10, max_length=800)

    @field_validator("service")
    @classmethod
    def valid_service(cls, v: str) -> str:
        if v not in FEEDBACK_SERVICES:
            raise ValueError("Unknown service category")
        return v


class FeedbackOut(BaseModel):
    id: int
    name: str
    service: str
    rating: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class ContactOut(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    service: str
    message: Optional[str]
    from_station: Optional[str]
    to_station: Optional[str]
    journey_date: Optional[str]
    return_date: Optional[str]
    passengers: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
