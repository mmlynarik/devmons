from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    email: str | None
    password: str | None
    salt: str | None
    github_id: int | None
    github_name: str | None


@dataclass
class UserCreate:
    email: str | None = None
    password: str | None = None
    salt: str | None = None
    github_id: int | None = None
    github_name: str | None = None


@dataclass
class UserCreated:
    id: int


@dataclass
class UserAlreadyExists(Exception):
    pass
