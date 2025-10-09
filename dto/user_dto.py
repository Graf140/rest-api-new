from dataclasses import dataclass

#посложнее уже
@dataclass
class AddLogUserDTO:
    username: str
    password: str

@dataclass
class LogUserDTO:
    username: str
    password: str


@dataclass
class GenJWTDTO:
    user_id: int
    username: str

@dataclass
class GetUserProfileDTO:
    user_id: int