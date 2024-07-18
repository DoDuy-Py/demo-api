from sqlalchemy import Column, Integer, String, Float, BigInteger, Boolean, ForeignKey, Table
from core.settings import Base
from sqlalchemy.orm import relationship, declarative_base

user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    is_activate = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    roles = relationship('Role', secondary=user_roles, back_populates='users')

    accounts = relationship("UserLogin", back_populates="user")


class UserLogin(Base):
    __tablename__ = "users_login"

    id = id = Column(Integer, primary_key=True, index=True)
    account = Column(String, unique=True)
    password = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="accounts")

    is_deleted = Column(Boolean, default=False)


class WaterQuality(Base):
    __tablename__ = "water_quality"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    ph_level = Column(Float)
    temperature = Column(Float)
    turbidity = Column(Float)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    users = relationship('User', secondary=user_roles, back_populates='roles')
