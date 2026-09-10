from __future__ import annotations

import re
from typing import Any


def _signature(finding: dict) -> str:
    return re.sub(r"\W+", " ", finding.get("claim", "").lower()).strip()


def run_counter_review(findings: list[dict], *, parsing_status: str) -> dict[str, Any]:
    checks = []
    seen = set()
    changed = 0
    for finding in findings:
        finding_checks = []
        signature = _signature(finding)
        if signature in seen:
            finding_checks.append("duplicate_claim")
        seen.add(signature)
        evidence = finding.get("evidence") or []
        if not evidence:
            finding_checks.append("evidence_missing")
        if finding.get("severity") == "must":
            validated = evidence and all(item.get("validator_status") == "validated" for item in evidence)
            if not validated:
                finding["severity"] = "human_review"
                finding["confidence"] = "low"
                finding_checks.append("unsupported_must_downgraded")
                changed += 1
        if parsing_status != "complete" and "formal_completeness_candidate" in finding.get("finding_type", []):
            if finding.get("confidence") != "low":
                finding["confidence"] = "low"
                changed += 1
            finding_checks.append("partial_parsing_blocks_absence_conclusion")
        if any(item.get("validator_status") == "example_only" for item in evidence):
            if finding.get("severity") not in {"comparison", "human_review"}:
                finding["severity"] = "comparison"
                changed += 1
            finding_checks.append("comparison_not_legal_evidence")
        finding["counter_review"] = {
            "status": "attention" if finding_checks else "passed",
            "checks": finding_checks,
        }
        checks.append({"finding_id": finding.get("finding_id"), **finding["counter_review"]})
    return {
        "status": "complete",
        "checks": checks,
        "changed_findings": changed,
        "attention": sum(check["status"] == "attention" for check in checks),
        "method": "deterministic_safety_review_v1",
    }
