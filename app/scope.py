from __future__ import annotations

"""Productscope for the deterministic checker.

SE/CE-specific controls and jurisprudence are intentionally outside the active
product scope. Keeping this in one module prevents those records from leaking
back into retrieval, completeness or reporting through generic token matches.
"""

EXCLUDED_RULE_PREFIXES = ("SE-", "CE-", "PTA-", "HUL-", "ROO-")
FORMAL_RULE_PREFIXES = ("REG-", "ROL-", "BER-", "MAA-")
EXCLUDED_CONTENT_MARKERS = (
    "schoolexamen", " se ", "pta", "centraal examen", " ce ",
    "examenwerk", "tijdvak", "cspe",
)


def rule_in_scope(rule: dict) -> bool:
    rule_id = str(rule.get("rule_id", ""))
    text = " " + " ".join(
        str(rule.get(key, "")) for key in ("topic", "rule_summary", "applies_when", "limitations")
    ).lower() + " "
    return (
        bool(rule_id)
        and not rule_id.startswith(EXCLUDED_RULE_PREFIXES)
        and not any(marker in text for marker in EXCLUDED_CONTENT_MARKERS)
    )


def formal_rule_in_scope(rule: dict) -> bool:
    rule_id = str(rule.get("rule_id", ""))
    return rule_in_scope(rule) and rule_id.startswith(FORMAL_RULE_PREFIXES)


def scope_summary() -> dict:
    return {
        "included": [
            "documentextractie",
            "formele volledigheidsscreening",
            "interne consistentie",
            "bronactualiteit binnen de opgeslagen snapshot",
            "vergelijkingsmateriaal als voorbeeld",
            "kritische tegenlezing",
            "evidence- en provenancevalidatie",
        ],
        "excluded": ["SE/CE-inhoudelijke controle", "jurisprudentie-analyse"],
    }
