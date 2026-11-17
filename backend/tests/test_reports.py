import sqlite3

from fastapi.testclient import TestClient

from app.main import app


def test_create_report_persists_submission(tmp_path, monkeypatch):
    database = tmp_path / "reports.db"
    monkeypatch.setenv("REPORTS_DB_PATH", str(database))
    payload = {
        "contract_id": "SECOP-II-12345",
        "category": "Posible sobrecosto o adición",
        "description": "Se observó una adición que requiere verificar los soportes del proceso.",
        "reporter_name": "Ciudadanía",
        "reporter_email": "ciudadania@example.com",
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/reports", json=payload)

    assert response.status_code == 201
    receipt = response.json()
    assert receipt["status"] == "received"
    assert receipt["id"]
    assert receipt["created_at"]

    with sqlite3.connect(database) as connection:
        saved = connection.execute(
            "SELECT contract_id, category, description, reporter_name, reporter_email "
            "FROM reports WHERE id = ?",
            (receipt["id"],),
        ).fetchone()

    assert saved == (
        payload["contract_id"],
        payload["category"],
        payload["description"],
        payload["reporter_name"],
        payload["reporter_email"],
    )


def test_create_report_allows_optional_fields_to_be_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("REPORTS_DB_PATH", str(tmp_path / "reports.db"))
    payload = {
        "contract_id": " ",
        "category": "Otro",
        "description": "Hay hechos que deben verificarse dentro de este contrato.",
        "reporter_name": " ",
        "reporter_email": None,
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/reports", json=payload)

    assert response.status_code == 201
    with sqlite3.connect(tmp_path / "reports.db") as connection:
        saved = connection.execute(
            "SELECT contract_id, reporter_name, reporter_email FROM reports"
        ).fetchone()
    assert saved == (None, None, None)


def test_create_report_rejects_invalid_input(tmp_path, monkeypatch):
    monkeypatch.setenv("REPORTS_DB_PATH", str(tmp_path / "reports.db"))
    invalid_payloads = [
        {
            "category": "Categoria desconocida",
            "description": "Una descripción suficientemente larga para la validación.",
        },
        {
            "category": "Otro",
            "description": "corta",
        },
        {
            "category": "Otro",
            "description": "Una descripción suficientemente larga para la validación.",
            "reporter_email": "correo-invalido",
        },
    ]

    with TestClient(app) as client:
        for payload in invalid_payloads:
            response = client.post("/api/v1/reports", json=payload)
            assert response.status_code == 422


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
