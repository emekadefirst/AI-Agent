import logging
from typing import List, Optional
from src.configs import env, http
from src.tools.hotel.amadeus import auth
from src.schemas.hotel import HotelOrderSchema, GeoCode

# --- Configure logger ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Change to DEBUG for more detailed logs

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class AmadeusHotelTool:

    @classmethod
    async def get_token(cls) -> str:
        """Retrieve the Amadeus API access token asynchronously."""
        try:
            return await auth.AmadeusAuth.get_token()
        except Exception as e:
            logger.error(f"Failed to get token: {e}")
            raise RuntimeError("Unable to retrieve Amadeus API token.") from e

    @classmethod
    async def fetch(
        cls,
        hotel_id: Optional[str] = None,
        geo_code: Optional[GeoCode] = None,
        city_code: Optional[str] = None
    ):
        """Fetch hotel data by city code, geo coordinates, or hotel IDs."""
        try:
            url = None
            if city_code:
                url = (
                    f"{env.AMADEUS_BASE_URL}/v1/reference-data/locations/hotels/by-city"
                    f"?cityCode={city_code.upper()}"
                )
            elif geo_code:
                url = (
                    f"{env.AMADEUS_BASE_URL}/v1/reference-data/locations/hotels/by-geocode"
                    f"?latitude={geo_code.latitude}&longitude={geo_code.longitude}"
                )
            elif hotel_id:
                url = (
                    f"{env.AMADEUS_BASE_URL}/v1/reference-data/locations/hotels/by-hotels"
                    f"?hotelIds={hotel_id}"
                )
            else:
                raise ValueError("At least one of hotel_id, geo_code, or city_code must be provided.")

            token = await cls.get_token()
            return await http.AsyncHTTPRequest.request(
                method=http.Methods.GET,
                url=url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
        except Exception as e:
            logger.error(f"Fetching hotel data failed: {e}")
            raise

    @classmethod
    async def rating(
        cls,
        hotel_ids: Optional[List[str]] = None
    ):
        """Fetch hotel ratings / sentiment data."""
        try:
            if not hotel_ids:
                raise ValueError("hotel_ids list must be provided for rating.")

            hotel_ids_str = ",".join(hotel_ids)
            url = (
                f"{env.AMADEUS_BASE_URL}/v2/e-reputation/hotel-sentiments"
                f"?hotelIds={hotel_ids_str}"
            )

            token = await cls.get_token()
            return await http.AsyncHTTPRequest.request(
                method=http.Methods.GET,
                url=url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
        except Exception as e:
            logger.error(f"Fetching hotel ratings failed: {e}")
            raise

    @classmethod
    async def offer(
        cls,
        hotel_id: str,
        adult_count: int = 1
    ):
        """Fetch hotel offers."""
        try:
            url = f"{env.AMADEUS_BASE_URL}/v3/shopping/hotel-offers?hotelIds={hotel_id}&adults={adult_count}"
            token = await cls.get_token()
            return await http.AsyncHTTPRequest.request(
                method=http.Methods.GET,
                url=url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
        except Exception as e:
            logger.error(f"Fetching hotel offers failed: {e}")
            raise

    @classmethod
    async def book(
        cls,
        data: HotelOrderSchema
    ):
        """Book a hotel using the provided HotelOrderSchema data."""
        try:
            url = f"{env.AMADEUS_BASE_URL}/v2/booking/hotel-orders"
            token = await cls.get_token()
            return await http.AsyncHTTPRequest.request(
                method=http.Methods.POST,
                url=url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=data.dict()
            )
        except Exception as e:
            logger.error(f"Booking hotel failed: {e}")
            raise
