from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    code = "INTERNAL_ERROR"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidUrlError(AppError):
    code = "INVALID_URL"
    status_code = status.HTTP_400_BAD_REQUEST


class RepoNotFoundError(AppError):
    code = "REPO_NOT_FOUND"
    status_code = status.HTTP_404_NOT_FOUND


class GithubRateLimitError(AppError):
    code = "GITHUB_RATE_LIMIT"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class GeminiTimeoutError(AppError):
    code = "GEMINI_TIMEOUT"
    status_code = status.HTTP_504_GATEWAY_TIMEOUT


class GeminiApiError(AppError):
    code = "GEMINI_ERROR"
    status_code = status.HTTP_502_BAD_GATEWAY


class GeminiInvalidResponseError(AppError):
    code = "GEMINI_INVALID_RESPONSE"
    status_code = status.HTTP_502_BAD_GATEWAY


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Erro interno inesperado."}},
    )
