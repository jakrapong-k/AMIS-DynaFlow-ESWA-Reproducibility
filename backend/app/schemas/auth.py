from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    id: str
    email: EmailStr
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: LoginUser
