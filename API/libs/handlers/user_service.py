import json
from fastapi import APIRouter, Response
import logging

from libs.requester.requester import send_request
from libs.services import get_user_service_url

from ..models.models import (
    AuthWithUsernameRequest,
    AuthWithTokenRequest,
    AuthResponse,
    RegistrationRequest,
    RegistrationResponse,
    GetUserByUsernameRequest,
    GetUserByIDRequest,
    GetUserResponse,
    UserUpdateRequest,
    UserUpdateResponse,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.post("/register_user", status_code=200, response_model=RegistrationResponse, responses={400: {
    "model": RegistrationResponse}})
async def register_user(body: RegistrationRequest, response: Response) -> RegistrationResponse:
    service_response = await send_request('POST', get_user_service_url() + '/register_user', dict(body))
    response.status_code = service_response.status_code
    return json.loads(service_response.body.decode("utf-8"))


@api_router.post("/auth_with_username", status_code=200, response_model=AuthResponse, responses={400: {
    "model": AuthResponse}})
async def auth_with_username(body: AuthWithUsernameRequest, response: Response) -> AuthResponse:
    service_response = await send_request('POST', get_user_service_url() + '/auth_with_username', dict(body))
    response.status_code = service_response.status_code
    return json.loads(service_response.body.decode("utf-8"))


@api_router.post("/auth_with_token", status_code=200, response_model=AuthResponse, responses={400: {
    "model": AuthResponse}})
async def auth_with_token(body: AuthWithTokenRequest, response: Response) -> AuthResponse:
    service_response = await send_request('POST', get_user_service_url() + '/auth_with_token', dict(body))
    response.status_code = service_response.status_code
    return json.loads(service_response.body.decode("utf-8"))


@api_router.post("/get_user_by_username", status_code=200, response_model=GetUserResponse, responses={400: {
    "model": GetUserResponse}})
async def get_user_by_username(body: GetUserByUsernameRequest, response: Response) -> GetUserResponse:
    service_response = await send_request('POST', get_user_service_url() + '/get_user_by_username', dict(body))
    response.status_code = service_response.status_code
    return json.loads(service_response.body.decode("utf-8"))

@api_router.post("/get_user_by_id", status_code=200, response_model=GetUserResponse, responses={400: {
    "model": GetUserResponse}})
async def get_user_by_id(body: GetUserByIDRequest, response: Response) -> GetUserResponse:
    service_response = await send_request('POST', get_user_service_url() + '/get_user_by_id', dict(body))
    response.status_code = service_response.status_code
    return json.loads(service_response.body.decode("utf-8"))


@api_router.post("/update_user", status_code=200, response_model=UserUpdateResponse, responses={400: {
    "model": UserUpdateResponse}})
async def update_user(body: UserUpdateRequest, response: Response) -> UserUpdateResponse:
    service_response = await send_request('POST', get_user_service_url() + '/update_user', dict(body))
    response.status_code = service_response.status_code
    return json.loads(service_response.body.decode("utf-8"))


















