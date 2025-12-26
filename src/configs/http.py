import httpx
from enum import Enum
from typing import Optional, Dict, Any


class Methods(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
    OPTION = "option"
    HEAD = "head"


class AsyncHTTPRequest:
    _client: Optional[httpx.AsyncClient] = None

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        if cls._client is None:
            limits = httpx.Limits(
                max_connections=50,
                max_keepalive_connections=20,
            )
            cls._client = httpx.AsyncClient(timeout=30.0, limits=limits)
        return cls._client

    @classmethod
    async def request(
        cls,
        *,
        url: str,
        method: Methods,
        params: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ):
        client = await cls.get_client()

        response = await client.request(
            method.value.upper(),
            url,
            params=params,
            json=json,
            headers=headers,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            print("Gemini error response:", response.text)
            raise

        return response.json()
