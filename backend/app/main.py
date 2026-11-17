import logging
import os
import sqlite3
from contextlib import asynccontextmanager, closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator

logger = logging.getLogger(__name__)

Category = Literal[
    "Posible sobrecosto o adición",
    "Retrasos o prórrogas",
    "Posible incumplimiento",
    "Documentación incompleta",
    "Posible fraccionamiento",
    "Otro",
]


class ReportSubmission(BaseModel):
    contract_id: str | None = Field(default=None, max_length=100)
    category: Category
    description: str = Field(min_length=20, max_length=3000)
    reporter_name: str | None = Field(default=None, max_length=120)
    reporter_email: EmailStr | None = None

    @field_validator("contract_id", "reporter_name", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("El campo debe ser texto.")
        normalized = value.strip()
        return normalized or None

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 20:
            raise ValueError("La descripción debe tener al menos 20 caracteres.")
        return normalized


class ReportReceipt(BaseModel):
    id: str
    status: Literal["received"]
    created_at: datetime


def database_path() -> Path:
    configured_path = os.environ.get("REPORTS_DB_PATH")
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return Path(__file__).resolve().parents[1] / "reports.db"


def initialize_database() -> None:
    path = database_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(path, timeout=5)) as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA busy_timeout = 5000")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS reports (
                    id TEXT PRIMARY KEY,
                    contract_id TEXT,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    reporter_name TEXT,
                    reporter_email TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS reports_created_at_idx
                    ON reports (created_at);
                """
            )
            connection.commit()
    except sqlite3.Error:
        logger.exception("Could not initialize the reports database.")
        raise


def allowed_origins() -> list[str]:
    configured = os.environ.get("CORS_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return ["http://localhost:5173", "http://127.0.0.1:5173"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="CaliTransparente Reports API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
)


@app.get("/api/v1/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/api/v1/reports",
    response_model=ReportReceipt,
    status_code=status.HTTP_201_CREATED,
    tags=["reports"],
)
def create_report(submission: ReportSubmission) -> ReportReceipt:
    receipt = ReportReceipt(
        id=str(uuid4()),
        status="received",
        created_at=datetime.now(timezone.utc),
    )
    path = database_path()

    try:
        with closing(sqlite3.connect(path, timeout=5)) as connection:
            connection.execute("PRAGMA busy_timeout = 5000")
            connection.execute(
                """
                INSERT INTO reports (
                    id, contract_id, category, description,
                    reporter_name, reporter_email, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    receipt.id,
                    submission.contract_id,
                    submission.category,
                    submission.description,
                    submission.reporter_name,
                    str(submission.reporter_email) if submission.reporter_email else None,
                    receipt.created_at.isoformat(),
                ),
            )
            connection.commit()
    except sqlite3.Error as error:
        logger.exception("Could not save report %s.", receipt.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible guardar el reporte. Intente de nuevo más tarde.",
        ) from error

    return receipt
