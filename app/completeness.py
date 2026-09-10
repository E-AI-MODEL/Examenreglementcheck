from __future__ import annotations

import re
import uuid
from typing import Any

from .scope import formal_rule_in_scope

TOKEN_RE = re.compile(r"[a-zà-ÿ0-9]{3,}", re.I)
STOP = {
    "aan", "als", "bij", "binnen", "dat", "deze", "een", "heeft", "het",
    "kan", "met", "naar", "niet", "onder", "over", "uit", "van", "voor",
    "wordt", "zijn", "reglement", "regels", "informatie", "bevat",
}


def _tokens(value: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(value) if token.lower() not in STOP}


def _document_location(document: dict, unit: dict | None = None) -> dict:
    unit = unit or (document.get("units") or [{}])[0]
    return {
        "article": unit.get("article"),
        "page": unit.get("page"),
        "anchor_id": unit.get("anchor_id"),
        "text": unit.get("text", document.get("filename", "Documentbrede controle")),
    }


def _finding(document: dict, run_id: str, rule: dict, score: int) -> dict[str, Any]:
    evidence = []
    for item in rule.get("evidence") or []:
        evidence.append({
            "source_id": rule.get("source_id"),
            "rule_id": rule.get("rule_id"),
            "article": rule.get("article"),
            "fragment_id": item.get("fragment_id"),
            "quote_or_summary": rule.get("rule_summary"),
            "validator_status": "pending_evidence_validation",
        })
    return {
        "finding_id": "f-" + uuid.uuid4().hex[:10],
        "run_id": run_id,
        "document_location": _document_location(document),
        "related_document_locations": [],
        "topic": str(rule.get("topic") or "formele volledigheid"),
        "finding_type": ["formal_completeness_candidate"],
        "severity": "human_review",
        "confidence": "low" if document.get("parsing_status") != "complete" else "medium",
        "claim": (
            f"Controlepunt {rule['rule_id']} (‘{rule.get('topic', 'zonder onderwerp')}’) "
            "is niet overtuigend teruggevonden in de uitgelezen documenttekst."
        ),
        "evidence": evidence,
        "suggested_action": (
            "Controleer handmatig of dit onderwerp ontbreekt, elders is geformuleerd of door "
            "de extractie is gemist. Een ontbrekende tokenmatch is geen juridisch bewijs van afwezigheid."
        ),
        "suggested_text": None,
        "human_status": "unreviewed",
        "review_notes": None,
        "in_change_set": False,
        "deterministic_score": score,
    }


def assess_completeness(document: dict, rules: list[dict], run_id: str) -> dict[str, Any]:
    units = document.get("units") or []
    unit_rows = [(unit, _tokens(unit.get("text", ""))) for unit in units]
    checks = []
    findings = []
    for rule in rules:
        if not formal_rule_in_scope(rule):
            continue
        query = _tokens(" ".join(str(rule.get(key, "")) for key in ("topic", "rule_summary")))
        ranked = []
        for unit, tokens in unit_rows:
            overlap = len(query & tokens)
            if overlap:
                ranked.append((overlap, unit))
        ranked.sort(key=lambda item: (-item[0], item[1].get("order", 0)))
        best_score, best_unit = ranked[0] if ranked else (0, None)
        threshold = 2 if len(query) >= 4 else 1
        status = "candidate_present" if best_score >= threshold else "requires_human_review"
        checks.append({
            "rule_id": rule["rule_id"],
            "source_id": rule.get("source_id"),
            "topic": rule.get("topic"),
            "status": status,
            "score": best_score,
            "threshold": threshold,
            "document_location": _document_location(document, best_unit) if best_unit else None,
            "rule_status": rule.get("verification_status"),
            "production_approved": bool(rule.get("production_approved")),
            "reason": (
                "Deterministische tekstsignalen gevonden; inhoudelijke gelijkwaardigheid vereist menselijke review."
                if status == "candidate_present"
                else "Onvoldoende tekstsignalen; afwezigheid is niet automatisch bewezen."
            ),
        })
        if status == "requires_human_review":
            findings.append(_finding(document, run_id, rule, best_score))
    present = sum(check["status"] == "candidate_present" for check in checks)
    return {
        "status": "complete" if document.get("parsing_status") == "complete" else "partial",
        "checks": checks,
        "findings": findings,
        "summary": {
            "checked": len(checks),
            "candidate_present": present,
            "requires_human_review": len(checks) - present,
        },
        "method": "deterministic_token_screen_v1",
        "limitation": (
            "Dit is een formele volledigheidsscreening. Alleen menselijke inhoudelijke beoordeling "
            "kan bevestigen dat een regel werkelijk ontbreekt of juridisch afdoende is opgenomen."
        ),
    }
