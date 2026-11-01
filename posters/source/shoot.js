// Usage: node shoot.js <build dir>  ->  <build dir>/out/*.png
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const dir=path.resolve(process.argv[2]||'build');const jobs=require(path.join(dir,'jobs.json'));fs.mkdirSync(path.join(dir,'out'),{recursive:true});
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [n,w,h] of jobs){await p.setViewportSize({width:w,height:h});await p.goto('file://'+path.join(dir,'html',n+'.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);await p.screenshot({path:path.join(dir,'out',n+'.png'),clip:{x:0,y:0,width:w,height:h}});}
await b.close();})();
