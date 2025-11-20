import httpx
from app.domain.models import TextResponse, AvailableIdsResponse
from app.core.exceptions import DjangoAPIError


class DjangoClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_text(self, item_id: int) -> TextResponse:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.base_url}/lol/{item_id}/")
                if response.status_code == 404:
                    return TextResponse(id=item_id, extracted_text="", error="Not found")
                response.raise_for_status()
                data = response.json()
                return TextResponse(
                    id=item_id,
                    extracted_text=data.get("extracted_text", "Text not found")
                )
        except Exception as e:
            raise DjangoAPIError(f"Django API error: {str(e)}")

    async def get_available_ids(self) -> AvailableIdsResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/available-ids/")
                response.raise_for_status()
                data = response.json()
                return AvailableIdsResponse(**data)
        except Exception as e:
            raise DjangoAPIError(f"Django API error: {str(e)}")

    async def download_image(self, image_url: str) -> bytes:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise DjangoAPIError(f"Image download error: {str(e)}")