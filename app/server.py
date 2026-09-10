from __future__ import annotations
import shutil,time,re,zipfile
from pathlib import Path
from fastapi import FastAPI,UploadFile,File,Form,HTTPException
from fastapi.responses import HTMLResponse,PlainTextResponse
from pydantic import BaseModel
from . import __version__
from .ai_adapter import status as ai_status
from .parser import parse_document,PARSER_VERSION,expected_exam_year,ocr_status
from .analyzer import analyze_document,ANALYZER_VERSION
from .exporter import build_export,export_markdown
from .run_store import RunStore
from .scope import scope_summary

ROOT=Path(__file__).resolve().parents[1];store=RunStore(ROOT)
app=FastAPI(title='Examenreglement-checker v3.3',version=__version__)
ALLOWED_REVIEW={'unreviewed','accepted','rejected','needs_legal_review','implemented','resolved'}
ALLOWED_STATUS={'concept','vastgesteld','historisch'}
ALLOWED_TYPES={'havo','vwo','vmbo'}
MAX_UPLOAD=20*1024*1024
MAX_DOCX_UNCOMPRESSED=100*1024*1024

class AnalyzeRequest(BaseModel):
    school_year:str|None=None
    school_types:list[str]|None=None
    document_status:str='concept'
    confirmed:bool=True
    ai_mode:str='off'
class ReviewRequest(BaseModel):
    human_status:str
    review_notes:str|None=None
    in_change_set:bool=False
    suggested_text:str|None=None

def _validated_context(school_year:str|None,school_types:list[str],document_status:str):
    if not school_year or expected_exam_year(school_year) is None:raise HTTPException(422,detail='Schooljaar moet bijvoorbeeld 2026-2027 zijn en uit twee opeenvolgende jaren bestaan.')
    types=sorted(set(school_types))
    if not types or any(x not in ALLOWED_TYPES for x in types):raise HTTPException(422,detail='Kies minimaal één geldige schoolsoort: havo, vwo of vmbo.')
    if document_status not in ALLOWED_STATUS:raise HTTPException(422,detail='Ongeldige documentstatus.')
    return {'school_year':school_year,'exam_year':expected_exam_year(school_year),'school_types':types,'document_status':document_status}

def _apply_confirmed_context(run,context):
    doc=run['document'];doc['school_year']=context['school_year'];doc['metadata']['school_year']=context['school_year'];doc['metadata']['expected_exam_year']=context['exam_year'];doc['school_types']=context['school_types'];doc['document_status']=context['document_status']
    run['school_year']=context['school_year'];run['exam_year']=context['exam_year'];run['confirmed_context']=dict(context);run['context_status']='confirmed';run['document']=doc

def _event(action,**extra):return {'time':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'action':action,**extra}

def _save_upload_limited(upload,path):
    total=0
    with path.open('wb') as out:
        while True:
            chunk=upload.file.read(1024*1024)
            if not chunk:break
            total+=len(chunk)
            if total>MAX_UPLOAD:
                out.close();path.unlink(missing_ok=True)
                raise HTTPException(413,detail='Bestand is groter dan 20 MB.')
            out.write(chunk)
    return total

def _validate_file_content(path,suffix):
    if suffix=='.pdf':
        if path.read_bytes()[:5] != b'%PDF-':
            raise HTTPException(415,detail='Het bestand heeft .pdf als naam maar is geen geldig PDF-bestand.')
        return
    try:
        with zipfile.ZipFile(path) as z:
            names=set(z.namelist())
            if '[Content_Types].xml' not in names or 'word/document.xml' not in names:
                raise HTTPException(415,detail='Het bestand heeft .docx als naam maar bevat geen geldig Word-document.')
            total=sum(i.file_size for i in z.infolist())
            if total>MAX_DOCX_UNCOMPRESSED:
                raise HTTPException(413,detail='DOCX pakt uit tot meer dan 100 MB en wordt niet verwerkt.')
    except zipfile.BadZipFile:
        raise HTTPException(415,detail='Het bestand heeft .docx als naam maar is geen geldig DOCX-bestand.')

@app.get('/',response_class=HTMLResponse)
def home():return (ROOT/'web/index.html').read_text()
@app.get('/api/health')
def health():return {'ok':True,'version':__version__,'analysis_mode':'deterministic','ai':ai_status().__dict__,'ocr':ocr_status(),'scope':scope_summary()}

@app.post('/api/parse')
async def parse(file:UploadFile=File(...),school_year:str|None=Form(None),school_types:str=Form(''),document_status:str=Form('concept'),ai_mode:str=Form('off')):
    if ai_mode!='off':raise HTTPException(409,detail=ai_status().reason)
    suffix=Path(file.filename or '').suffix.lower()
    if suffix not in {'.pdf','.docx'}:raise HTTPException(415,detail='Alleen PDF en DOCX worden ondersteund.')
    run_id=store.new_id();path=store.upload_path(run_id,file.filename or ('document'+suffix))
    _save_upload_limited(file,path)
    try:_validate_file_content(path,suffix)
    except HTTPException:
        path.unlink(missing_ok=True);raise
    try:doc=parse_document(path,school_year=school_year or None,school_types=[x.strip() for x in school_types.split(',') if x.strip()],document_status=document_status)
    except Exception as e:path.unlink(missing_ok=True);raise HTTPException(422,detail=f'Extractie mislukt: {e}')
    run={'run_id':run_id,'document_hash':doc['sha256'],'school_year':doc.get('school_year') or '', 'exam_year':doc.get('metadata',{}).get('expected_exam_year') or 0,'context_status':'unconfirmed','status':'awaiting_confirmation','source_snapshot':'2026-09-07-first-content','analysis_mode':'deterministic_no_ai','scope':scope_summary(),'phase_status':{'A_extractie':'complete' if doc['parsing_status']=='complete' else 'partial','B_volledigheid':'not_started','C_interne_consistentie':'not_started','D_actualiteit':'not_started','E_se_ce':'out_of_scope','F_jurisprudentie':'out_of_scope','G_vergelijking':'not_started','H_tegenlezing':'not_started','I_evidence_validatie':'not_started'},'versions':{'analyzer':ANALYZER_VERSION,'rule_set':'candidate-rules-v0.2','parser':PARSER_VERSION,'model':None,'prompt_set':None},'document':doc,'upload_path':str(path.relative_to(ROOT)),'findings':[],'registers':{},'source_candidates':[],'review_history':[],'partial_reasons':[],'audit':[_event('document_parsed') ]}
    store.save(run_id,run);return run

@app.post('/api/analyze/{run_id}')
def analyze(run_id:str,request:AnalyzeRequest):
    if request.ai_mode!='off':raise HTTPException(409,detail=ai_status().reason)
    try:run=store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
    if not request.confirmed:raise HTTPException(409,detail='Bevestig de documentcheck vóór analyse.')
    selected_types=request.school_types if request.school_types is not None else run['document'].get('school_types') or []
    context=_validated_context(request.school_year or run.get('school_year'),selected_types,request.document_status)
    _apply_confirmed_context(run,context)
    run['status']='analyzing'
    for phase in ('B_volledigheid','C_interne_consistentie','D_actualiteit','G_vergelijking','H_tegenlezing','I_evidence_validatie'):run['phase_status'][phase]='running'
    run.setdefault('audit',[]).append(_event('context_confirmed',context=context));store.save(run_id,run)
    result=analyze_document(run['document'],root=ROOT,run_id=run_id,as_of=time.strftime('%Y-%m-%d',time.gmtime()))
    run.update(result)
    run['phase_status'].update({'B_volledigheid':result['completeness']['status'],'C_interne_consistentie':'complete','D_actualiteit':result['actuality']['status'],'E_se_ce':'out_of_scope','F_jurisprudentie':'out_of_scope','G_vergelijking':result['comparisons']['status'],'H_tegenlezing':result['counter_review']['status'],'I_evidence_validatie':result['evidence_validation']['status']})
    included=('A_extractie','B_volledigheid','C_interne_consistentie','D_actualiteit','G_vergelijking','H_tegenlezing','I_evidence_validatie')
    partial=[phase for phase in included if run['phase_status'].get(phase)!='complete']
    run['status']='partial' if partial else 'complete'
    run['partial_reasons']=[f"Fase {phase.split('_',1)[0]} is {run['phase_status'].get(phase)}." for phase in partial]
    run['audit'].append(_event('analysis_completed',status=run['status'],findings=len(run['findings']),source_candidates=len(run['source_candidates'])));store.save(run_id,run);return run

@app.patch('/api/runs/{run_id}/findings/{finding_id}')
def review_finding(run_id:str,finding_id:str,request:ReviewRequest):
    if request.human_status not in ALLOWED_REVIEW:raise HTTPException(422,detail='Ongeldige reviewstatus.')
    try:run=store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
    finding=next((f for f in run.get('findings',[]) if f.get('finding_id')==finding_id),None)
    if not finding:raise HTTPException(404,detail='Bevinding niet gevonden.')
    before=finding.get('human_status','unreviewed');finding['human_status']=request.human_status;finding['review_notes']=request.review_notes;finding['in_change_set']=bool(request.in_change_set)
    if request.suggested_text is not None:finding['suggested_text']=request.suggested_text
    event=_event('finding_reviewed',finding_id=finding_id,from_status=before,to_status=request.human_status,in_change_set=finding['in_change_set']);run.setdefault('review_history',[]).append(event);run.setdefault('audit',[]).append(event);store.save(run_id,run);return finding

@app.get('/api/runs/{run_id}/changes')
def changes(run_id:str):
    try:run=store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
    return {'run_id':run_id,'changes':[f for f in run.get('findings',[]) if f.get('in_change_set')]}

@app.get('/api/runs')
def list_runs():return {'runs':store.list()}

@app.get('/api/runs/{run_id}/export')
def export_run(run_id:str):
    try:run=store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
    return build_export(run)

@app.get('/api/runs/{run_id}/export.md',response_class=PlainTextResponse)
def export_run_markdown(run_id:str):
    try:run=store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
    return PlainTextResponse(export_markdown(run),media_type='text/markdown; charset=utf-8',headers={'Content-Disposition':f'attachment; filename="{run_id}-rapport.md"'})

@app.delete('/api/runs/{run_id}')
def delete_run(run_id:str):
    try:run=store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
    upload=ROOT/run.get('upload_path','')
    if upload.is_file():upload.unlink(missing_ok=True)
    (store.runs/f'{run_id}.json').unlink(missing_ok=True)
    return {'deleted':True,'run_id':run_id}

@app.get('/api/runs/{run_id}')
def get_run(run_id:str):
    try:return store.load(run_id)
    except FileNotFoundError:raise HTTPException(404,detail='Run niet gevonden.')
