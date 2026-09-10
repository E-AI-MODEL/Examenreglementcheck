from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path
from typing import Any


def _date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assess_actuality(
    root: Path,
    sources: list[dict],
    candidates: list[dict],
    *,
    as_of: str,
    exam_year: int | None,
    school_year: str | None,
) -> dict[str, Any]:
    today = _date(as_of) or date.today()
    used_ids = {candidate.get("source_id") for candidate in candidates}
    rows = []
    for source in sources:
        source_id = source.get("id")
        if source_id not in used_ids:
            continue
        reasons = []
        integrity = "not_checked"
        content_path = source.get("original_path") or source.get("content_path")
        if content_path:
            path = root / content_path
            if not path.is_file():
                integrity = "missing"
                reasons.append("source_file_missing")
            else:
                expected = source.get("content_hash") or source.get("sha256")
                integrity = "valid" if expected and _hash(path) == expected else "mismatch"
                if integrity != "valid":
                    reasons.append("source_hash_mismatch")
        else:
            reasons.append("source_file_not_registered")
        valid_from = _date(source.get("valid_from"))
        valid_to = _date(source.get("valid_to"))
        if valid_from and today < valid_from:
            reasons.append("not_yet_valid")
        if valid_to and today > valid_to:
            reasons.append("expired")
        if exam_year and source.get("exam_year") not in (None, exam_year):
            reasons.append("exam_year_mismatch")
        if school_year and source.get("school_year") not in (None, school_year):
            reasons.append("school_year_mismatch")
        if source.get("fetch_status") != "retrieved":
            reasons.append("not_retrieved")
        retrieved = _date(source.get("retrieved_at"))
        age_days = (today - retrieved).days if retrieved else None
        if retrieved is None:
            reasons.append("retrieval_date_missing")
        status = "current_in_snapshot" if not reasons else "requires_review"
        rows.append({
            "source_id": source_id,
            "title": source.get("title"),
            "status": status,
            "reasons": reasons,
            "retrieved_at": source.get("retrieved_at"),
            "snapshot_age_days": age_days,
            "valid_from": source.get("valid_from"),
            "valid_to": source.get("valid_to"),
            "exam_year": source.get("exam_year"),
            "school_year": source.get("school_year"),
            "integrity": integrity,
            "resolved_url": source.get("resolved_url") or source.get("url"),
            "production_approved": bool(source.get("production_approved")),
        })
    return {
        "status": "complete",
        "scope": "stored_source_snapshot",
        "as_of": today.isoformat(),
        "live_web_check_performed": False,
        "sources": rows,
        "summary": {
            "checked": len(rows),
            "current_in_snapshot": sum(row["status"] == "current_in_snapshot" for row in rows),
            "requires_review": sum(row["status"] != "current_in_snapshot" for row in rows),
        },
        "limitation": (
            "De controle valideert versievelden, toepassingsjaar en lokale bronintegriteit binnen de "
            "opgeslagen snapshot. Zij beweert niet dat na de ophaaldatum geen externe wijziging is gepubliceerd."
        ),
    }
