# FastAPI project template

A [Copier](https://copier.readthedocs.io) template for new FastAPI projects with uv, PostgreSQL (async SQLAlchemy 2 + Alembic), Redis, Celery, SQLAdmin, Docker Compose, ruff, ty, prek and pytest.

Only the `template/` folder is copied into new projects. This README and `copier.yml` stay here.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- [prek](https://github.com/j178/prek), for the Git hooks
- Docker Desktop
- Git

## Create a new project

```bash
uvx copier copy --trust gh:osamahasanone/fastapi_template ~/Desktop/my_project
```

Copier asks for:

- **Project name**: lowercase with underscores, e.g. `my_project`. Also used for the PostgreSQL database, user and password in `.env`, and as the API title.
- **Description**: goes into `pyproject.toml`.
- **Python version**: press Enter to keep `3.14`. The same value is written to `pyproject.toml`, `.python-version` and the `Dockerfile`, so they always match.

`--trust` is needed because the template runs commands after copying the files. Those commands:

1. Run `git init`.
2. Install all packages with `uv add`, always the latest versions.
3. Generate a unique `SECRET_KEY` and `ADMIN_PASSWORD` and write them to `.env`.
4. Install the prek Git hooks.
5. Run ruff to fix and format the code.

Then start the project:

```bash
cd ~/Desktop/my_project
docker compose up -d --build
docker compose exec web uv run pytest
```

Open:

- http://localhost:8000/docs — Swagger UI
- http://localhost:8000/health — returns `{"status": "ok"}` when the database is reachable
- http://localhost:8000/admin — SQLAdmin; log in with `ADMIN_USERNAME` and `ADMIN_PASSWORD` from `.env`

## Add a model

1. Create `app/models/item.py` with a class that inherits from `Base` (from `app.core.db`).
2. Import it in `app/models/__init__.py` and add it to `__all__`, so Alembic can see it.
3. Create and apply the migration:
   ```bash
   docker compose exec web uv run alembic revision --autogenerate -m "create item"
   docker compose exec web uv run alembic upgrade head
   ```
4. Optional: show it in the admin with a `ModelView` registered in `app/admin.py`.

Put Celery tasks in `app/tasks.py`; the worker finds them automatically. Restart it after changes (VS Code task "Celery: restart worker").

## What's in a new project

| File | Purpose |
|---|---|
| `pyproject.toml` | Project metadata, ruff and pytest settings |
| `.env` / `.env.example` | Real local values (never committed) / the list of variables to set (committed) |
| `app/main.py` | Creates the FastAPI app, adds the routes and the admin, closes the DB engine on shutdown |
| `app/core/config.py` | Reads `.env` with pydantic-settings and builds the database URL |
| `app/core/db.py` | Async engine, `SessionDep` dependency, `Base` with constraint naming rules |
| `app/core/celery_app.py` | Creates the Celery app (Redis as broker and result backend) |
| `app/api/` | Routers; `health.py` is the example |
| `app/models/` | SQLAlchemy models |
| `app/admin.py` | SQLAdmin with username/password login |
| `alembic.ini`, `migrations/` | Async Alembic setup; new migrations are dated and formatted by ruff |
| `tests/` | pytest with an async `client` fixture (httpx, no server needed) |
| `Dockerfile`, `.dockerignore` | Image for `web` and `celery` |
| `compose.yaml` | `web` (FastAPI with auto-reload), `celery` (worker), `db` (PostgreSQL), `redis`, with healthchecks |
| `prek.toml` | Checks that run on every commit |
| `.vscode/tasks.json` | Common commands via `Cmd + Shift + P` → Tasks: Run Task |
| `.vscode/settings.json` | Lets Pytest Runner run tests inside the `web` container |
| `.copier-answers.yml` | Your answers, used by `copier update` |

## Change the template

1. Edit files in `template/`. Files ending in `.jinja` can use `{{ project_name }}`, `{{ description }}` and `{{ python_version }}`. Copier removes `.jinja` from their names.
2. Commit and tag a new version:
   ```bash
   git commit -am "Describe the change"
   git tag v1.1.0
   git push --follow-tags
   ```
3. Pull the change into an existing project (run inside that project, with its changes committed):
   ```bash
   uvx copier update --trust
   ```
