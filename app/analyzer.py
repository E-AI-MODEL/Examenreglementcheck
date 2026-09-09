from __future__ import annotations
import re,uuid
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from .registers import build_registers
from .retrieval import SourceLibrary,infer_scope

ANALYZER_VERSION='v3.1-deterministic-0.2'

def _doc_ev(document,loc):
    return {"source_id":"document:"+document['document_id'],"quote_or_summary":loc['text'],"anchor_id":loc['anchor_id'],"page":loc.get('page'),"article":loc.get('article')}

def _finding(document,run_id,severity,topic,claim,action,locations,ftype):
    primary=locations[0]
    return {"finding_id":"f-"+uuid.uuid4().hex[:10],"run_id":run_id,"document_location":{"article":primary.get('article'),"page":primary.get('page'),"anchor_id":primary.get('anchor_id'),"text":primary.get('text','')},"related_document_locations":locations[1:],"topic":topic,"finding_type":[ftype],"severity":severity,"confidence":"high","claim":claim,"evidence":[_doc_ev(document,l) for l in locations],"suggested_action":action,"suggested_text":None,"human_status":"unreviewed","review_notes":None,"in_change_set":False}

def _term_key(t):
    # Only compare deadlines that are known to describe the same kind of step.
    if t.get('deadline_type') in (None,'unspecified'):return None
    event=re.sub(r'\W+',' ',(t.get('start_event') or '').lower()).strip()
    return (t['topic'],t['deadline_type'],t.get('action') or '',event)

def internal_findings(document,regs,run_id):
    out=[];by=defaultdict(list)
    for t in regs['term_registry']:
        key=_term_key(t)
        if key:by[key].append(t)
    for key,items in by.items():
        # Same semantic step, same unit family, different numeric values. Cross-unit comparisons remain human work.
        units={x['unit'] for x in items};vals={x['value'] for x in items}
        if len(vals)>1 and len(units)==1:
            topic,deadline_type,action,event=key;locs=[x['location'] for x in items[:6]];unit=next(iter(units));values=', '.join(f"{v} {unit}" for v in sorted(vals))
            step={'filing':'indienen/instellen','registration':'aanmelden','decision':'beslissen','notification':'bekendmaken','retry':'herkansen'}.get(deadline_type,deadline_type)
            out.append(_finding(document,run_id,'internal_conflict',topic,f"Het document noemt voor dezelfde stap ({step}) bij {topic} verschillende termijnen: {values}.","Controleer of deze passages werkelijk dezelfde procedurestap en hetzelfde startmoment beschrijven. Leg één termijn vast of maak het onderscheid expliciet.",locs,'term_conflict'))
    # Compare decision-makers only for the same action and decision type. Advisors are not decision-makers.
    proc=defaultdict(list)
    for p in regs['procedure_registry']:
        if p.get('action')=='decide' and p.get('actor'):
            proc[(p['topic'],p.get('decision_type') or p['topic'])].append(p)
    for (topic,decision_type),items in proc.items():
        actors={p['actor'] for p in items if p.get('actor') not in {'kandidaat'}}
        if topic!='algemeen' and len(actors)>1:
            locs=[p['location'] for p in items[:6]]
            out.append(_finding(document,run_id,'internal_conflict',topic,f"Het document koppelt dezelfde beslissing over {topic} aan verschillende beslissers: {', '.join(sorted(actors))}.","Controleer of dit echt dezelfde beslissing en fase betreft. Maak bevoegdheid, mandaat of faseverschil expliciet.",locs,'role_conflict'))
    for r in regs['cross_reference_registry']:
        if r['reference_scope']=='internal' and not r['resolved']:
            out.append(_finding(document,run_id,'editorial','verwijzingen',f"De interne verwijzing naar artikel {r['target']} kan in het uitgelezen document niet worden teruggevonden.","Controleer het bedoelde artikelnummer. Bij onvolledige parsing eerst de documentextractie controleren.",[r['location']],'broken_reference'))
    defs=defaultdict(list)
    for d in regs['definition_registry']:defs[d['term']].append(d)
    for term,items in defs.items():
        norm={re.sub(r'\W+',' ',x['definition'].lower()).strip() for x in items}
        if len(norm)>1:
            out.append(_finding(document,run_id,'internal_conflict','definities',f"Het begrip ‘{term}’ krijgt meer dan één verschillende definitie.","Vergelijk de definities en maak duidelijk of één definitie leidend is.",[x['location'] for x in items[:6]],'definition_conflict'))
    return out

def source_candidates(document,lib):
    meta=document.get('metadata',{});exam_year=meta.get('expected_exam_year');snippets=[];seen=set()
    for u in document['units']:
        if len(u['text'])<20:continue
        scope=infer_scope(u['text'])
        for hit in lib.search(u['text'],exam_year=exam_year,school_year=document.get('school_year'),school_types=document.get('school_types') or [],scope=scope,legal_regime='WVO 2020',limit=3,min_score=2):
            key=hit['rule_id']
            if key in seen:continue
            seen.add(key);hit['document_location']={k:u.get(k) for k in ('anchor_id','page','article','text')};snippets.append(hit)
            if len(snippets)>=12:return snippets
    return snippets

def analyze_document(document:dict[str,Any],*,root:Path,run_id:str,as_of:str|None=None)->dict[str,Any]:
    regs=build_registers(document);findings=internal_findings(document,regs,run_id);lib=SourceLibrary(root);candidates=source_candidates(document,lib)
    as_of=as_of or date.today().isoformat();exam_year=document.get('metadata',{}).get('expected_exam_year');gate_results=[]
    for c in candidates:
        allowed,reason=lib.gate(c['rule_id'],as_of=as_of,exam_year=exam_year);c['source_gate']={'eligible':allowed,'reason':reason};gate_results.append(c['source_gate'])
    eligible=sum(1 for g in gate_results if g['eligible'])
    return {"registers":regs,"findings":findings,"source_candidates":candidates,"coverage":{"legal_must_enabled":False,"source_gate_checked":len(gate_results),"source_gate_eligible":eligible,"semantic_evidence_validator":"not_implemented","reason":"De bronpoort is uitgevoerd. De semantische evidence-validator ontbreekt nog, dus v3.1 produceert geen juridische must-findings.","candidate_count":len(candidates)}}
