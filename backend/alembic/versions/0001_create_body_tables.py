"""create body photo tables

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "body_photos",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("view", sa.String(length=16), nullable=False),
        sa.Column("file_url", sa.String(length=1024), nullable=False),
        sa.Column("distance_cm", sa.Integer(), nullable=True),
        sa.Column("camera_height_cm", sa.Integer(), nullable=True),
        sa.Column("lighting", sa.String(length=128), nullable=True),
        sa.Column("clothing", sa.String(length=128), nullable=True),
        sa.Column("pose_hint", sa.String(length=128), nullable=True),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("pose_keypoints", sa.JSON(), nullable=True),
        sa.Column("segmentation_key", sa.String(length=1024), nullable=True),
    )

    op.create_table(
        "body_comparisons",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("from_photo_id", sa.String(length=36), sa.ForeignKey("body_photos.id"), nullable=False),
        sa.Column("to_photo_id", sa.String(length=36), sa.ForeignKey("body_photos.id"), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("body_comparisons")
    op.drop_table("body_photos")
    op.drop_table("users")
