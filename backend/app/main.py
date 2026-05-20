from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.schemas.common import ErrorDetail, ErrorResponse

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(api_router, prefix=settings.api_prefix)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    error_payload = ErrorResponse(
        error=ErrorDetail(
            code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            details=None,
        )
    )
    return JSONResponse(status_code=exc.status_code, content=error_payload.model_dump())
