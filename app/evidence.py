from __future__ import annotations

import hashlib
import re
from datetime import date
from typing import Any

TOKEN_RE = re.compile(r"[a-zà-ÿ0-9]{3,}", re.I)
STOP = {"een", "het", "van", "voor", "met", "dat", "wordt", "zijn", "kan", "deze", "naar", "bij", "uit", "aan", "over"}


def _tokens(value: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(value) if token.lower() not in STOP}


def validate_candidates(library, candidates: list[dict], *, as_of: str, exam_year: int | None) -> dict[str, Any]:
    results = []
    for candidate in candidates:
        rule = library.rule_index.get(candidate.get("rule_id"))
        source = library.source_index.get(candidate.get("source_id"))
        fragment = library.fragment_index.get(candidate.get("fragment_id"))
        reasons = []
        provenance_valid = bool(rule and source and fragment)
        if not rule:
            reasons.append("rule_missing")
        if not source:
            reasons.append("source_missing")
        if not fragment:
            reasons.append("fragment_missing")
        if fragment:
            actual_hash = hashlib.sha256(fragment.get("text", "").encode()).hexdigest()
            if actual_hash != fragment.get("text_hash"):
                provenance_valid = False
                reasons.append("fragment_hash_mismatch")
        gate_allowed, gate_reason = library.gate(candidate.get("rule_id", ""), as_of=as_of, exam_year=exam_year)
        if not gate_allowed:
            reasons.append(gate_reason)
        document_text = (candidate.get("document_location") or {}).get("text", "")
        reference_text = " ".join([
            str((rule or {}).get("topic", "")),
            str((rule or {}).get("rule_summary", "")),
            str((fragment or {}).get("text", ""))[:2500],
        ])
        doc_tokens = _tokens(document_text)
        ref_tokens = _tokens(reference_text)
        overlap = len(doc_tokens & ref_tokens)
        semantic_signal = "sufficient" if overlap >= 2 else "weak"
        if semantic_signal == "weak":
            reasons.append("weak_semantic_signal")
        status = "validated_for_must" if provenance_valid and gate_allowed and semantic_signal == "sufficient" else "human_review"
        validation = {
            "rule_id": candidate.get("rule_id"),
            "source_id": candidate.get("source_id"),
            "fragment_id": candidate.get("fragment_id"),
            "status": status,
            "provenance_valid": provenance_valid,
            "gate_allowed": gate_allowed,
            "gate_reason": gate_reason,
            "semantic_signal": semantic_signal,
            "token_overlap": overlap,
            "reasons": sorted(set(reason for reason in reasons if reason)),
            "validated_at": date.fromisoformat(as_of).isoformat(),
        }
        candidate["evidence_validation"] = validation
        results.append(validation)
    return {
        "status": "complete",
        "method": "provenance_gate_and_deterministic_overlap_v1",
        "results": results,
        "summary": {
            "checked": len(results),
            "validated_for_must": sum(result["status"] == "validated_for_must" for result in results),
            "human_review": sum(result["status"] != "validated_for_must" for result in results),
        },
        "limitation": (
            "Tokenoverlap is alleen een conservatief semantisch signaal. Een regel moet daarnaast expliciet "
            "productiegoedgekeurd zijn; deze validator keurt regels nooit zelf goed."
        ),
    }
