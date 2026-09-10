const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'..');const h=fs.readFileSync(path.join(root,'web/index.html'),'utf8');
if(!h.includes('Zonder AI')||!h.includes('Met AI')||!h.includes('disabled title="Nog niet aangesloten"'))throw Error('AI toggle ontbreekt of is niet disabled');
for(const label of ['Nieuwe controle','Documentcheck','Volledigheid','Bronkandidaten','Vergelijking','Registers','Wijzigingen','Audit','Bronpoort / evidence-validatie','Eerdere controles','Rapport','Verwijder'])if(!h.includes(label))throw Error('v3.3 UI ontbreekt: '+label);
if(!h.includes('Review opslaan'))throw Error('reviewflow ontbreekt');
for(const marker of ['out_of_scope','loadRuns','loadRun','downloadExport','evidence_validation'])if(!h.includes(marker))throw Error('v3.3 functionaliteit ontbreekt: '+marker);
const js=h.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(js);console.log('PASS v3.3 HTML syntax, no-AI toggle, run management, export and required views');
