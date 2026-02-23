import httpx
from fastapi import HTTPException

CHICAGO_API_URL = "https://api.artic.edu/api/v1/artworks"


async def validate_external_place(external_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CHICAGO_API_URL}/{external_id}", timeout=5.0)

            if response.status_code == 200:
                return True
            return False
        except httpx.RequestError:
            raise HTTPException(
                status_code=503,
                detail="Chicago API is currently unavailable"
            )