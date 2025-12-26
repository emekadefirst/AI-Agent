from typing import Dict, Any
from src.tools.registry import ToolRegistry
from src.tools.hotel.amadeus.core import AmadeusHotelTool
from src.schemas.hotel import HotelOrderSchema, GeoCode


class HotelToolRouter:
    @staticmethod
    async def execute(action: str, payload: Dict[str, Any]) -> Any:
        """
        Execute the given hotel action with the provided payload.
        Validates the action and parameters using ToolRegistry.
        """
        ToolRegistry.validate_action(action, payload)

        if action == "fetch_hotel":
            geo_code = payload.get("geo_code")
            if geo_code and isinstance(geo_code, dict):
                geo_code = GeoCode(**geo_code)  # convert dict to Pydantic model
            return await AmadeusHotelTool.fetch(
                hotel_id=payload.get("hotel_id"),
                city_code=payload.get("city_code"),
                geo_code=geo_code
            )

        if action == "fetch_hotel_offers":
            return await AmadeusHotelTool.offer(
                hotel_id=payload["hotel_id"],
                adult_count=payload.get("adult_count", 1)
            )

        if action == "fetch_hotel_rating":
            return await AmadeusHotelTool.rating(
                hotel_ids=payload["hotel_ids"]
            )

        if action == "book_hotel":
            data = payload["data"]
            if isinstance(data, dict):
                data = HotelOrderSchema(**data)  # convert dict to Pydantic model
            return await AmadeusHotelTool.book(data)
