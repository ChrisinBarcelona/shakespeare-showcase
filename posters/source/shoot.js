const {chromium}=require('playwright');const jobs=require('./jobs.json');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [n,w,h] of jobs){await p.setViewportSize({width:w,height:h});await p.goto('file:///home/claude/posters/html/'+n+'.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);await p.screenshot({path:'out/'+n+'.png',clip:{x:0,y:0,width:w,height:h}});}
await b.close();})();
