"""Fail-closed source/rule activation gate. It does not validate a school-document claim."""
from datetime import date
from hashlib import sha256

def can_support_must(rule, source, fragments, *, as_of, exam_year):
    if rule.get('source_id') != source.get('id'): return False, 'source_mismatch'
    if source.get('authority_class') != 'binding': return False, 'not_binding'
    if rule.get('norm_type') == 'advisory': return False, 'advisory_rule'
    if rule.get('verification_status') != 'validated' or not rule.get('production_approved'): return False, 'rule_not_approved'
    if not source.get('production_approved') or source.get('legal_review_status') != 'approved': return False, 'source_not_approved'
    if source.get('status') != 'active_reviewed' or source.get('fetch_status') != 'retrieved': return False, 'source_not_active'
    if not rule.get('verified_by') or not rule.get('verified_at'): return False, 'review_provenance_missing'
    try:
        target=date.fromisoformat(as_of)
        for obj in (source,rule):
            if obj.get('valid_from') and target < date.fromisoformat(obj['valid_from']): return False, 'not_yet_valid'
            if obj.get('valid_to') and target >= date.fromisoformat(obj['valid_to']): return False, 'expired'
            if obj.get('exam_year') is not None and obj['exam_year'] != exam_year: return False, 'wrong_exam_year'
    except (ValueError,TypeError): return False, 'invalid_date'
    evidence=rule.get('evidence',[])
    if not evidence:return False,'evidence_missing'
    index={f['fragment_id']:f for f in fragments}
    for ev in evidence:
        fragment=index.get(ev.get('fragment_id'))
        if not fragment or fragment.get('source_id') != source['id']: return False,'fragment_missing_or_mismatched'
        if not fragment.get('text') or ev.get('text_hash') != fragment.get('text_hash') or sha256(fragment['text'].encode()).hexdigest()!=fragment.get('text_hash'): return False,'fragment_hash_mismatch'
    return True,'eligible_source_only_context_and_school_evidence_still_required'
