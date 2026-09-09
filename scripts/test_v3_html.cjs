const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'..');const h=fs.readFileSync(path.join(root,'web/index.html'),'utf8');
if(!h.includes('Zonder AI')||!h.includes('Met AI')||!h.includes('disabled title="Nog niet aangesloten"'))throw Error('AI toggle ontbreekt of is niet disabled');
for(const label of ['Nieuwe controle','Documentcheck','Bronkandidaten','Registers','Wijzigingen','Audit','Bronpoort / evidence-validatie'])if(!h.includes(label))throw Error('v3.1 UI ontbreekt: '+label);
if(!h.includes('Review opslaan'))throw Error('reviewflow ontbreekt');
const js=h.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(js);console.log('PASS v3.1 HTML syntax, no-AI toggle, reviewflow and required views');
