from fastapi import APIRouter

from app.schemas.auth import LoginRequest, LoginResponse, LoginUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    return LoginResponse(
        access_token="mock-jwt-token",
        token_type="bearer",
        expires_in=3600,
        user=LoginUser(id="usr_mock_001", email=payload.email, role="operator"),
    )
