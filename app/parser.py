from __future__ import annotations
import hashlib, re, shutil, subprocess, uuid
from pathlib import Path
from typing import Any

PARSER_VERSION = "v3.3-parser-0.3"
YEAR_RE = re.compile(r"\b(20\d{2})\s*[-/]\s*(20\d{2})\b")
EXPLICIT_ARTICLE_RE = re.compile(r"^\s*artikel\s+(?P<num>\d{1,3}(?:\.\d+)*(?:[a-z])?)\b", re.I)
DOTTED_ARTICLE_RE = re.compile(r"^\s*(?P<num>\d{1,3}(?:\.\d+)+(?:[a-z])?)\s+(?P<title>\S.+)$", re.I)
HEADING_NUMBER_RE = re.compile(r"^\s*(?P<num>\d{1,3})(?:[.)])?\s+(?P<title>\S.+)$", re.I)
DEFINITION_RE = re.compile(r"^\s*(?P<term>[^:]{2,50})\s+(?:betekent|wordt verstaan onder)\s+(?P<definition>.+)$", re.I)
MONTHS = {"januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"}

def _sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def expected_exam_year(school_year: str | None) -> int | None:
    if not school_year:
        return None
    m=YEAR_RE.fullmatch(school_year.strip())
    if not m:
        return None
    start,end=map(int,m.groups())
    if end != start + 1:
        return None
    return end

def _is_heading_style(style: str | None) -> bool:
    return bool(style and (style.lower().startswith('heading') or style.lower().startswith('kop')))

def _kind(text: str, style: str | None = None) -> tuple[str, str | None]:
    """Conservative structure detection. Bare dates/years are never articles."""
    t=' '.join(text.split())
    if not t:
        return 'paragraph', None
    m=EXPLICIT_ARTICLE_RE.match(t)
    if m:
        return 'article', m.group('num')
    m=DOTTED_ARTICLE_RE.match(t)
    if m:
        return 'article', m.group('num')
    if _is_heading_style(style):
        m=HEADING_NUMBER_RE.match(t)
        if m:
            title=m.group('title').strip().lower()
            if title.split()[0].strip('.,') not in MONTHS and not YEAR_RE.search(t):
                return 'article', m.group('num')
        return 'section', None
    if DEFINITION_RE.match(t):
        return 'definition', None
    return 'paragraph', None

def parse_docx(path: Path) -> tuple[list[dict[str,Any]], list[dict[str,Any]]]:
    from docx import Document
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    from docx.text.paragraph import Paragraph
    from docx.table import Table
    doc=Document(path)
    units=[]; warnings=[]; order=0
    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            p=Paragraph(child, doc); text=p.text.strip()
            if not text: continue
            order+=1; style=p.style.name if p.style else None; kind,article=_kind(text,style)
            units.append({"unit_id":f"u-{order:04d}","type":kind,"text":text,"order":order,"page":None,"anchor_id":f"docx-p-{order:04d}","article":article,"style":style,"extraction_method":"docx_native","confidence":"high"})
        elif isinstance(child, CT_Tbl):
            table=Table(child, doc); rows=[]
            for row in table.rows: rows.append([cell.text.strip() for cell in row.cells])
            if not any(any(c for c in r) for r in rows): continue
            order+=1; text=' | '.join(' | '.join(r) for r in rows)
            units.append({"unit_id":f"u-{order:04d}","type":"table","text":text,"order":order,"page":None,"anchor_id":f"docx-table-{order:04d}","article":None,"rows":rows,"extraction_method":"docx_native","confidence":"high"})
    if not units: warnings.append({"code":"empty_document","message":"Geen uitleesbare tekst in DOCX gevonden.","severity":"high"})
    return units,warnings

def ocr_status() -> dict[str,Any]:
    executable=shutil.which('tesseract')
    return {
        "available":bool(executable),
        "engine":"tesseract" if executable else None,
        "reason":"Tesseract is beschikbaar voor gescande PDF-pagina's." if executable else "Tesseract is niet geïnstalleerd; tekst-PDF en DOCX blijven beschikbaar.",
    }

def _ocr_page_text(page) -> str | None:
    """OCR a rendered page through a fixed, non-shell Tesseract invocation."""
    executable=shutil.which('tesseract')
    if not executable:return None
    pix=page.get_pixmap(dpi=200,alpha=False)
    try:
        result=subprocess.run(
            [executable,'stdin','stdout','--dpi','200','--psm','6'],
            input=pix.tobytes('png'),capture_output=True,timeout=45,check=False,
        )
    except (OSError,subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:return None
    text=result.stdout.decode('utf-8',errors='replace').strip()
    return text or None

def parse_pdf(path: Path) -> tuple[list[dict[str,Any]], list[dict[str,Any]]]:
    try:
        import pymupdf as fitz
    except ImportError:  # backwards-compatible module name
        import fitz
    pdf=fitz.open(path); units=[];warnings=[];order=0
    for pno,page in enumerate(pdf, start=1):
        blocks=sorted(page.get_text('blocks'),key=lambda b:(round(b[1],1),round(b[0],1)))
        page_chars=sum(len((b[4] or '').strip()) for b in blocks)
        ocr_text=None
        if page_chars < 30:
            ocr_text=_ocr_page_text(page)
            if ocr_text and len(ocr_text) >= 30:
                warnings.append({"code":"page_ocr_used","page":pno,"message":f"Pagina {pno} bevatte weinig digitale tekst en is met OCR uitgelezen.","severity":"low"})
            else:
                available=ocr_status()['available']
                warnings.append({"code":"low_text_page" if available else "ocr_unavailable","page":pno,"message":f"Pagina {pno} bevat weinig uitleesbare tekst; OCR leverde geen betrouwbare tekst op." if available else f"Pagina {pno} bevat weinig uitleesbare tekst en Tesseract OCR is niet beschikbaar.","severity":"medium"})
        if ocr_text and len(ocr_text) >= 30:
            paragraphs=[part.strip() for part in re.split(r'\n\s*\n|\n',ocr_text) if part.strip()]
            for bidx,text in enumerate(paragraphs,start=1):
                order+=1;kind,article=_kind(text)
                units.append({"unit_id":f"u-{order:04d}","type":kind,"text":' '.join(text.split()),"order":order,"page":pno,"anchor_id":f"pdf-p{pno:03d}-ocr{bidx:03d}","article":article,"bbox":[0.0,0.0,round(page.rect.width,2),round(page.rect.height,2)],"extraction_method":"ocr_tesseract","confidence":"medium"})
            continue
        for bidx,b in enumerate(blocks,start=1):
            text=' '.join((b[4] or '').split())
            if not text: continue
            order+=1;kind,article=_kind(text)
            # Confidence here means extraction coverage signal, not semantic correctness.
            conf='high' if len(text)>=40 else ('medium' if len(text)>=12 else 'low')
            units.append({"unit_id":f"u-{order:04d}","type":kind,"text":text,"order":order,"page":pno,"anchor_id":f"pdf-p{pno:03d}-b{bidx:03d}","article":article,"bbox":[round(x,2) for x in b[:4]],"extraction_method":"pdf_text","confidence":conf})
    if not units: warnings.append({"code":"empty_document","message":"Geen uitleesbare tekst in PDF gevonden, ook niet via de beschikbare OCR-fallback.","severity":"high"})
    return units,warnings

def infer_metadata(units: list[dict[str,Any]], supplied_year: str | None = None) -> dict[str,Any]:
    texts=[u['text'] for u in units]
    title=next((u['text'] for u in units if u['type']=='section' and len(u['text'])<140), None)
    if not title: title=next((t for t in texts[:12] if 4 < len(t) < 140), 'Onbekend document')
    year=supplied_year
    if not year:
        for t in texts[:40]:
            m=YEAR_RE.search(t)
            if m: year=f"{m.group(1)}-{m.group(2)}";break
    exam_year=expected_exam_year(year)
    article_count=sum(u['type']=='article' for u in units)
    section_count=sum(u['type']=='section' for u in units)
    return {"title":title,"school_year":year,"expected_exam_year":exam_year,"article_count":article_count,"section_count":section_count}

def parse_document(path: str | Path, *, school_year: str | None=None, school_types: list[str] | None=None, document_status: str='concept') -> dict[str,Any]:
    path=Path(path); suffix=path.suffix.lower()
    if suffix=='.docx': units,warnings=parse_docx(path);mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif suffix=='.pdf': units,warnings=parse_pdf(path);mime='application/pdf'
    else: raise ValueError('Alleen PDF en DOCX worden ondersteund.')
    meta=infer_metadata(units,school_year)
    return {"document_id":"doc-"+uuid.uuid4().hex[:12],"sha256":_sha256(path),"filename":path.name,"mime_type":mime,"parser_version":PARSER_VERSION,"school_year":meta['school_year'],"school_types":school_types or [],"document_status":document_status,"parsing_status":"partial" if any(w['severity'] in {'high','medium'} for w in warnings) else 'complete',"metadata":meta,"units":units,"warnings":warnings}
