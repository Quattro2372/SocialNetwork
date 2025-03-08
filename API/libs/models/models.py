import uuid
from pydantic import BaseModel
from typing import Optional

class RegistrationData(BaseModel):
    username: str
    email: str
    password: str

class AuthWithTokenData(BaseModel):
    token: uuid.UUID

class AuthWithUsernameData(BaseModel):
    username: str
    password: str

class AuthResponseData(BaseModel):
    token: Optional[uuid.UUID] = None
    user_id: uuid.UUID

class UserData(BaseModel):
    user_id: uuid.UUID
    username: str
    name: Optional[str] = None
    surname: Optional[str] = None
    date_of_birth: Optional[str] = None
    email: str
    phone_number: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: int
    updated_at: int

class UserUpdateData(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    photo_url: Optional[str] = None


class RegistrationRequest(BaseModel):
    registration_data: RegistrationData

class RegistrationResponse(BaseModel):
    error: Optional[str] = None
    auth_response_data: Optional[AuthResponseData] = None


class AuthWithUsernameRequest(BaseModel):
    auth_data: AuthWithUsernameData

class AuthWithTokenRequest(BaseModel):
    auth_data: AuthWithTokenData

class AuthResponse(BaseModel):
    error: Optional[str] = None
    auth_response_data: Optional[AuthResponseData] = None


class UserUpdateRequest(BaseModel):
    user_id: uuid.UUID
    user_update_data: UserUpdateData

class UserUpdateResponse(BaseModel):
    error: Optional[str] = None


class GetUserByIDRequest(BaseModel):
    user_id: uuid.UUID

class GetUserByUsernameRequest(BaseModel):
    username: str

class GetUserResponse(BaseModel):
    error: Optional[str] = None
    user_data: Optional[UserData] = None
