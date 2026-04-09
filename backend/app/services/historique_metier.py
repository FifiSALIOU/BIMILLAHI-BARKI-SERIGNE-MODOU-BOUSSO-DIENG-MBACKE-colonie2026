"""Écritures dans la table `historique` — uniquement en complément du métier (non bloquant si échec)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.models import HistoriqueEntry

logger = logging.getLogger(__name__)

_VALID_TYPES = frozenset({"REJET", "DESISTEMENT"})


def append_historique_best_effort(
    db: Session,
    *,
    event_type: str,
    enfant_id: int,
    demande_id: int | None,
    motif: str,
    ajoute_par_id: int,
    desistement_id: int | None = None,
    date_action: datetime | None = None,
) -> None:
    if event_type not in _VALID_TYPES:
        return
    try:
        db.add(
            HistoriqueEntry(
                event_type=event_type,
                enfant_id=int(enfant_id),
                demande_id=int(demande_id) if demande_id is not None else None,
                motif=motif or "",
                date_action=date_action if date_action is not None else datetime.now(timezone.utc),
                ajoute_par_id=int(ajoute_par_id),
                desistement_id=int(desistement_id) if desistement_id is not None else None,
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("historique: écriture ignorée (non bloquant pour le métier)")
