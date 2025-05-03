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
class UserCreateByEmail:
    email: str
    password: str
    salt: str


@dataclass
class UserCreateByGithub:
    github_id: int
    github_name: str


@dataclass
class UserCreated:
    id: int


@dataclass
class UserAlreadyExists(Exception):
    pass
