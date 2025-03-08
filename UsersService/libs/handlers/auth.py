from datetime import datetime, timedelta

from fastapi import APIRouter, Response, status
import logging
import uuid

from models.models import (
    AuthResponseData,
    AuthWithUsernameData,
    AuthWithTokenData,
    AuthWithUsernameRequest,
    AuthWithTokenRequest,
    AuthResponse,
)
from libs.utils.password import check_password, encode_password
from libs.database.queries.queries import (
    add_user_to_users_table,
    add_user_session_to_user_sessions_table,
    add_user_profile_to_user_profiles_table,
    select_user_by_username,
    select_user_session_by_token,
)
from models.database_models import User, UserSession, UserProfile
from libs.database.database_management import Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.post("/auth_with_username", status_code=200, response_model=AuthResponse, responses={400: {
    "model": AuthResponse}, 401: {
    "model": AuthResponse}})
async def auth_with_username(body: AuthWithUsernameRequest, response: Response) -> AuthResponse:
    session = Session()
    auth_data: AuthWithUsernameData = body.auth_data

    username: str = auth_data.username
    password: str = auth_data.password
    logger.info(f"Authorizing user with username: {username=} {password=}")

    if not username:
        logger.info(f"Got invalid Username: {username}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AuthResponse(error="Invalid Username")

    user_from_db: User = select_user_by_username(session, username)
    logger.info(f"Got user by username: {user_from_db=}")
    if user_from_db is None:
        logger.info("No user exists with such username")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AuthResponse(error="User with such username does not exist")

    if not check_password(password, user_from_db.encoded_password):
        logger.info("Unsuccessful auth attempt")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return AuthResponse(error="Wrong password")

    session_token: uuid.UUID = uuid.uuid4()

    user_session: UserSession = UserSession(token=session_token, user_id=user_from_db.user_id, created_at=datetime.now(), active_until=(datetime.now() + timedelta(days=2)))

    add_user_session_to_user_sessions_table(session, user_session)
    logger.info(f"Added user_session to user_sessions table, {user_session=}")

    auth_response_data: AuthResponseData = AuthResponseData(token=session_token, user_id=user_from_db.user_id)
    auth_response: AuthResponse = AuthResponse(auth_response_data=auth_response_data)

    logger.info(f"Successfully handled auth with username request {user_session=}")
    session.commit()
    return auth_response


@api_router.post("/auth_with_token", status_code=200, response_model=AuthResponse, responses={400: {
    "model": AuthResponse}, 401: {
    "model": AuthResponse}})
async def auth_with_token(body: AuthWithTokenRequest, response: Response) -> AuthResponse:
    session = Session()
    auth_data: AuthWithTokenData = body.auth_data

    session_token: str = auth_data.token
    logger.info(f"Authorizing with token: {session_token=}")

    if not session_token:
        logger.info(f"Got invalid authorization token: {session_token}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AuthResponse(error="Invalid token")

    session_from_db = select_user_session_by_token(session, session_token)
    logger.info(f"Got session by token: {session_from_db=}")
    if session_from_db is None:
        logger.info("No session exists with such token")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return AuthResponse(error="No session with such token exists")

    if session_from_db.terminated:
        logger.info("Session was terminated")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return AuthResponse(error="Session was terminated")

    if datetime.now(session_from_db.active_until.tzinfo) > session_from_db.active_until:
        logger.info("Session expired")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return AuthResponse(error="Session expired")

    auth_response_data: AuthResponseData = AuthResponseData(user_id=session_from_db.user_id)
    auth_response: AuthResponse = AuthResponse(auth_response_data=auth_response_data)

    logger.info(f"Successfully handled auth with token request {session_from_db=}")
    session.commit()
    return auth_response






















