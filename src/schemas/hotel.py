from typing import List
from datetime import date
from pydantic import BaseModel, EmailStr, Field
from src.schemas.agent import AgentGuidedModel


class GeoCode(BaseModel):
    latitude: float 
    longitude: float 



class GuestSchema(BaseModel):
    tid: int
    title: str = Field(..., max_length=10)
    firstName: str = Field(..., max_length=150)
    lastName: str = Field(..., max_length=150)
    phone: str = Field(..., max_length=25)
    email: EmailStr = Field(..., max_length=60)


# --- Payment Card Info ---
class PaymentCardInfoSchema(BaseModel):
    vendorCode: str = Field(..., max_length=5)
    cardNumber: str = Field(..., max_length=20)
    expiryDate: date
    holderName: str = Field(..., max_length=250)


class PaymentCardSchema(BaseModel):
    paymentCardInfo: PaymentCardInfoSchema


class PaymentSchema(BaseModel):
    method: str = Field(..., max_length=50)
    paymentCard: PaymentCardSchema


# --- Travel Agent ---
class AgentContactSchema(BaseModel):
    email: EmailStr = Field(..., max_length=60)


class TravelAgentSchema(BaseModel):
    contact: AgentContactSchema


# --- Room Associations ---
class GuestReferenceSchema(BaseModel):
    guestReference: str  


class RoomAssociationSchema(BaseModel):
    guestReferences: List[GuestReferenceSchema]
    hotelOfferId: str 


# --- Hotel Order Main Schema ---
class HotelOrderDataSchema(BaseModel):
    type: str = Field(..., max_length=50)
    guests: List[GuestSchema]
    travelAgent: TravelAgentSchema
    roomAssociations: List[RoomAssociationSchema]
    payment: PaymentSchema


class HotelOrderSchema(AgentGuidedModel):
    data: HotelOrderDataSchema

