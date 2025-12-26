from src.schemas.flight import FlightOffer
from src.schemas.traveller import TravellerObject
from pydantic import BaseModel
from typing import Literal, List
from src.schemas.agent import AgentGuidedModel

class FlightOrderSchema(AgentGuidedModel):
    type: Literal["flight-order"]
    flightOffers: List[FlightOffer]
    travelers: List[TravellerObject]

    @classmethod
    def example(cls):
        return cls(
            type="flight-order",
            flightOffers=[FlightOffer.example()],
            travelers=[TravellerObject.example()]
        )



class CreateFlightOrder(AgentGuidedModel):
    data: FlightOrderSchema

    @classmethod
    def example(cls):
        return cls(
            data=FlightOrderSchema.example()
        )

