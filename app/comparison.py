from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"[a-zà-ÿ0-9]{4,}", re.I)
STOP = {"deze", "document", "examenreglement", "wordt", "voor", "onder", "alleen", "status", "bron"}
TOPICS = {
    "beroep": ("beroep", "commissie", "verzoekschrift"),
    "maatregelen": ("maatregel", "onregelmatigheid", "fraude"),
    "rollen": ("rector", "directeur", "examencommissie", "examensecretaris"),
    "vaststelling": ("vaststelling", "instemming", "publicatie"),
    "afwezigheid": ("afwezigheid", "ziekte", "overmacht"),
    "inzage": ("inzage", "inzien"),
}


def _tokens(value: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(value) if token.lower() not in STOP}


def _topics(value: str) -> list[str]:
    lowered = value.lower()
    return [name for name, terms in TOPICS.items() if any(term in lowered for term in terms)]


def compare_document(root: Path, document: dict) -> dict[str, Any]:
    records = json.loads((root / "sources/comparisons.json").read_text())
    school_year = document.get("school_year")
    school_types = set(document.get("school_types") or [])
    own_text = "\n".join(unit.get("text", "") for unit in document.get("units") or [])
    own_tokens = _tokens(own_text)
    own_topics = set(_topics(own_text))
    rows = []
    skipped = []
    for record in records:
        if record.get("year") != school_year:
            skipped.append({"comparison_id": record.get("comparison_id"), "reason": "school_year_mismatch"})
            continue
        record_types = set(record.get("school_types") or [])
        if school_types and record_types and not (school_types & record_types):
            skipped.append({"comparison_id": record.get("comparison_id"), "reason": "school_type_mismatch"})
            continue
        comparison_id = record.get("comparison_id", "")
        path = root / "sources/content" / f"{comparison_id}.md"
        if not path.is_file():
            skipped.append({"comparison_id": comparison_id, "reason": "comparison_content_missing"})
            continue
        content = path.read_text()
        comparison_tokens = _tokens(content)
        comparison_topics = set(_topics(content))
        shared_topics = sorted(own_topics & comparison_topics)
        overlap = len(own_tokens & comparison_tokens)
        rows.append({
            "comparison_id": comparison_id,
            "school": record.get("school"),
            "school_types": sorted(record_types),
            "year": record.get("year"),
            "status": record.get("status"),
            "url": record.get("url"),
            "authority_class": "example",
            "comparison_performed": True,
            "shared_topics": shared_topics,
            "token_overlap": overlap,
            "excerpt": " ".join(content.split())[:700],
            "legal_evidence": False,
            "limitation": "Alleen structuur en onderwerpen vergelijken; dit document is nooit juridisch bewijs.",
        })
    return {
        "status": "complete",
        "method": "metadata_topic_comparison_v1",
        "comparisons": rows,
        "skipped": skipped,
        "summary": {
            "compared": len(rows),
            "skipped": len(skipped),
            "shared_topics": sorted({topic for row in rows for topic in row["shared_topics"]}),
        },
        "limitation": (
            "De meegeleverde vergelijkingsteksten zijn korte bronnotities. De uitkomst toont alleen "
            "onderwerp- en structuurparallellen en trekt geen juridische conclusie."
        ),
    }
