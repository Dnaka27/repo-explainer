from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exceptions import AppError, app_error_handler, unhandled_error_handler
from app.routers import analyze

app = FastAPI(title="Graph View API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, unhandled_error_handler)

app.include_router(analyze.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
