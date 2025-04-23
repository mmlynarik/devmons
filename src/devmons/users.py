from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    email: str
    password: str
    salt: str


@dataclass
class UserCreate:
    email: str
    password: str
    salt: str


@dataclass
class UserCreated:
    id: int
    email: str


@dataclass
class UserAlreadyExists(Exception):
    pass
