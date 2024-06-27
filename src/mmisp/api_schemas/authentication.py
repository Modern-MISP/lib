from enum import Enum

from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str
    reqiuredPasswordChange: bool


class ChangePasswordResponse(BaseModel):
    successful: bool


class IdentityProviderInfo(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class LoginType(Enum):
    PASSWORD = "password"
    IDENTITY_PROVIDER = "idp"


class StartLoginBody(BaseModel):
    email: str


class PasswordLoginBody(BaseModel):
    email: str
    password: str

class ChangePasswordBody(BaseModel):
    password: str

class ExchangeTokenLoginBody(BaseModel):
    exchangeToken: str


class StartLoginResponse(BaseModel):
    loginType: LoginType
    identityProviders: list[IdentityProviderInfo] = []
