from src.configs.http import AsyncHTTPRequest, Methods
from src.configs.env import (
    AMADEUS_CLIENT_ID,
    AMADEUS_CLIENT_SECRET,
    AMADEUS_BASE_URL
)
import httpx

class AmadeusAuth:
    _access_token: str | None = None

    @classmethod
    async def get_token(cls) -> str:
        if cls._access_token:
            return cls._access_token

        # Use httpx directly for form-encoded data
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AMADEUS_BASE_URL}/v1/security/oauth2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "client_credentials",
                    "client_id": AMADEUS_CLIENT_ID,
                    "client_secret": AMADEUS_CLIENT_SECRET
                }
            )
            response.raise_for_status()
            response_json = response.json()
        
        cls._access_token = response_json["access_token"]
        return cls._access_token