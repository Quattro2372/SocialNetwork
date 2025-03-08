from datetime import datetime, timedelta

from fastapi import APIRouter, Response, status
import logging
import uuid

from models.models import (
    AuthResponseData,
    RegistrationRequest,
    RegistrationData,
    RegistrationResponse,
)
from libs.utils.validators import validate_email, validate_password
from libs.utils.password import encode_password
from libs.database.queries.queries import (
    add_user_to_users_table,
    add_user_session_to_user_sessions_table,
    add_user_profile_to_user_profiles_table,
    select_user_by_username,
)
from models.database_models import User, UserSession, UserProfile
from libs.database.database_management import Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.post("/register_user", status_code=200, response_model=RegistrationResponse, responses={400: {
    "model": RegistrationResponse}})
async def register_user(body: RegistrationRequest, response: Response) -> RegistrationResponse:
    session = Session()
    registration_data: RegistrationData = body.registration_data

    username: str = registration_data.username
    email: str = registration_data.email
    password: str = registration_data.password
    logger.info(f"Registering user: {username=} {email=}")

    if not username:
        logger.info(f"Got invalid Username: {username}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return RegistrationResponse(error="Invalid Username")

    if not validate_password(password):
        logger.info(f"Got invalid Password: {password}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return RegistrationResponse(error="Password does not satisfy requirements")

    if not validate_email(email):
        logger.info(f"Got invalid Email: {email}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return RegistrationResponse(error="Invalid Email")

    user_from_db: User = select_user_by_username(session, username)
    logger.info(f"Got user by username: {user_from_db=}")
    if user_from_db is not None:
        logger.info("Got user with such username")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return RegistrationResponse(error="User with such username already exists")

    encoded_password: str = encode_password(password)
    logger.info(f"Got encoded password: {encoded_password=}")

    user_id: uuid.UUID = uuid.uuid4()
    session_token: uuid.UUID = uuid.uuid4()

    user: User = User(user_id=user_id, username=username, encoded_password=encoded_password, email=email, created_at=datetime.now(), updated_at=datetime.now())
    user_session: UserSession = UserSession(token=session_token, user_id=user_id, created_at=datetime.now(), active_until=(datetime.now() + timedelta(days=2)))
    user_profile = UserProfile(user_id=user_id)

    add_user_to_users_table(session, user)
    logger.info(f"Added user to users table, {user=}")
    add_user_session_to_user_sessions_table(session, user_session)
    logger.info(f"Added user_session to user_sessions table, {user_session=}")
    add_user_profile_to_user_profiles_table(session, user_profile)
    logger.info(f"Added user_profile to user_profiles table, {user_profile=}")

    auth_response_data: AuthResponseData = AuthResponseData(token=session_token, user_id=user_id)
    registration_response: RegistrationResponse = RegistrationResponse(auth_response_data=auth_response_data)

    logger.info(f"Successfully handled registration request {user=}")
    session.commit()
    return registration_response






















