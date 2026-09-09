from __future__ import annotations
import re, unicodedata
from typing import Any

ROLE_PATTERNS={
 'rector':r'\brector\b','directeur':r'\bdirecteur\b','examencommissie':r'\bexamencommissie\b',
 'examensecretaris':r'\bexamensecretaris\b','commissie_van_beroep':r'\bcommissie van beroep\b',
 'bevoegd_gezag':r'\bbevoegd gezag\b','kandidaat':r'\b(?:kandidaat|examenkandidaat)\b'
}
TERM_RE=re.compile(r'\b(?P<value>\d+)\s*(?P<unit>schooldagen?|werkdagen?|dagen?|weken?)\b',re.I)
REF_RE=re.compile(r'\bartikel\s+(?P<article>\d{1,3}(?:\.\d+)*(?:[a-z])?)\b',re.I)
DEF_RE=re.compile(r'^\s*(?P<term>[^:]{2,50}?)\s+(?:betekent|wordt verstaan onder)\s+(?P<definition>.+)$',re.I)
TOPICS=[
 ('beroep',('beroep','commissie van beroep','verzoekschrift')),
 ('herkansing',('herkans','aanmeld')),
 ('maatregel',('maatregel','onregelmatigheid','fraude')),
 ('inzage',('inzage','inzien')),
 ('afwezigheid',('afwezig','ziekte','overmacht')),
 ('schoolexamen',('schoolexamen','se ')),
 ('centraal_examen',('centraal examen',' ce ','examenwerk')),
 ('vaststelling',('vaststell','instemming','medezeggenschapsraad')),
]
ACTION_PATTERNS=[
 ('advise',r'\b(?:adviseert|adviseren|advies uitbrengt?|advies geeft?)\b'),
 ('file_appeal',r'\b(?:beroep\s+(?:instellen|indienen)|verzoekschrift\s+(?:indienen|wordt ingediend))\b'),
 ('register',r'\b(?:meldt zich|aanmeld(?:en|t)?|inschrij(?:ven|ft))\b'),
 ('decide',r'\b(?:besluit|beslist|beslissen|stelt vast|vaststellen|bepaalt)\b'),
 ('notify',r'\b(?:zendt|verstuurt|deelt mee|bekendmaakt|wordt meegedeeld)\b'),
 ('review',r'\b(?:beoordeelt|controleert|toetst)\b'),
 ('allow',r'\b(?:toestaat|toestaan|kan .*? toestaan)\b'),
 ('must_do',r'\b(?:dient|moet)\b'),
]
EXTERNAL_SOURCES={
 'wvo_2020':r'\b(?:wvo\s*2020|wet voortgezet onderwijs(?:\s*2020)?)\b',
 'uitvoeringsbesluit_wvo_2020':r'\buitvoeringsbesluit\s+wvo(?:\s*2020)?\b',
 'awb':r'\b(?:awb|algemene wet bestuursrecht)\b',
 'wms':r'\b(?:wms|wet medezeggenschap op scholen)\b',
 'cvte':r'\b(?:cvte|college voor toetsen en examens)\b',
}

def _norm(s:str)->str:
    s=unicodedata.normalize('NFKD',s.lower());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'\s+',' ',s).strip()

def _topic(text:str)->str:
    n=' '+_norm(text)+' '
    for key,words in TOPICS:
        if any(w in n for w in words):return key
    return 'algemeen'

def _clauses(text:str)->list[str]:
    # Split explicit sentences and coordination that introduces a new grammatical subject.
    parts=re.split(r'(?<=[.;!?])\s+|\s+en\s+(?=(?:de|het|een)\s+(?:rector|directeur|examencommissie|examensecretaris|commissie|bevoegd gezag|kandidaat))',text,flags=re.I)
    return [p.strip(' ;') for p in parts if p.strip(' ;')]

def _roles_with_positions(text:str):
    low=_norm(text);rows=[]
    for role,pat in ROLE_PATTERNS.items():
        for m in re.finditer(pat,low,re.I):rows.append((role,m.start(),m.end()))
    return sorted(rows,key=lambda x:x[1])

def _action(text:str)->tuple[str|None,int|None]:
    low=_norm(text);found=[]
    for action,pat in ACTION_PATTERNS:
        m=re.search(pat,low,re.I)
        if m:found.append((m.start(),action))
    if not found:return None,None
    pos,action=min(found)
    return action,pos

def _actor_for_clause(clause:str, action_pos:int|None)->tuple[str|None,list[str]]:
    rows=_roles_with_positions(clause);roles=[r for r,_,_ in rows]
    if action_pos is None:return (roles[0] if len(roles)==1 else None),roles
    before=[r for r,s,e in rows if s <= action_pos]
    actor=before[-1] if before else (roles[0] if roles else None)
    return actor,roles

def _start_event(clause:str)->str|None:
    # V3.2 bugfix: beperk tot het eerste kern-zelfstandignaamwoord, niet de hele rest van de clausule.
    # V3.1 pakte alles tussen "na" en het eerste leesteken — daardoor kregen termijnen
    # die semantisch dezelfde stap beschrijven verschillende start_events (bv. "publicatie"
    # vs "publicatie aan voor de herkansing") en werden conflicts onterecht gemist.
    low=_norm(clause)
    # Stop-lijst van voorzetsels, werkwoorden en voegwoorden die einde van het kern-zelfstandignaamwoord aangeven.
    stop_words = {'aan','voor','tot','van','om','op','bij','met','in','uit','en','wordt','kan','moet','dient',
                  'binnen','gedurende','naar','tegen','boven','onder','tot','aan'}
    m=re.search(r'\b(?:na|vanaf|volgend op)\s+(?:de\s+)?([a-zà-ÿ]{3,30}(?:\s+[a-zà-ÿ]{3,30}){0,1})',low)
    if not m: return None
    # Neem alleen woorden die niet in de stop-lijst staan
    words = m.group(1).strip().split()
    keep = []
    for w in words:
        if w in stop_words: break
        keep.append(w)
    return ' '.join(keep) if keep else None

def _deadline_type(action:str|None,clause:str)->str:
    if action=='file_appeal':return 'filing'
    if action=='register':return 'registration'
    if action=='decide':return 'decision'
    if action=='notify':return 'notification'
    n=_norm(clause)
    if 'herkans' in n:return 'retry'
    return 'unspecified'

def _external_source(clause:str)->str|None:
    low=_norm(clause)
    for key,pat in EXTERNAL_SOURCES.items():
        if re.search(pat,low,re.I):return key
    return None

def build_registers(document:dict[str,Any])->dict[str,Any]:
    roles=[];terms=[];definitions=[];procedures=[];refs=[]
    articles={str(u.get('article')) for u in document['units'] if u.get('article')}
    for u in document['units']:
        text=u['text'];loc={"unit_id":u['unit_id'],"anchor_id":u['anchor_id'],"page":u.get('page'),"article":u.get('article'),"text":text}
        # Procedure and role records are clause-aware so advisor and decision-maker are not conflated.
        for clause in _clauses(text):
            topic=_topic(clause);action,action_pos=_action(clause);actor,clause_roles=_actor_for_clause(clause,action_pos)
            for role,_,_ in _roles_with_positions(clause):
                roles.append({"role":role,"topic":topic,"action":action,"actor":role==actor,"clause":clause,"location":loc})
            if action:
                procedures.append({"topic":topic,"action":action,"actor":actor,"roles":clause_roles,"decision_type":topic if action=='decide' else None,"phase":_deadline_type(action,clause),"start_event":_start_event(clause),"text":clause,"location":loc})
            for m in TERM_RE.finditer(clause):
                terms.append({"topic":topic,"value":int(m.group('value')),"unit":_norm(m.group('unit')),"action":action,"actor":actor,"deadline_type":_deadline_type(action,clause),"start_event":_start_event(clause),"clause":clause,"location":loc})
        m=DEF_RE.match(text)
        if m:definitions.append({"term":_norm(m.group('term')),"definition":m.group('definition').strip(),"location":loc})
        # Reference scope is explicit. Generic words such as "wet" do not turn an internal reference external.
        for clause in _clauses(text):
            source=_external_source(clause)
            for m in REF_RE.finditer(clause):
                target=m.group('article');external=source is not None
                refs.append({"target":target,"resolved":True if external else target in articles,"external":external,"reference_scope":"external" if external else "internal","target_source":source,"clause":clause,"location":loc})
    return {"role_registry":roles,"term_registry":terms,"definition_registry":definitions,"procedure_registry":procedures,"cross_reference_registry":refs}
