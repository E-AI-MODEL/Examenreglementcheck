from __future__ import annotations

from typing import Any


def build_export(run: dict) -> dict[str, Any]:
    findings = run.get("findings") or []
    changes = [finding for finding in findings if finding.get("in_change_set")]
    sources = []
    for candidate in run.get("source_candidates") or []:
        sources.append({
            key: candidate.get(key)
            for key in (
                "rule_id", "source_id", "source_title", "article", "url", "authority_class",
                "source_status", "source_gate", "evidence_validation",
            )
        })
    return {
        "export_version": "1.0",
        "run_id": run.get("run_id"),
        "generated_from_updated_at": run.get("updated_at"),
        "decision_note": {
            "status": run.get("status"),
            "school_year": run.get("school_year"),
            "exam_year": run.get("exam_year"),
            "school_types": (run.get("confirmed_context") or {}).get("school_types", []),
            "finding_count": len(findings),
            "accepted": sum(finding.get("human_status") == "accepted" for finding in findings),
            "needs_legal_review": sum(finding.get("human_status") == "needs_legal_review" for finding in findings),
            "partial_reasons": run.get("partial_reasons") or [],
        },
        "findings_report": findings,
        "change_list": changes,
        "source_accountability": sources,
        "audit_overview": run.get("audit") or [],
        "phase_status": run.get("phase_status") or {},
        "scope": run.get("scope") or {},
        "limitations": [
            "Geen juridisch keurmerk.",
            "SE/CE-controle en jurisprudentie-analyse vallen buiten de productscope.",
            "Vergelijkingsmateriaal is nooit juridisch bewijs.",
        ],
    }


def export_markdown(run: dict) -> str:
    bundle = build_export(run)
    note = bundle["decision_note"]
    lines = [
        "# Examenreglement-check — rapport",
        "",
        f"- Run: `{bundle['run_id']}`",
        f"- Status: **{note['status']}**",
        f"- Schooljaar: {note['school_year']}",
        f"- Schoolsoorten: {', '.join(note['school_types']) or 'niet bevestigd'}",
        f"- Bevindingen: {note['finding_count']}",
        f"- In wijzigingsset: {len(bundle['change_list'])}",
        "",
        "> Geen juridisch keurmerk. SE/CE en jurisprudentie vallen buiten de productscope.",
        "",
        "## Beslisnotitie",
        "",
    ]
    if note["partial_reasons"]:
        lines.extend(f"- {reason}" for reason in note["partial_reasons"])
    else:
        lines.append("- Alle controles binnen de gekozen productscope zijn uitgevoerd.")
    lines.extend(["", "## Bevindingen", ""])
    for finding in bundle["findings_report"]:
        lines.extend([
            f"### {finding.get('finding_id')} — {finding.get('topic')}",
            "",
            f"- Ernst: {finding.get('severity')}",
            f"- Zekerheid: {finding.get('confidence')}",
            f"- Reviewstatus: {finding.get('human_status')}",
            f"- Claim: {finding.get('claim')}",
            f"- Actie: {finding.get('suggested_action')}",
            f"- Vindplaats: {(finding.get('document_location') or {}).get('anchor_id') or 'documentbreed'}",
            "",
        ])
    lines.extend(["## Wijzigingslijst", ""])
    if not bundle["change_list"]:
        lines.append("Geen bevindingen geselecteerd.")
    for finding in bundle["change_list"]:
        lines.extend([
            f"- **{finding.get('topic')}** — {finding.get('suggested_text') or finding.get('suggested_action')}",
            f"  - Status: {finding.get('human_status')}",
        ])
    lines.extend(["", "## Bronverantwoording", ""])
    for source in bundle["source_accountability"]:
        validation = source.get("evidence_validation") or {}
        lines.append(
            f"- `{source.get('rule_id')}` — {source.get('source_title')} · "
            f"evidence: {validation.get('status', 'niet gevalideerd')} · {source.get('url')}"
        )
    lines.extend(["", "## Audit", ""])
    lines.extend(f"- {event.get('time')} — {event.get('action')}" for event in bundle["audit_overview"])
    return "\n".join(lines).rstrip() + "\n"
