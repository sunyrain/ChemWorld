// Extend the approved artwork with native data charts and spacious editable reflection text.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';

const ROOT=path.resolve(import.meta.dirname,'../..');
const RUNTIME='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=RUNTIME;
const SKILL='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(path.join(RUNTIME,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const {default:sharp}=await import(pathToFileURL(path.join(RUNTIME,'sharp/dist/index.cjs')).href);
const OUT=path.join(ROOT,'output/figures/research-case-v16');
const FINAL=path.join(ROOT,'output/pptx/c-w05-research-paths-v16.pptx');
const BUILD=path.join(os.tmpdir(),'chemworld-research-case-v16');
await fs.mkdir(BUILD,{recursive:true});await fs.mkdir(path.dirname(FINAL),{recursive:true});
const support=path.join(BUILD,'python-support');await fs.mkdir(support,{recursive:true});
await fs.symlink('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages/lxml',path.join(support,'lxml'),'junction').catch(e=>{if(e.code!=='EEXIST')throw e;});
process.env.PYTHONPATH=[support,process.env.PYTHONPATH].filter(Boolean).join(path.delimiter);
const DATA=JSON.parse(await fs.readFile(path.join(OUT,'data.json'),'utf8'));
const ART=await fs.readFile(path.join(ROOT,'output/imagegen/c-w05-research-paths-v15.png'));
const W=1800,H=3440,FONT='Arial';
const C={ink:'#24282C',muted:'#66717A',rule:'#C9D2DA',blue:'#0066DB',teal:'#009BB5',fail:'#BA6A56',light:'#D8DDE1'};
const p=Presentation.create({slideSize:{width:W,height:H}}),s=p.slides.add();s.background.fill='#FFFFFF';
const heartbeat=setInterval(()=>console.log('figure stage=authoring/export/render active'),30000);
function shape(type,x,y,w,h,fill='none',stroke='none',lw=0){return s.shapes.add({geometry:type,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:lw}});}
function text(t,x,y,w,h=40,size=26,bold=false,color=C.ink,align='left'){
 const o=shape('textbox',x,y,w,h);o.text=t;o.text.style={typeface:FONT,fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',wrap:'none',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};return o;
}
function rule(x1,y,x2,color=C.rule,width=1){shape('line',x1,y,x2-x1,0,'none',color,width);}
async function crop(left,top,width,height,x,y,w){
 const blob=await sharp(ART).extract({left,top,width,height}).png().toBuffer();
 s.images.add({blob,contentType:'image/png',position:{left:x,top:y,width:w,height:height*w/width},fit:'contain',alt:'Preserved approved illustration, cropped and uniformly scaled'});
}
// Excel workbooks store 12 significant digits; data.json retains source precision.
function series(name,x,y,color,marker='none',width=0){const digits=v=>Number(v.toPrecision(12));return {name,xValues:x.map(digits),values:y.map(digits),fill:color,line:{fill:width?color:'none',width},marker:{symbol:marker,size:9}};}
function axis(title,min,max,step,visible=true){return {visible,min,max,majorUnit:step,numberFormatCode:'0',tickLabelPosition:visible?'nextTo':'none',title:title?{text:title,textStyle:{typeface:FONT,fontSize:25,fill:C.ink}}:undefined,textStyle:{typeface:FONT,fontSize:22,fill:C.ink},line:{fill:C.muted,width:1},majorGridlines:null,minorGridlines:null};}
function chart(ser,x,y,w,h,xAxis,yAxis){const ch=s.charts.add('scatter',{position:{left:x,top:y,width:w,height:h},titlePlacement:'none',hasLegend:false,series:ser,scatterOptions:{style:'lineWithMarkers'},xAxis,yAxis,chartFill:'#FFFFFF',chartLine:{fill:'none',width:0},plotAreaFill:'#FFFFFF',plotAreaLine:{fill:'none',width:0}});applyPresentationChartFont(ch,{fontFamily:FONT});return ch;}

console.log('figure stage=layout');
await crop(0,0,1143,296,0,0,W);
text('Optimization across successive batches',35,484,1600,44,32,true);
for(let i=0;i<2;i++){
 const session=DATA.pair[i],rows=session.rows,col=i?C.teal:C.blue,x=30+i*900;
 text(`${session.budget}-batch session`,x+60,544,760,40,27,true,col);
 const good=rows.filter(r=>r.quality_feasible),bad=rows.filter(r=>!r.quality_feasible);
 const best=rows.filter(r=>r.best_feasible_recovery_pct!==null),xx=[],yy=[];
 best.forEach((r,j)=>{if(j){xx.push(r.batch);yy.push(best[j-1].best_feasible_recovery_pct);}xx.push(r.batch);yy.push(r.best_feasible_recovery_pct);});
 const recovery=[series('All observed recoveries',rows.map(r=>r.batch),rows.map(r=>r.recovery_pct),C.light,'none',1),
 series('Best feasible recovery so far',xx,yy,col,'none',2.7),
 series('Quality-feasible batch',good.map(r=>r.batch),good.map(r=>r.recovery_pct),col,'circle'),
 series('Quality-infeasible batch',bad.map(r=>r.batch),bad.map(r=>r.recovery_pct),C.fail,'x')];
 chart(recovery,x,588,855,290,axis('',0,session.budget,i?4:3,false),axis('Recovery (%)',20,65,10));
 const fines=[series('Fines limit',[0,session.budget],[50,50],C.muted,'none',1),
 series('Observed fines',rows.map(r=>r.batch),rows.map(r=>r.fines_pct),C.light,'none',1),
 series('Quality-feasible batch',good.map(r=>r.batch),good.map(r=>r.fines_pct),col,'circle'),
 series('Quality-infeasible batch',bad.map(r=>r.batch),bad.map(r=>r.fines_pct),C.fail,'x')];
 chart(fines,x,881,855,224,axis('Batch',0,session.budget,i?4:3),axis('Fines (%)',0,105,50));
 text(i?'First feasible: batch 20; best: 57.0%':'First feasible: 34.7%; best: 51.2%',x+105,1112,730,36,25,false,C.ink,'center');
}
text('●  Quality-feasible    ×  Quality-infeasible    ━  Best feasible recovery so far',160,1162,1510,34,23,false,C.ink,'center');
text('Independent sessions. Fines limit: 50%; all shown batches meet the purity threshold.',100,1203,1600,34,23,false,C.muted,'center');
rule(30,1250,1770);
const BY=1268;
await crop(0,297,1143,655,0,BY,W);
const BOTTOM=BY+655*W/1143;
text('Quench stops reaction chemistry; cooling and crystal growth can continue.',50,BOTTOM+10,1700,38,25,false,C.muted,'center');
const CY=Math.ceil(BOTTOM+76);
rule(30,CY-10,1770);
text('c',31,CY,50,58,46,true);
text('Selected recipes and independent retest',95,CY,1650,58,42,true);
for(let i=0;i<2;i++){
 const x=35+i*900,col=i?C.teal:C.blue,fill=i?'#EAF8FA':'#EDF6FF';
 shape('rect',x,CY+81,830,53,fill);
 text(i?'Selected batch 23 (24-batch campaign)':'Selected batch 10 (12-batch campaign)',x+14,CY+85,806,44,27,true);
 text('Later reflection (condensed)',x+12,CY+157,810,40,26,true);
 await crop(30,1052,65,72,x+3,CY+232,100);
 shape('roundRect',x+143,CY+215,683,204,fill,'#C4D6E1',1);
 const lines=i?['Hotter, shorter heating + staged cooling.','Batches 22–24 formed a broad','recovery plateau.']:
 ['Batch 12 had fewer fines.','Batch 10 led in measured recovery.','The small recovery gap was unresolved.'];
 lines.forEach((t,j)=>text(t,x+164,CY+242+j*48,642,40,26));
 text(i?'Observed: recovery 57.0%  |  purity 100%  |  fines 14.2%':'Observed: recovery 51.2%  |  purity 97.8%  |  fines 45.7%',x+4,CY+453,832,38,24);
}
// Preserve the original selected-recipe icons and labels, with uniform scaling.
await crop(0,1149,1143,88,0,CY+521,W);
for(let i=0;i<2;i++){
 const x=35+i*900,col=i?C.teal:C.blue,fill=i?'#EAF8FA':'#EDF6FF';
 shape('rect',x,CY+701,830,151,fill);
 text('Independent retest',x+12,CY+711,806,39,27,false,C.ink,'center');
 text('Recovery',x+45,CY+757,300,34,25,false,C.ink,'center');
 text('Fines',x+485,CY+757,300,34,25,false,C.ink,'center');
 text(i?'58.1%':'50.4%',x+45,CY+797,300,47,42,true,col,'center');
 text(i?'19.3%':'46.2%',x+485,CY+797,300,47,42,true,col,'center');
}
text('Both selected recipes meet quality constraints.',100,CY+879,1600,39,28,true,C.ink,'center');
rule(30,CY+938,1770);
text('Selected illustrative case; independent sessions. Recovery excludes seed mass. Fines: particles <20 µm.',35,CY+953,1720,32,22,false,C.muted,'center');
text('Heating values and cooling steps denote requested targets, not measured temperature trajectories.',35,CY+991,1720,32,22,false,C.muted,'center');
const actualBottom=CY+1030;
if(actualBottom>H)throw Error(`Canvas too short: ${actualBottom} > ${H}`);
s.speakerNotes.textFrame.setText(
 'Sources: workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/C-W05-B12-E-Aligned.md and C-W05-B24-E-Aligned.md. '+
 'All 36 original source batches are retained in the native charts. Feasibility: purity >=0.80, fines <=0.50, crystal size >0. Running best is undefined until first feasibility. '+
 'The 12/24 sessions are independent. Retrospective K1 accounts are not logged immediate thoughts. Quench semantics: src/chemworld/runtime/primitive_services.py, quench. '+
 'The selected illustration does not estimate a causal or population-wide budget effect.');
const stamp=Date.now(),candidate=path.join(BUILD,`candidate-${stamp}.pptx`);
console.log('figure stage=export native-charts=4');
await (await PresentationFile.exportPptx(p)).save(candidate);
const repaired=spawnSync('C:/Users/Admin/AppData/Local/Microsoft/WinGet/Links/uv.exe',['run','--no-sync','python',path.join(ROOT,'paper/tools/repair_figure_chart_markers.py'),candidate],{cwd:ROOT,encoding:'utf8'});
if(repaired.status!==0)throw Error(repaired.stderr||repaired.stdout||String(repaired.error));
const checked=path.join(BUILD,'final',`checked-${stamp}.pptx`);await fs.mkdir(path.dirname(checked),{recursive:true});
await finalizePresentation({workspaceDir:BUILD,candidatePath:candidate,finalPath:checked,
 pythonExecutable:path.join(ROOT,'.venv/Scripts/python.exe'),
 integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu',`${W*9525},${H*9525}`,'--validate-heading-fit'],
 explicitTotalSlideCount:1,requiredNativeChartOwnerSlides:[1],materializeLiteralChartWorkbooks:true,
 fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,`validation-${stamp}.json`)});
await fs.copyFile(checked,FINAL);
console.log('figure stage=render finalized-pptx');
const rendered=await PresentationFile.importPptx(await FileBlob.load(FINAL)),slide=rendered.slides.getItem(0);
const result=await rendered.export({slide,format:'png',scale:2});
const buf=Buffer.from(await result.arrayBuffer());
await fs.writeFile(path.join(OUT,'c-w05-research-paths-v16.png'),buf);
await sharp(buf).resize(W,H).png().toFile(path.join(BUILD,'preview.png'));
await fs.writeFile(path.join(BUILD,'layout.json'),await (await slide.export({format:'layout'})).text());
clearInterval(heartbeat);
console.log(JSON.stringify({pptx:FINAL,figure:path.join(OUT,'c-w05-research-paths-v16.png'),preview:path.join(BUILD,'preview.png'),canvas:[W,H],bottom:actualBottom}));
