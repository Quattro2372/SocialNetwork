from sqlalchemy import create_engine, Column, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    encoded_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, default='')
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    sessions = relationship('UserSession', back_populates='user', cascade="all, delete-orphan")
    profile = relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"""
            <User>(
            user_id='{self.user_id}', 
            username='{self.username}', 
            encoded_password='{self.encoded_password}', 
            email='{self.email}', 
            phone_number='{self.phone_number}
            created_at='{self.created_at}',
            updated_at='{self.updated_at}')
        """


class UserSession(Base):
    __tablename__ = 'user_sessions'

    token = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    terminated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    active_until = Column(DateTime(timezone=True), nullable=False)

    user = relationship('User', back_populates='sessions')

    def __repr__(self):
        return f"""
            <UserSession>(
            token='{self.token}',
            user_id='{self.user_id}',
            terminated='{self.terminated}',
            created_at='{self.created_at}',
            active_until='{self.active_until}')
        """


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True, nullable=False)
    name = Column(String, nullable=False, default='')
    surname = Column(String, nullable=False, default='')
    date_of_birth = Column(String, nullable=False, default='')
    photo_url = Column(String, nullable=False, default='')

    user = relationship('User', back_populates='profile')

    def __repr__(self):
        return f"""
            <UserProfile>(
            user_id='{self.user_id}', 
            name='{self.name}', 
            surname='{self.surname}', 
            date_of_birth='{self.date_of_birth}',
            photo_url='{self.photo_url}')
        """