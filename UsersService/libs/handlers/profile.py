from datetime import datetime, timedelta

from fastapi import APIRouter, Response, status
import logging
import uuid

from models.models import (
    GetUserByIDRequest,
    GetUserByUsernameRequest,
    GetUserResponse,
    UserData,
    UserUpdateRequest,
    UserUpdateResponse,
    UserUpdateData,
)
from libs.database.queries.queries import (
    add_user_to_users_table,
    add_user_session_to_user_sessions_table,
    add_user_profile_to_user_profiles_table,
    select_user_by_username,
    select_user_session_by_token,
    select_user_profile_by_user_id,
    select_user_by_user_id,
)
from models.database_models import User, UserSession, UserProfile
from libs.database.database_management import Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.post("/get_user_by_username", status_code=200, response_model=GetUserResponse, responses={400: {
    "model": GetUserResponse}})
async def get_user_by_username(body: GetUserByUsernameRequest, response: Response) -> GetUserResponse:
    session = Session()

    username: str = body.username
    logger.info(f"Getting user with username: {username=}")

    if not username:
        logger.info(f"Got invalid Username: {username}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return GetUserResponse(error="Invalid Username")

    user_from_db: User = select_user_by_username(session, username)
    logger.info(f"Got user by username: {user_from_db=}")
    if user_from_db is None:
        logger.info("No user exists with such username")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return GetUserResponse(error="User with such username does not exist")

    user_profile_from_db: UserProfile = select_user_profile_by_user_id(session, user_from_db.user_id)

    if not user_profile_from_db:
        logger.info("No user_profile exists with such id")
        raise RuntimeError("User exists in users table, but not in user_profiles table. Invariant failed")

    user_data: UserData = UserData(
        user_id=user_from_db.user_id,
        username=user_from_db.username,
        name=user_profile_from_db.name,
        surname=user_profile_from_db.surname,
        date_of_birth=user_profile_from_db.date_of_birth,
        email=user_from_db.email,
        phone_number=user_from_db.phone_number,
        photo_url=user_profile_from_db.photo_url,
        created_at=int(user_from_db.created_at.timestamp()),
        updated_at=int(user_from_db.updated_at.timestamp()),
    )


    logger.info(f"Got user_data:, {user_data=}")
    get_user_response: GetUserResponse = GetUserResponse(user_data=user_data)

    logger.info(f"Successfully handled get_user_by_username request {user_data=}")
    session.commit()
    return get_user_response


@api_router.post("/get_user_by_id", status_code=200, response_model=GetUserResponse, responses={400: {
    "model": GetUserResponse}})
async def get_user_by_id(body: GetUserByIDRequest, response: Response) -> GetUserResponse:
    session = Session()

    user_id: uuid.UUID = body.user_id
    logger.info(f"Getting user with user_id: {user_id=}")

    if not user_id:
        logger.info(f"Got invalid user_id: {user_id}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return GetUserResponse(error="Invalid user_id")

    user_from_db: User = select_user_by_user_id(session, user_id)
    logger.info(f"Got user by user_id: {user_from_db=}")
    if user_from_db is None:
        logger.info("No user exists with such user_id")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return GetUserResponse(error="User with such user_id does not exist")

    user_profile_from_db: UserProfile = select_user_profile_by_user_id(session, user_id)

    if not user_profile_from_db:
        logger.info("No user_profile exists with such id")
        raise RuntimeError("User exists in users table, but not in user_profiles table. Invariant failed")

    user_data: UserData = UserData(
        user_id=user_from_db.user_id,
        username=user_from_db.username,
        name=user_profile_from_db.name,
        surname=user_profile_from_db.surname,
        date_of_birth=user_profile_from_db.date_of_birth,
        email=user_from_db.email,
        phone_number=user_from_db.phone_number,
        photo_url=user_profile_from_db.photo_url,
        created_at=int(user_from_db.created_at.timestamp()),
        updated_at=int(user_from_db.updated_at.timestamp()),
    )

    logger.info(f"Got user_data:, {user_data=}")
    get_user_response: GetUserResponse = GetUserResponse(user_data=user_data)

    logger.info(f"Successfully handled get_user_by_id request {user_data=}")
    session.commit()
    return get_user_response


@api_router.post("/update_user", status_code=200, response_model=UserUpdateResponse, responses={400: {
    "model": UserUpdateResponse}})
async def update_user(body: UserUpdateRequest, response: Response) -> UserUpdateResponse:
    session = Session()

    user_id: uuid.UUID = body.user_id
    logger.info(f"Updating user with user_id: {user_id=}")

    if not user_id:
        logger.info(f"Got invalid user_id: {user_id}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserUpdateResponse(error="Invalid user_id")

    user_from_db: User = select_user_by_user_id(session, user_id)
    logger.info(f"Got user by user_id: {user_from_db=}")
    if user_from_db is None:
        logger.info("No user exists with such user_id")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserUpdateResponse(error="User with such user_id does not exist")

    user_profile_from_db: UserProfile = select_user_profile_by_user_id(session, user_id)

    if not user_profile_from_db:
        logger.info("No user_profile exists with such id")
        raise RuntimeError("User exists in users table, but not in user_profiles table. Invariant failed")

    user_update_data: UserUpdateData = body.user_update_data

    if user_update_data.name is not None:
        user_profile_from_db.name = user_update_data.name
    if user_update_data.surname is not None:
        user_profile_from_db.surname = user_update_data.surname
    if user_update_data.date_of_birth is not None:
        user_profile_from_db.date_of_birth = user_update_data.date_of_birth
    if user_update_data.photo_url is not None:
        user_profile_from_db.photo_url = user_update_data.photo_url

    if user_update_data.email is not None:
        user_from_db.email = user_update_data.email
    if user_update_data.phone_number is not None:
        user_from_db.phone_number = user_update_data.phone_number

    user_from_db.updated_at = datetime.now()

    session.commit()
    logger.info(f"Successfully handled update_user request {user_from_db=}, {user_profile_from_db=}")
    return UserUpdateResponse()


