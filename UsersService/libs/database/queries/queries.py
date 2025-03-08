import uuid

from libs.database.database_management import Session
from models.database_models import User, UserSession, UserProfile


def add_user_to_users_table(session, user: User) -> None:
    session.add(user)

def add_user_session_to_user_sessions_table(session, user_session: UserSession) -> None:
    session.add(user_session)

def add_user_profile_to_user_profiles_table(session, user_profile: UserProfile) -> None:
    session.add(user_profile)


def select_all_users(session) -> list[User]:
    users: list[User] = session.query(User).all()
    return users

def select_user_by_username(session, username: str) -> None | User:
    users: list[User] = session.query(User).filter_by(username=username).all()

    if len(users) > 1:
        raise RuntimeError("More than one user with same username in database. Invariant failed")

    return users[0] if users else None

def select_user_by_user_id(session, user_id: uuid.UUID) -> None | User:
    users: list[User] = session.query(User).filter_by(user_id=user_id).all()

    if len(users) > 1:
        raise RuntimeError("More than one user with same user_id in database. Invariant failed")

    return users[0] if users else None


def select_user_profile_by_user_id(session, user_id: uuid.UUID) -> None | UserProfile:
    user_profiles: list[UserProfile] = session.query(UserProfile).filter_by(user_id=user_id).all()

    if len(user_profiles) > 1:
        raise RuntimeError("More than one user_profile with same user_id in database. Invariant failed")

    return user_profiles[0] if user_profiles else None


def select_user_sessions_by_user_id(session, user_id: uuid.UUID) -> None | UserSession:
    user_sessions: list[UserSession] = session.query(UserSession).filter_by(user_id=user_id).all()

    return user_sessions if user_sessions else None

def select_user_session_by_token(session, token: uuid.UUID) -> None | UserSession:
    user_sessions: list[UserSession] = session.query(UserSession).filter_by(token=token).all()

    if len(user_sessions) > 1:
        raise RuntimeError("More than one user_session with same token in database. Invariant failed")

    return user_sessions[0] if user_sessions else None