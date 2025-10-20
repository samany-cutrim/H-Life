from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class BodyPhoto(Base):
    __tablename__ = "body_photos"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    view: Mapped[str] = mapped_column(String(16), nullable=False)
    file_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    distance_cm: Mapped[int | None] = mapped_column(nullable=True)
    camera_height_cm: Mapped[int | None] = mapped_column(nullable=True)
    lighting: Mapped[str | None] = mapped_column(String(128))
    clothing: Mapped[str | None] = mapped_column(String(128))
    pose_hint: Mapped[str | None] = mapped_column(String(128))
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    pose_keypoints: Mapped[dict | None] = mapped_column(JSON, default=None)
    segmentation_key: Mapped[str | None] = mapped_column(String(1024))

    user: Mapped["User"] = relationship(back_populates="body_photos")
    comparisons_from: Mapped[list["BodyComparison"]] = relationship(
        back_populates="from_photo", foreign_keys="BodyComparison.from_photo_id"
    )
    comparisons_to: Mapped[list["BodyComparison"]] = relationship(
        back_populates="to_photo", foreign_keys="BodyComparison.to_photo_id"
    )


class BodyComparison(Base):
    __tablename__ = "body_comparisons"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    from_photo_id: Mapped[str] = mapped_column(ForeignKey("body_photos.id"), nullable=False)
    to_photo_id: Mapped[str] = mapped_column(ForeignKey("body_photos.id"), nullable=False)
    result: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="body_comparisons")
    from_photo: Mapped[BodyPhoto] = relationship(
        back_populates="comparisons_from", foreign_keys=[from_photo_id]
    )
    to_photo: Mapped[BodyPhoto] = relationship(
        back_populates="comparisons_to", foreign_keys=[to_photo_id]
    )


from app.models.user import User  # noqa: E402
