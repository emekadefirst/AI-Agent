import logging
from typing import List, Optional
from langchain_core.tools import tool
from src.tools.hotel.amadeus.core import AmadeusHotelTool
from src.schemas.hotel import HotelOrderSchema, GeoCode

# --- Logger setup ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class AgentHotelTool:
    """
    LangChain tools wrapper for AmadeusHotelTool.
    Provides async tools for:
    - fetch hotel data
    - fetch hotel ratings
    - fetch hotel offers
    - book hotels
    """

    @classmethod
    def fetch_tool(cls):
        @tool(
            description=(
                "Fetch hotel information by city code, geo coordinates, or hotel ID. "
                "At least one parameter must be provided: city_code, geo_code, or hotel_id. "
                "Returns hotel details including name, location, and basic info."
            )
        )
        async def fetch(
            hotel_id: Optional[str] = None,
            geo_code: Optional[GeoCode] = None,
            city_code: Optional[str] = None
        ):
            try:
                return await AmadeusHotelTool.fetch(hotel_id=hotel_id, geo_code=geo_code, city_code=city_code)
            except Exception as e:
                logger.error(f"fetch_hotel_tool error: {e}")
                return {}

        return fetch

    @classmethod
    def rating_tool(cls):
        @tool(
            description=(
                "Fetch hotel ratings or sentiment data by providing a list of hotel IDs. "
                "Returns ratings and guest sentiment insights for the specified hotels."
            )
        )
        async def rating(hotel_ids: Optional[List[str]] = None):
            try:
                return await AmadeusHotelTool.rating(hotel_ids=hotel_ids)
            except Exception as e:
                logger.error(f"fetch_hotel_rating_tool error: {e}")
                return {}

        return rating

    @classmethod
    def offer_tool(cls):
        @tool(
            description=(
                "Fetch hotel offers for a given hotel ID and number of adults. "
                "Returns available room offers including prices and availability."
            )
        )
        async def offer(hotel_id: str, adult_count: int = 1):
            try:
                return await AmadeusHotelTool.offer(hotel_id=hotel_id, adult_count=adult_count)
            except Exception as e:
                logger.error(f"fetch_hotel_offer_tool error: {e}")
                return {}

        return offer

    @classmethod
    def book_tool(cls):
        @tool(
            description=(
                "Book a hotel using the provided HotelOrderSchema data, which includes "
                "guest details, hotel ID, and room information. Returns booking confirmation or errors."
            )
        )
        async def book(data: HotelOrderSchema):
            try:
                return await AmadeusHotelTool.book(data)
            except Exception as e:
                logger.error(f"book_hotel_tool error: {e}")
                return {}

        return book


# --- Tools list ---

