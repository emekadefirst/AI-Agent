from typing import List, Optional
from pydantic import BaseModel
from src.schemas.agent import AgentGuidedModel



# -------------------------
# Common / Shared Models
# -------------------------

class Aircraft(BaseModel):
    code: str


class Operating(BaseModel):
    carrierCode: str


class Location(BaseModel):
    iataCode: str
    terminal: Optional[str] = None
    at: str


class AmenityProvider(BaseModel):
    name: str


class Amenity(BaseModel):
    description: str
    isChargeable: bool
    amenityType: str
    amenityProvider: AmenityProvider


class BagAllowance(BaseModel):
    quantity: int


# -------------------------
# Flight Segments
# -------------------------

class Segment(BaseModel):
    departure: Location
    arrival: Location
    carrierCode: str
    number: str
    aircraft: Aircraft
    operating: Operating
    duration: str
    id: str
    numberOfStops: int
    blacklistedInEU: bool


class Itinerary(BaseModel):
    duration: str
    segments: List[Segment]


# -------------------------
# Pricing
# -------------------------

class Fee(BaseModel):
    amount: str
    type: str


class AdditionalService(BaseModel):
    amount: str
    type: str


class Price(BaseModel):
    currency: str
    total: str
    base: str
    fees: Optional[List[Fee]] = None
    grandTotal: Optional[str] = None
    additionalServices: Optional[List[AdditionalService]] = None


class PricingOptions(BaseModel):
    fareType: List[str]
    includedCheckedBagsOnly: bool


# -------------------------
# Traveler Pricing
# -------------------------

class FareDetailsBySegment(BaseModel):
    segmentId: str
    cabin: str
    fareBasis: str
    brandedFare: str
    brandedFareLabel: str
    class_: str
    includedCheckedBags: BagAllowance
    includedCabinBags: BagAllowance
    amenities: List[Amenity]

    class Config:
        fields = {"class_": "class"}


class TravelerPricing(BaseModel):
    travelerId: str
    fareOption: str
    travelerType: str
    price: Price
    fareDetailsBySegment: List[FareDetailsBySegment]


# -------------------------
# Root Flight Offer
# -------------------------

class FlightOffer(AgentGuidedModel):
    type: str
    id: str
    source: str
    instantTicketingRequired: bool
    nonHomogeneous: bool
    oneWay: bool
    isUpsellOffer: bool
    lastTicketingDate: str
    lastTicketingDateTime: str
    numberOfBookableSeats: int
    itineraries: List[Itinerary]
    price: Price
    pricingOptions: PricingOptions
    validatingAirlineCodes: List[str]
    travelerPricings: List[TravelerPricing]


    @classmethod
    def example(cls):
        return cls(
            type="flight-offer",
            id="1",
            source="GDS",
            instantTicketingRequired=False,
            nonHomogeneous=False,
            oneWay=False,
            isUpsellOffer=False,
            lastTicketingDate="2026-01-07",
            lastTicketingDateTime="2026-01-07",
            numberOfBookableSeats=9,
            itineraries=[],
            price=Price(
                currency="EUR",
                total="250.00",
                base="200.00"
            ),
            pricingOptions=PricingOptions(
                fareType=["PUBLISHED"],
                includedCheckedBagsOnly=True
            ),
            validatingAirlineCodes=["AF"],
            travelerPricings=[]
        )
