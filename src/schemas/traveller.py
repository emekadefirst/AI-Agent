from enum import Enum
from typing import List
from datetime import date
from src.schemas.agent import AgentGuidedModel
from pydantic import BaseModel, EmailStr, Field


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class DocumentType(str, Enum):
    PASSPORT = "PASSPORT"


class FullName(BaseModel):
    firstName: str
    lastName: str


class PhoneObject(BaseModel):
    deviceType: str
    countryCallingCode: str
    number: str


class Contact(BaseModel):
    emailAddress: EmailStr
    phones: List[PhoneObject]


class DocumentObject(BaseModel):
    documentType: DocumentType
    birthPlace: str
    issuanceLocation: str
    issuanceDate: date
    number: str
    expiryDate: date
    issuanceCountry: str
    validityCountry: str
    nationality: str
    holder: bool


class TravellerObject(AgentGuidedModel):
    id: str
    dateOfBirth: date
    name: FullName
    gender: Gender
    contact: Contact
    documents: List[DocumentObject]

    
    @classmethod
    def example(cls) -> "TravellerObject":
        return cls(
            id="1",
            dateOfBirth=date(1982, 1, 16),
            name=FullName(
                firstName="JORGE",
                lastName="GONZALES"
            ),
            gender=Gender.MALE,
            contact=Contact(
                emailAddress="jorge.gonzales833@telefonica.es",
                phones=[
                    PhoneObject(
                        deviceType="MOBILE",
                        countryCallingCode="34",
                        number="480080076"
                    )
                ]
            ),
            documents=[
                DocumentObject(
                    documentType=DocumentType.PASSPORT,
                    birthPlace="Madrid",
                    issuanceLocation="Madrid",
                    issuanceDate=date(2015, 4, 14),
                    number="00000000",
                    expiryDate=date(2025, 4, 14),
                    issuanceCountry="ES",
                    validityCountry="ES",
                    nationality="ES",
                    holder=True
                )
            ]
        )


