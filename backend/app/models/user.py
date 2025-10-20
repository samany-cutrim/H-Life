from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    body_photos: Mapped[list["BodyPhoto"]] = relationship(back_populates="user")
    body_comparisons: Mapped[list["BodyComparison"]] = relationship(back_populates="user")


from app.models.body import BodyPhoto, BodyComparison  # noqa: E402  circular
