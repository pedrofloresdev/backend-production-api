"""improve schema

Revision ID: a1b2c3d4e5f6
Revises: d41c395aa420
Create Date: 2026-05-13 00:00:00.000000

Changes:
- users: created_at / updated_at → TIMESTAMPTZ (timezone-aware)
- posts: title / content → NOT NULL
- posts: owner_id → NOT NULL, ON DELETE CASCADE, index added
- posts: created_at / updated_at audit columns added
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "d41c395aa420"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- users: make timestamps timezone-aware ---
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        nullable=False,
        server_default=sa.text("now()"),
    )
    op.alter_column(
        "users",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        nullable=False,
        server_default=sa.text("now()"),
    )

    # --- posts: title / content NOT NULL ---
    op.alter_column("posts", "title", existing_type=sa.String(), nullable=False)
    op.alter_column("posts", "content", existing_type=sa.String(), nullable=False)

    # --- posts: owner_id NOT NULL + recreate FK with CASCADE + index ---
    op.drop_constraint("posts_owner_id_fkey", "posts", type_="foreignkey")
    op.alter_column("posts", "owner_id", existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key(
        "posts_owner_id_fkey",
        "posts",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index("ix_posts_owner_id", "posts", ["owner_id"], unique=False)

    # --- posts: add audit timestamps ---
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "updated_at")
    op.drop_column("posts", "created_at")
    op.drop_index("ix_posts_owner_id", table_name="posts")
    op.drop_constraint("posts_owner_id_fkey", "posts", type_="foreignkey")
    op.create_foreign_key(
        "posts_owner_id_fkey", "posts", "users", ["owner_id"], ["id"]
    )
    op.alter_column("posts", "owner_id", existing_type=sa.Integer(), nullable=True)
    op.alter_column("posts", "content", existing_type=sa.String(), nullable=True)
    op.alter_column("posts", "title", existing_type=sa.String(), nullable=True)
    op.alter_column(
        "users",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
        nullable=True,
        server_default=None,
    )
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
        nullable=True,
        server_default=None,
    )
