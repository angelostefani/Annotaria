# Repository Guidelines

## Project Structure & Module Organization
- `main.py`: FastAPI entrypoint; mounts `static/` and `image_data/`, includes routers.
- `database.py`: SQLAlchemy engine/session; reads `DATABASE_URL` from `.env`.
- `models.py`: ORM models (users, images, questions, labels, annotations, …).
- `routers/`: FastAPI routers grouped by domain (`images.py`, `questions.py`, `ui.py`, …).
- `schemas/`: Pydantic models for requests/responses.
- `templates/`, `static/`: Jinja2 views and assets.
- `docs/`: API and setup docs; check `docs/API_REST.md` and `docs/Setup.md`.
- `image_data/`: Image source folder (configurable via `IMAGE_DIR`).

## Build, Test, and Development Commands
- Create env: `python -m venv .venv && source .venv/bin/activate` (Windows: ` .venv\\Scripts\\activate`).
- Install deps: `pip install -r requirements.txt`.
- Run API (dev): `uvicorn main:app --reload`.
- Run API (custom host/port): `uvicorn main:app --host 0.0.0.0 --port 8000`.
- Example `.env`:
  - `DATABASE_URL=sqlite:///./annotaria.db`
  - `IMAGE_DIR=./image_data`
  - `SECRET_KEY=change-me`

## Docker & Containers
- Repo files: `Dockerfile` and `docker-compose.yml` are included.
- Build image: `docker build -t annotaria .`.
- Run (SQLite): `docker run --rm -p 8000:8000 --env-file .env -v "$PWD/image_data:/app/image_data" annotaria`.
- Compose (PostgreSQL): `docker compose up --build` (uses `DATABASE_URL` for Postgres service).
- Example `Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  ENV IMAGE_DIR=/app/image_data
  CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
  ```
- `docker-compose.yml` (PostgreSQL):
  ```yaml
  services:
    db:
      image: postgres:16
      environment:
        POSTGRES_DB: annotaria
        POSTGRES_USER: annotaria
        POSTGRES_PASSWORD: annotaria
      volumes:
        - db_data:/var/lib/postgresql/data
    app:
      build: .
      depends_on: [db]
      environment:
        DATABASE_URL: postgresql://annotaria:annotaria@db:5432/annotaria
        IMAGE_DIR: /app/image_data
        SECRET_KEY: change-me
      volumes:
        - ./image_data:/app/image_data
      ports: ["8000:8000"]
  volumes: { db_data: {} }
  ```

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indentation, type hints for public functions.
- Files: snake_case (`image_types.py`), classes: PascalCase (`ImageType`).
- Routers: one domain per file in `routers/`; path operations prefixed accordingly.
- Schemas: mirror models; keep request/response objects explicit.
- Templates: keep logic minimal; prefer server-side in routers/schemas.

## Testing Guidelines
- Framework: pytest (tests folder not yet present).
- Structure: `tests/` with files named `test_*.py` per router/model.
- Run: `pytest -q` (ensure app imports without side effects).
- Focus: router responses, model relations, EXIF parsing, auth flows.

## Commit & Pull Request Guidelines
- Style: Prefer Conventional Commits (`feat:`, `fix:`, `docs:`). Short imperative subject; optional scope (`feat(images): upload EXIF`).
- Branches: `feature/<short-name>` or `fix/<short-name>`.
- PRs: clear description, linked issues, steps to test, screenshots for UI (`templates/`), and DB impact notes. Keep changes focused; include migration notes if models change.

## Security & Configuration Tips
- Never commit real secrets or `annotaria.db` from production.
- CORS: `ALLOWED_ORIGINS` (`.env`) controls origins; default is permissive for dev.
- Default DB is SQLite; use PostgreSQL in production via `DATABASE_URL`.
