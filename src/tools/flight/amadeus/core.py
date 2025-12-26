import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from src.configs.http import AsyncHTTPRequest, Methods
from src.tools.flight.amadeus.auth import AmadeusAuth
from src.configs.env import AMADEUS_BASE_URL
from src.schemas.order import CreateFlightOrder, FlightOffer

# --- Logger setup ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

CITY_TO_IATA = {
    "lagos": "LOS",
    "london": "LHR",
    "new york": "JFK",
    "paris": "CDG",
    "tokyo": "NRT",
    "dubai": "DXB",
    "los angeles": "LAX",
    "san francisco": "SFO",
    "toronto": "YYZ",
    "sydney": "SYD",
    "mumbai": "BOM",
    "delhi": "DEL",
    "singapore": "SIN",
    "hong kong": "HKG",
    "bangkok": "BKK",
}


class AmadeusFlightTool:

    @staticmethod
    def _to_iata_code(location: str) -> str:
        """Convert city/country name to IATA code if possible."""
        try:
            if not location:
                return location
            
            location_clean = location.strip().upper()
            if len(location_clean) == 3 and location_clean.isalpha():
                return location_clean

            location_lower = location.lower().strip()
            for city, code in CITY_TO_IATA.items():
                if city in location_lower or location_lower in city:
                    return code
            
            # Fallback: first 3 letters
            words = location.split()
            if words and len(words[0]) >= 3:
                return words[0][:3].upper()
            
            return location
        except Exception as e:
            logger.error(f"Error converting location '{location}' to IATA: {e}")
            return location

    @staticmethod
    def _normalize_date(date_str: str, return_date: Optional[str] = None) -> str:
        """Normalize date string and fix past years relative to 2025-12-25."""
        try:
            if not date_str:
                return date_str
            
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime(2025, 12, 25)
            
            if date_obj < today:
                date_obj = date_obj.replace(year=date_obj.year + 1)
            
            if return_date:
                try:
                    return_obj = datetime.strptime(return_date, "%Y-%m-%d")
                    if date_obj > return_obj:
                        date_obj = date_obj.replace(year=date_obj.year - 1)
                except Exception:
                    pass
            
            return date_obj.strftime("%Y-%m-%d")
        except Exception as e:
            logger.warning(f"Failed to normalize date '{date_str}': {e}")
            return date_str

    @classmethod
    async def search_flights(
        cls,
        origin: str,
        destination: Optional[str] = None,
        departure_date: Optional[str] = None,
        return_date: Optional[str] = None,
        adults: int = 1,
        travel_class: str = "ECONOMY",
        max_price: Optional[float] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Fetch flight offers or destinations."""
        try:
            token = await AmadeusAuth.get_token()

            def clean_param(val):
                if val is None or str(val).strip() in ("None", ""):
                    return None
                return str(val).strip()
            
            origin = clean_param(origin)
            destination = clean_param(destination)
            departure_date = clean_param(departure_date)
            return_date = clean_param(return_date)
            max_price = clean_param(max_price)
            travel_class = clean_param(travel_class) or "ECONOMY"

            departure_date = cls._normalize_date(departure_date, return_date)
            return_date = cls._normalize_date(return_date)

            origin = cls._to_iata_code(origin)
            destination = cls._to_iata_code(destination)

            try:
                adults = int(adults) if clean_param(adults) else 1
            except (ValueError, TypeError):
                adults = 1

            try:
                max_results = int(max_results) if clean_param(max_results) else 10
            except (ValueError, TypeError):
                max_results = 10

            if destination:
                params = {
                    "originLocationCode": origin,
                    "destinationLocationCode": destination,
                    "adults": adults,
                    "travelClass": travel_class.upper(),
                    "currencyCode": "USD",
                    "max": max_results
                }
                if departure_date:
                    params["departureDate"] = departure_date
                if return_date:
                    params["returnDate"] = return_date

                response = await AsyncHTTPRequest.request(
                    method=Methods.GET,
                    url=f"{AMADEUS_BASE_URL}/v2/shopping/flight-offers",
                    headers={"Authorization": f"Bearer {token}"},
                    params=params
                )
                return response.get("data", [])

            else:
                params = {"origin": origin}
                if max_price:
                    params["maxPrice"] = max_price
                if departure_date:
                    params["departureDate"] = departure_date
                if return_date:
                    params["returnDate"] = return_date

                response = await AsyncHTTPRequest.request(
                    method=Methods.GET,
                    url=f"{AMADEUS_BASE_URL}/v1/shopping/flight-destinations",
                    headers={"Authorization": f"Bearer {token}"},
                    params=params
                )
                return response.get("data", [])

        except Exception as e:
            logger.error(f"Search flights failed: {e}")
            return []

    @classmethod
    async def get_flight_price(cls, flight_offer: FlightOffer) -> Dict:
        """Get pricing for a flight offer."""
        try:
            token = await AmadeusAuth.get_token()
            return await AsyncHTTPRequest.request(
                method=Methods.POST,
                url=f"{AMADEUS_BASE_URL}/v1/shopping/flight-offers/pricing",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "data": {
                        "type": "flight-offers-pricing",
                        "flightOffers": [flight_offer]
                    }
                }
            )
        except Exception as e:
            logger.error(f"Get flight price failed: {e}")
            return {}

    @classmethod
    async def create_order(cls, order_info: CreateFlightOrder) -> Dict:
        """Create a flight order."""
        try:
            token = await AmadeusAuth.get_token()
            return await AsyncHTTPRequest.request(
                method=Methods.POST,
                url=f"{AMADEUS_BASE_URL}/v1/booking/flight-orders",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=order_info
            )
        except Exception as e:
            logger.error(f"Create flight order failed: {e}")
            return {}
