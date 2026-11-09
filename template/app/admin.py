"""SQLAdmin at /admin. Log in with ADMIN_USERNAME and ADMIN_PASSWORD from .env."""

import secrets

from fastapi import FastAPI
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings
from app.core.db import engine


def _matches(given: object, expected: str) -> bool:
    return secrets.compare_digest(str(given or "").encode(), expected.encode())


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        if _matches(form.get("username"), settings.admin_username) and _matches(
            form.get("password"), settings.admin_password
        ):
            request.session["admin"] = True
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("admin"))


def setup_admin(app: FastAPI) -> Admin:
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.secret_key),
    )
    # Register model views here, e.g. admin.add_view(UserAdmin)
    return admin
