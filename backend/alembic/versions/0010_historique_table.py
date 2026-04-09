"""Table historique (journal rejet / désistement).

Revision ID: 0010_historique_table
Revises: 0009_users_must_chg_pwd
Create Date: 2026-04-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0010_historique_table"
down_revision = "0009_users_must_chg_pwd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "historique",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("enfant_id", sa.BigInteger(), nullable=False),
        sa.Column("demande_id", sa.BigInteger(), nullable=True),
        sa.Column("motif", sa.Text(), nullable=False, server_default=""),
        sa.Column("date_action", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ajoute_par_id", sa.BigInteger(), nullable=True),
        sa.Column("desistement_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["enfant_id"], ["enfants.id"]),
        sa.ForeignKeyConstraint(["demande_id"], ["demandes.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["ajoute_par_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_historique_date_action", "historique", ["date_action"])
    op.create_index("ix_historique_enfant_id", "historique", ["enfant_id"])
    op.create_index("ix_historique_demande_id", "historique", ["demande_id"])


def downgrade() -> None:
    op.drop_index("ix_historique_demande_id", table_name="historique")
    op.drop_index("ix_historique_enfant_id", table_name="historique")
    op.drop_index("ix_historique_date_action", table_name="historique")
    op.drop_table("historique")
