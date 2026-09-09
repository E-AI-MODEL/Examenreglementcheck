from __future__ import annotations
import json,re
from pathlib import Path
from typing import Any
from .source_gate import can_support_must

TOKEN_RE=re.compile(r'[a-zà-ÿ0-9]{3,}',re.I)
STOP={'het','een','van','voor','met','dat','wordt','zijn','kan','deze','naar','bij','uit','aan','over','onder','heeft','als','ook'}

def _tokens(s:str)->set[str]: return {x.lower() for x in TOKEN_RE.findall(s) if x.lower() not in STOP}
def infer_scope(text:str)->str:
    n=' '+text.lower()+' '
    if any(x in n for x in (' centraal examen ',' ce ','examenwerk','tijdvak')):return 'ce'
    if any(x in n for x in (' schoolexamen ',' se ','pta','herkans')):return 'se'
    return 'algemeen'

def _rule_scope(rule:dict,source:dict)->set[str]:
    txt=' '.join(str(rule.get(k,'')) for k in ('topic','rule_summary','article','limitations')).lower()+' '+' '.join(map(str,source.get('tags') or []))
    scopes={'algemeen'}
    if any(x in txt for x in ('centraal examen',' ce ','examenwerk','tijdvak','hulpmiddel')):scopes.add('ce')
    if any(x in txt for x in ('schoolexamen',' se ','pta','herkans')):scopes.add('se')
    return scopes

class SourceLibrary:
    def __init__(self,root:Path):
        self.sources=json.loads((root/'sources/registry.json').read_text())
        self.rules=json.loads((root/'rules/candidates.json').read_text())
        self.fragments=json.loads((root/'sources/fragments.json').read_text())
        self.source_index={s['id']:s for s in self.sources};self.rule_index={r['rule_id']:r for r in self.rules};self.fragment_index={f['fragment_id']:f for f in self.fragments}
    def search(self,query:str,*,exam_year:int|None=None,school_year:str|None=None,school_types:list[str]|None=None,scope:str|None=None,legal_regime:str|None='WVO 2020',limit:int=8,min_score:int=2,include_comparison:bool=False)->list[dict[str,Any]]:
        q=_tokens(query);scope=scope or infer_scope(query);rows=[];school_types=set(school_types or [])
        for r in self.rules:
            s=self.source_index.get(r['source_id'])
            if not s or s.get('fetch_status')!='retrieved':continue
            if s.get('status') in {'fetch_failed','excluded_wrong_year','rejected','archived'}:continue
            if not include_comparison and s.get('authority_class')=='example':continue
            if exam_year and s.get('exam_year') not in (None,exam_year):continue
            if school_year and s.get('school_year') not in (None,school_year):continue
            source_types=set(s.get('school_types') or [])
            if school_types and source_types and not (school_types & source_types):continue
            if legal_regime and s.get('legal_regime') not in (None,legal_regime):continue
            scopes=_rule_scope(r,s)
            if scope!='algemeen' and scope not in scopes and scopes != {'algemeen'}:continue
            text=' '.join(str(r.get(k,'')) for k in ('topic','rule_summary','article','limitations','applies_when'))+' '+' '.join(map(str,s.get('tags') or []))
            overlap=len(q & _tokens(text));topic_tokens=_tokens(str(r.get('topic','')))
            score=overlap+(2 if topic_tokens and (topic_tokens & q) else 0)
            if score<min_score:continue
            ev=r.get('evidence') or [];frag=None
            if ev and ev[0].get('fragment_id'):frag=self.fragment_index.get(ev[0]['fragment_id'])
            rows.append({"score":score,"scope":scope,"rule_id":r['rule_id'],"topic":r.get('topic'),"rule_summary":r.get('rule_summary'),"article":r.get('article'),"norm_type":r.get('norm_type'),"verification_status":r.get('verification_status'),"production_approved":r.get('production_approved',False),"source_id":s['id'],"source_title":s['title'],"authority_class":s.get('authority_class'),"source_status":s.get('status'),"source_exam_year":s.get('exam_year'),"source_school_year":s.get('school_year'),"legal_regime":s.get('legal_regime'),"fragment_id":frag.get('fragment_id') if frag else None,"fragment_excerpt":frag.get('text','')[:900] if frag else None,"url":ev[0].get('url') if ev else s.get('url')})
        rows.sort(key=lambda x:(-x['score'],x['authority_class']!='binding',x['rule_id']))
        return rows[:limit]
    def gate(self,rule_id:str,*,as_of:str,exam_year:int|None)->tuple[bool,str]:
        r=self.rule_index.get(rule_id)
        if not r:return False,'rule_missing'
        s=self.source_index.get(r.get('source_id'))
        if not s:return False,'source_missing'
        return can_support_must(r,s,self.fragments,as_of=as_of,exam_year=exam_year)
