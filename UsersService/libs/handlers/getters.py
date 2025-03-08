from datetime import datetime, timedelta
import logging
import uuid

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from libs.database.queries.queries import (
    select_all_users,
    select_user_by_user_id,
    select_user_by_username,
    select_user_profile_by_user_id,
    select_user_sessions_by_user_id,
)
from models.database_models import User, UserSession, UserProfile
from libs.database.database_management import Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()

def get_json_from_user(user: User) -> dict:
    return {
        "user_id": str(user.user_id),
        "username": user.username,
        "encoded_password": user.encoded_password,
        "email": user.email,
        "phone_number": user.phone_number,
    }

def get_json_from_user_session(user_session: UserSession) -> dict:
    return {
        "token": str(user_session.token),
        "user_id": str(user_session.user_id),
        "terminated": user_session.terminated,
        "created_at": user_session.created_at.timestamp(),
        "active_until": user_session.active_until.timestamp(),
    }

def get_json_from_user_profile(user_profile: UserProfile) -> dict:
    return {
        "user_id": str(user_profile.user_id),
        "name": user_profile.name,
        "surname": user_profile.surname,
        "photo_url": user_profile.photo_url,
        "update_timestamp": user_profile.update_timestamp.timestamp(),
    }

@api_router.get("/get_all_users_debug", include_in_schema=False)
async def get_all_users() -> JSONResponse:
    session = Session()

    users: list[User] = select_all_users(session)

    if not users:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    logger.info(f"Got all users: {users=}")
    session.commit()

    json_compatible_users: list[dict] = []
    for user in users:
        json_compatible_users.append(get_json_from_user(user))

    return JSONResponse(content=json_compatible_users)

@api_router.get("/get_user_by_user_id_debug/{user_id}", include_in_schema=False)
async def get_user_by_user_id(user_id: uuid.UUID) -> JSONResponse:
    session = Session()

    user: User = select_user_by_user_id(session, user_id)

    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    logger.info(f"Got user by user_id: {user=}")
    session.commit()

    json_compatible_user_data = get_json_from_user(user)
    return JSONResponse(content=json_compatible_user_data)


@api_router.get("/get_user_by_username_debug/{username}", include_in_schema=False)
async def get_user_by_username(username: str) -> JSONResponse:
    session = Session()

    user: User = select_user_by_username(session, username)

    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    logger.info(f"Got user by username: {user=}")
    session.commit()

    json_compatible_user_profile_data = jsonable_encoder(user)
    return JSONResponse(content=json_compatible_user_profile_data)


@api_router.get("/get_user_profile_by_user_id_debug/{user_id}", include_in_schema=False)
async def get_user_profile_by_user_id(user_id: uuid.UUID) -> JSONResponse:
    session = Session()

    user_profile: UserProfile = select_user_profile_by_user_id(session, user_id)

    if not user_profile:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    logger.info(f"Got user_profile by user_id: {user_profile=}")
    session.commit()

    json_compatible_user_session_data = get_json_from_user_profile(user_profile)
    return JSONResponse(content=json_compatible_user_session_data)


@api_router.get("/get_user_sessions_by_user_id_debug/{user_id}", include_in_schema=False)
async def get_user_sessions_by_user_id(user_id: uuid.UUID) -> JSONResponse:
    session = Session()

    user_sessions: list[UserSession] = select_user_sessions_by_user_id(session, user_id)

    if not user_sessions:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    logger.info(f"Got user_sessions by user_id: {user_sessions=}")
    session.commit()

    json_compatible_user_sessions: list[dict] = []
    for user_session in user_sessions:
        json_compatible_user_sessions.append(get_json_from_user_session(user_session))

    return JSONResponse(content=json_compatible_user_sessions)






















