"""Import every model here, so Alembic autogenerate can see its table.

Example:
    from app.models.user import User

    __all__ = ["Base", "User"]
"""

from app.core.db import Base

__all__ = ["Base"]
