from typing import Dict, Any
from src.tools.registry import ToolRegistry
from src.tools.flight.amadeus.core import AmadeusFlightTool


class FlightToolRouter:
    @staticmethod
    async def execute(action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        ToolRegistry.validate_action(action, payload)

        if action == "search_flight":
            return await AmadeusFlightTool.search_flights(**payload)

        if action == "get_flight_price":
            return await AmadeusFlightTool.get_flight_price(
                payload["flight_offer"]
            )

        if action == "book_flight":
            return await AmadeusFlightTool.create_order(payload)
