from __future__ import annotations
import json,time,uuid
from pathlib import Path

class RunStore:
    def __init__(self,root:Path):
        self.root=root;self.uploads=root/'runtime/uploads';self.runs=root/'runtime/runs';self.uploads.mkdir(parents=True,exist_ok=True);self.runs.mkdir(parents=True,exist_ok=True)
    def new_id(self):return 'run-'+uuid.uuid4().hex[:12]
    def upload_path(self,run_id,filename):
        safe=''.join(c for c in Path(filename).name if c.isalnum() or c in '._-') or 'document'
        return self.uploads/f'{run_id}-{safe}'
    def save(self,run_id,data):
        data['updated_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(self.runs/f'{run_id}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    def load(self,run_id):return json.loads((self.runs/f'{run_id}.json').read_text())
    def list(self):
        rows=[]
        for path in self.runs.glob('run-*.json'):
            try:data=json.loads(path.read_text())
            except (OSError,json.JSONDecodeError):continue
            rows.append({"run_id":data.get('run_id'),"filename":(data.get('document') or {}).get('filename'),"status":data.get('status'),"school_year":data.get('school_year'),"school_types":(data.get('confirmed_context') or data.get('document') or {}).get('school_types',[]),"finding_count":len(data.get('findings') or []),"updated_at":data.get('updated_at')})
        return sorted(rows,key=lambda row:row.get('updated_at') or '',reverse=True)
