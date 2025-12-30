import logging
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from src.tools.flight.amadeus.core import AmadeusFlightTool
from src.schemas.order import CreateFlightOrder, FlightOffer


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class AgentFlightTool:
    """
    LangChain tools wrapper for AmadeusFlightTool.
    Provides async tools for:
    - search_flights
    - get_flight_price
    - create_order
    """

    @classmethod
    def search_flights_tool(cls):
        @tool(
            description=(
                "Search for flights between an origin and a destination. "
                "Optional parameters include departure and return dates, "
                "number of adults, travel class, maximum price, and maximum number of results. "
                "Returns a list of flight offers."
            )
        )
        async def search_flights(
            origin: str,
            destination: Optional[str] = None,
            departure_date: Optional[str] = None,
            return_date: Optional[str] = None,
            adults: int = 1,
            travel_class: str = "ECONOMY",
            max_price: Optional[float] = None,
            max_results: int = 10
        ) -> List[Dict[str, Any]]:
            try:
                return await AmadeusFlightTool.search_flights(
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                    return_date=return_date,
                    adults=adults,
                    travel_class=travel_class,
                    max_price=max_price,
                    max_results=max_results
                )
            except Exception as e:
                logger.error(f"search_flights_tool error: {e}")
                return []

        return search_flights

    @classmethod
    def get_flight_price_tool(cls):
        @tool(
            description=(
                "Get detailed pricing for a specific flight offer. "
                "Input should be a flight offer object returned from search_flights. "
                "Returns the pricing details including total cost, taxes, and fare breakdown."
            )
        )
        async def get_flight_price(flight_offer: FlightOffer) -> Dict:
            try:
                return await AmadeusFlightTool.get_flight_price(flight_offer)
            except Exception as e:
                logger.error(f"get_flight_price_tool error: {e}")
                return {}

        return get_flight_price

    @classmethod
    def create_order_tool(cls):
        @tool(
            description=(
                "Create a flight order using provided order information. "
                "Input should be a CreateFlightOrder object with passenger and flight details. "
                "Returns the confirmed booking details or error information."
            )
        )
        async def create_order(order_info: CreateFlightOrder) -> Dict:
            try:
                return await AmadeusFlightTool.create_order(order_info)
            except Exception as e:
                logger.error(f"create_order_tool error: {e}")
                return {}

        return create_order
