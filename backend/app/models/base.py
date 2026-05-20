from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseModelPlaceholder:
    """Placeholder base model for MVP skeleton.

    This module intentionally avoids any real database connections.
    """

    created_at: datetime
    updated_at: datetime | None = None
