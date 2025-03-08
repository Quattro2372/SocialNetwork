import logging
import httpx

from fastapi import Response
from fastapi.encoders import jsonable_encoder


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_request(method: str, url: str, request: dict):
    async with httpx.AsyncClient() as client:
        logger.info(request)
        response = await client.request(method=method, url=url, json=jsonable_encoder(request))
        return Response(response.content, response.status_code)