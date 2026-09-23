import {addEqEvidence,addCrystalComparison} from './reader_figure_panels.mjs';
import {addPriorFinal,addCaseFinal,addSecondaryFinal} from './final_figure_panels.mjs';
// Preserve approved artwork while reorganizing the manuscript evidence.
import {addPreservedFigure} from "./preserved_figure_overlay.mjs";
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';

const ROOT=path.resolve(import.meta.dirname,'../..');
const caseOnly=process.argv.includes('--case-only');
const RUNTIME=process.env.CODEX_NODE_MODULES || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=RUNTIME;
const SKILL='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(path.join(RUNTIME,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const {default:sharp}=await import(pathToFileURL(path.join(RUNTIME,'sharp/dist/index.cjs')).href);
const DATA=JSON.parse(await fs.readFile(path.join(ROOT,'paper/figures/academic-ppt/retained-figure-data.json'),'utf8'));
const BUILD=path.join(os.tmpdir(),caseOnly?'chemworld-case-typography':'chemworld-final-ppt');
const OUT=path.join(ROOT,'paper/figures/final-ppt');
const DECK=path.join(ROOT,caseOnly?'output/pptx/chemworld-figure2-typography.pptx':'output/pptx/chemworld-figures-final.pptx');
await fs.mkdir(BUILD,{recursive:true}); await fs.mkdir(OUT,{recursive:true}); await fs.mkdir(path.dirname(DECK),{recursive:true});
// The packaging helper needs bundled lxml; expose only that package to the locked Python.
const pythonSupport=path.join(BUILD,'python-support');
await fs.mkdir(pythonSupport,{recursive:true});
await fs.symlink('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages/lxml',path.join(pythonSupport,'lxml'),'junction').catch(e=>{if(e.code!=='EEXIST')throw e;});
process.env.PYTHONPATH=[pythonSupport,process.env.PYTHONPATH].filter(Boolean).join(path.delimiter);
const W=1440,H=1900,FONT='Arial',FS=20,SM=18,PANEL=27;
const C={ink:'#24292D',muted:'#6A737B',grid:'#D7DDE1',light:'#EEF1F3',Opaque:'#637482',Aligned:'#277F8A',MisIndexed:'#BC7850',b12:'#416B92',b24:'#277F8A',bad:'#A35F42'};
const ARMS=['Opaque','Aligned','MisIndexed'];
const p=Presentation.create({slideSize:{width:W,height:H}});
const figures=[];
const heartbeat=setInterval(()=>console.log('ppt stage=authoring/export active'),30000);
const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;
function shape(s,type,x,y,w,h,fill='none',stroke=C.ink,lw=1.5){return s.shapes.add({geometry:type,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:lw}});}
function txt(s,t,x,y,w,h=38,size=FS,bold=false,color=C.ink,align='left'){
  const o=shape(s,'textbox',x,y,Math.min(w,W-x-20),h,'none','none',0);o.text=t;
  o.text.style={typeface:FONT,fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',wrap:'none',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};return o;
}
function line(s,x1,y1,x2,y2,color=C.ink,width=1.5,dash=false){
  const o=shape(s,'line',Math.min(x1,x2),Math.min(y1,y2),Math.max(.1,Math.abs(x2-x1)),Math.max(.1,Math.abs(y2-y1)),'none',color,width);
  if((x2-x1)*(y2-y1)<0)o.position={...o.position,verticalFlip:true};
  if(dash)o.line={fill:color,width,style:'dashed'}; return o;
}
function arrow(s,x1,y1,x2,y2,color=C.ink,width=1.5){
  line(s,x1,y1,x2,y2,color,width);const a=Math.atan2(y2-y1,x2-x1),r=9;
  line(s,x2,y2,x2-r*Math.cos(a-.5),y2-r*Math.sin(a-.5),color,width);
  line(s,x2,y2,x2-r*Math.cos(a+.5),y2-r*Math.sin(a+.5),color,width);
}
function marker(s,x,y,color,r=6,kind='circle'){
  if(kind==='x'){line(s,x-r,y-r,x+r,y+r,color,2);line(s,x-r,y+r,x+r,y-r,color,2);return;}
  return shape(s,kind==='triangle'?'triangle':'ellipse',x-r,y-r,2*r,2*r,color,color,1);
}
function panel(s,id,x,y,condition=''){txt(s,id,x,y,34,36,PANEL,true);if(condition)txt(s,condition,x+40,y,Math.min(520,condition.length*FS*.58+20),36,FS);}
function agent(s,x,y,color=C.ink){shape(s,'ellipse',x+17,y,26,26,'none',color,2);line(s,x+8,y+59,x+8,y+42,color,2);line(s,x+8,y+42,x+30,y+32,color,2);line(s,x+30,y+32,x+52,y+42,color,2);line(s,x+52,y+42,x+52,y+59,color,2);}
function box(s,t,x,y,w,h=68,color=C.ink){const b=shape(s,'rect',x,y,w,h,'#FFFFFF',color,1.5);txt(s,t,x+12,y+5,w-24,h-10,FS,false,C.ink,'center');return b;}
function notes(s,t){s.speakerNotes.textFrame.setText(t);}
function slide(name,height,note){const s=p.slides.add();s.background.fill='#FFFFFF';notes(s,note);figures.push({name,height,slide:s});return s;}
function legend(s,items,y,x=80){let cur=x;for(const [label,color,kind]of items){marker(s,cur+7,y+16,color,6,kind);txt(s,label,cur+25,y,Math.max(100,label.length*12),34,SM);cur+=40+label.length*12;}}
// Chart workbooks use 12 significant digits; full source precision stays in retained-figure-data.json.
function series(name,x,y,color=C.Aligned,kind='circle',lw=0){const digits=v=>Number(v.toPrecision(12));return {name,xValues:x.map(digits),values:y.map(digits),fill:color,line:{fill:lw?color:'none',width:lw},marker:{symbol:kind,size:8}};}
function seg(name,x,y,color=C.grid,lw=1.5){return series(name,x,y,color,'none',lw);}
function axis(title,min,max,step,fmt='0.0',visible=true){return{visible,min,max,majorUnit:step,numberFormatCode:fmt,tickLabelPosition:visible?'nextTo':'none',title:title?{text:title,textStyle:{typeface:FONT,fontSize:FS,fill:C.ink}}:undefined,textStyle:{typeface:FONT,fontSize:SM,fill:visible?C.ink:'#FFFFFF'},line:{fill:C.ink,width:1.3},majorGridlines:null,minorGridlines:null};}
function chart(s,ser,x,y,w,h,xax,yax,type='scatter',categories){
 const cfg={position:{left:x,top:y,width:w,height:h},titlePlacement:'none',hasLegend:false,series:ser,xAxis:xax,yAxis:yax,chartFill:'#FFFFFF',chartLine:{fill:'none',width:0},plotAreaFill:'#FFFFFF',plotAreaLine:{fill:'none',width:0}};
 if(type==='scatter')cfg.scatterOptions={style:'lineWithMarkers'};else{cfg.categories=categories;cfg.lineOptions={smooth:false};cfg.barOptions={direction:'column',grouping:'clustered',gapWidth:110};}
 const ch=s.charts.add(type,cfg);applyPresentationChartFont(ch,{fontFamily:FONT});return ch;
}
function rowdata(sys,goal,metric){return DATA.campaigns.filter(r=>r.system===sys&&r.goal===goal&&r.metric===metric);}
function groupedPoints(rows,xkey,ykey){return ARMS.map(arm=>{const a=rows.filter(r=>r.arm===arm);return series(arm,a.map(xkey),a.map(ykey),C[arm]);});}

const ctx={slide,panel,chart,axis,series,seg,txt,legend,DATA,C,ARMS,mean,line,ROOT,W,shape,groupedPoints};
if(caseOnly){
 await addCaseFinal(ctx,'figure02-research-paths-typography');
} else {
// Retained illustration with typography-only overlays.
figures.push(await addPreservedFigure(p,'figure01-framework',ROOT,W));
await addCaseFinal(ctx,'figure02-research-paths');

// Figure 2: matched goal changes, and the separate purification constraint.
{
const s=slide('figure03-operation-prediction',745,'Figure 3. Retained complete strategy comparisons. EC and RX have 30 matched pairs each. P has 15 recommendations. Source: integrated-results/analysis.json and campaign_metrics.csv.');
for(const [i,sys,minx,maxx,maxy,miny,xstep]of [[0,'EC',-.3,.6,.25,-.25,.3],[1,'RX',-.08,.08,.2,-.1,.04]]){
const x=25+i*720;panel(s,String.fromCharCode(97+i),x,16,sys==='EC'?'Electrochemistry':'Reaction processing');
txt(s,'Upper right: better operation, worse prediction',x+76,57,610,29,18,false,C.muted);
const points=DATA.goals.goal_contrasts[sys];
const ser=[seg('zero x',[0,0],[miny,maxy],C.grid),seg('zero y',[minx,maxx],[0,0],C.grid),...ARMS.map(a=>{const rr=points.filter(r=>r.arm===a);return series(a,rr.map(r=>r.delta_retest),rr.map(r=>r.delta_mae),C[a]);})];
chart(s,ser,x+5,90,675,440,axis('Retest gain (optimization - discovery)',minx,maxx,xstep,'0.00'),axis('Prediction error change',miny,maxy,.1,'0.00'));
const n=DATA.goals.goal_counts[sys];txt(s,`Retest improves: ${n.better_retest}/30`,x+77,548,370,32,SM);txt(s,`Prediction improves: ${n.lower_mae}/30`,x+77,580,370,32,SM);
txt(s,`Better retest + worse prediction: ${points.filter(r=>r.delta_retest>0&&r.delta_mae>0).length}/30`,x+77,619,610,33,20,true,C.bad);
}
legend(s,ARMS.map(a=>[a,C[a]]),692,440);
}

// Budget comparisons: selected main outcomes and complete supplemental view.
function addBudget(full=false) {
const s=slide(full?'figureS3-budget-detail':'figure04-research-envelope',1060,'Budget effects. All 90 response comparisons in 15 matched independent 12/24 pairs per panel. Positive change denotes lower MAE, higher coverage or higher recovery. Native editable data marks. Source shortfalls are retained and crossed. Complete response detail remains in the supplementary view. Source: campaign_metrics.csv.');
const allDefs=[['EC','discovery','score','mae','Electrochemistry\nDiscovery','Score MAE'],['EC','optimization','score','mae','Electrochemistry\nOptimization','Score MAE'],['PA','discovery','product_in_organic','mae','Partitioning','Organic-fraction\nMAE'],['C','delivery','crystal_yield','mae','Crystallization\nRecovery prediction','Recovery MAE'],['C','delivery','crystal_fines_fraction','coverage','Crystallization\nInterval coverage','Fines coverage (%)'],['C','delivery','crystal_yield','retest','Crystallization\nOperating delivery','Retested recovery']];
const defs=full?allDefs:[allDefs[0],allDefs[2],allDefs[3],allDefs[5]];
txt(s,'Mean, 12',20,173,125,30,SM);txt(s,'Mean, 24',20,212,125,30,SM);txt(s,'Improved',20,252,125,30,SM,true);
const yy=j=>350+Math.floor(j/3)*98+(j%3)*26;
for(let w=0;w<5;w++){txt(s,`World ${w+1}`,15,yy(w*3)+14,103,35,SM);ARMS.forEach((a,j)=>txt(s,['O','A','M'][j],119,yy(w*3+j)-16,30,32,SM));line(s,15,yy(w*3)+74,1410,yy(w*3)+74,C.grid,1);}
txt(s,'Mean change',15,855,138,32,SM,true);
defs.forEach(([sys,g,m,field,cond,label],i)=>{
const x=full?163+i*207:182+i*305,w=full?180:275,mid=x+w/2;txt(s,String.fromCharCode(97+i),x,12,40,36,PANEL,true);txt(s,cond,x-8,52,w+16,69,SM,true,C.ink,'center');txt(s,label,x-8,119,w+16,48,SM,false,C.muted,'center');
const pairs=new Map();rowdata(sys,g,m).forEach(r=>{const key=r.world+r.arm;if(!pairs.has(key))pairs.set(key,{});pairs.get(key)[r.budget]=r;});
const vals=[...pairs.values()].sort((a,b)=>a[12].world.localeCompare(b[12].world)||ARMS.indexOf(a[12].arm)-ARMS.indexOf(b[12].arm));if(vals.length!==15)throw Error('pair count');
const sc=field==='coverage'?100:1,dir=field==='mae'?-1:1,changes=vals.map(a=>dir*(a[24][field]-a[12][field])*sc),means=[12,24].map(b=>mean(vals.map(a=>a[b][field]*sc))),fmt=v=>field==='coverage'?v.toFixed(1)+'%':v.toFixed(4);
txt(s,fmt(means[0]),x,172,w,32,FS,false,C.b12,'center');txt(s,fmt(means[1]),x,211,w,32,FS,false,C.b24,'center');txt(s,`${changes.filter(v=>v>1e-12).length}/15`,x,251,w,32,FS,true,C.ink,'center');line(s,x,300,x+w,300,C.grid);
const step=field==='coverage'?25:.1,lim=sys==='EC'?.3:Math.ceil(Math.max(...changes.map(Math.abs))/step)*step,px=v=>mid+(v/lim)*(w/2-10);
line(s,mid,330,mid,895,C.muted,1.2);
changes.forEach((d,j)=>{const color=d>1e-12?C.Aligned:d< -1e-12?C.bad:C.muted,y=yy(j);line(s,mid,y,px(d),y,color,2);marker(s,px(d),y,color,4.5,(!vals[j][12].conforming||!vals[j][24].conforming)?'x':'circle');});
line(s,mid,871,px(mean(changes)),871,C.ink,2.5);shape(s,'diamond',px(mean(changes))-6,865,12,12,C.ink,C.ink,1);
line(s,x,905,x+w,905,C.ink,1.3);[-lim,0,lim].forEach(v=>{line(s,px(v),905,px(v),913,C.ink,1);txt(s,v===0?'0':(v>0?'+':'')+v.toFixed(field==='coverage'?0:1),px(v)-35,917,70,30,SM,false,C.ink,'center');});
txt(s,field==='mae'?(full?'MAE reduction':'Prediction error\nreduction'):field==='coverage'?'Coverage gain\n(percentage points)':'Recovery gain',x-8,950,w+16,58,SM,false,C.ink,'center');
});
legend(s,[['Favorable',C.Aligned],['Unfavorable',C.bad],['Source shortfall',C.muted,'x']],1020,350);
}

addBudget();

addEqEvidence(ctx);
addCrystalComparison(ctx);

// Extended figure S2: the same 16 system-specific panels as the existing supplement.
{
const s=slide('figureS1-prior-overview',1350,'Supplementary Figure S1. Complete prior overview, retaining the existing 16 selected readouts. Five matched worlds per panel, with all 240 campaigns retained in the tables. Source: campaign_metrics.csv. Scales differ.');
const defs=[['EC','E','discovery',12,'score'],['EC','E','discovery',24,'score'],['EC','E','optimization',12,'score'],['EC','E','optimization',24,'score'],['PA','E','discovery',12,'product_in_organic'],['PA','E','discovery',24,'product_in_organic'],['RX','P','discovery',12,'macro'],['RX','S','discovery',12,'macro'],['RX','P','optimization',12,'macro'],['RX','S','optimization',12,'macro'],['EQ','P','characterization',12,'macro'],['EQ','S','characterization',12,'macro'],['C','E','delivery',12,'crystal_fines_fraction'],['C','E','delivery',24,'crystal_fines_fraction'],['P','E','delivery',12,'purity'],['P','E','delivery',12,'recovery']];
defs.forEach(([sys,locus,goal,b,metric],i)=>{const x=20+(i%4)*358,y=12+Math.floor(i/4)*325;const rr=(metric==='macro'?DATA.macro_campaigns:DATA.campaigns).filter(r=>r.system===sys&&r.locus===locus&&r.goal===goal&&r.budget===b&&r.metric===metric);const worlds=[...new Set(rr.map(r=>r.world))].sort();if(rr.length!==15)throw Error('prior overview denominator');
txt(s,`${sys}/${locus}, ${goal==='optimization'?'opt.':goal==='discovery'?'disc.':goal==='characterization'?'char.':'delivery'}, ${b}`,x+35,y,318,32,SM);const lab=metric==='macro'?'Macro MAE':metric==='product_in_organic'?'Organic-fraction MAE':metric==='crystal_fines_fraction'?'Fines MAE':metric==='score'?'Score MAE':metric==='purity'?'Purity MAE':'Recovery MAE';txt(s,lab,x+35,y+34,318,30,SM,false,C.muted);
const ser=worlds.map(w=>seg(w,[0,1,2],ARMS.map(a=>rr.find(r=>r.world===w&&r.arm===a).mae),C.grid,1.2));
ARMS.forEach((a,j)=>{const vv=worlds.map(w=>rr.find(r=>r.world===w&&r.arm===a).mae);ser.push(series(a,vv.map(()=>j),vv,C[a]));});
const max=Math.max(...rr.map(r=>r.mae))*1.1;chart(s,ser,x,y+68,346,205,axis('',-.5,2.5,1,'0',false),axis('',0,max,undefined,'0.00'));
['O','A','M'].forEach((a,j)=>txt(s,a,x+83+j*88,y+286,52,30,SM,false,C.ink,'center'));
});legend(s,ARMS.map(a=>[a,C[a]]),1310,440);
}

addPriorFinal(ctx,'figureS2-prior-detail');
addBudget(true);
const reflection=await addPreservedFigure(p,'figure07-posttest-reflection',ROOT,W);
reflection.name='figureS4-posttest-reflection'; figures.push(reflection);
addSecondaryFinal(ctx);
}

const stamp=Date.now(); const candidate=path.join(BUILD,`candidate-${stamp}.pptx`);
console.log(`ppt stage=export slides=${figures.length}`);
await (await PresentationFile.exportPptx(p)).save(candidate);
// Explicit marker fills prevent PowerPoint from inheriting a no-line fill for points.
const repaired=spawnSync('C:/Users/Admin/AppData/Local/Microsoft/WinGet/Links/uv.exe',['run','--no-sync','python',path.join(ROOT,'paper/tools/repair_figure_chart_markers.py'),candidate],{cwd:ROOT,encoding:'utf8'});
if(repaired.status!==0)throw Error(repaired.stderr||String(repaired.error)||'Chart marker repair failed');
await fs.writeFile(path.join(BUILD,'figures.proto.json'),JSON.stringify(p.toProto()));
// The native package is the editing master. Finalizer preserves editable chart data.
const checked=path.join(BUILD,'final',`checked-${stamp}.pptx`);
await fs.mkdir(path.dirname(checked),{recursive:true});
await finalizePresentation({workspaceDir:BUILD,candidatePath:candidate,finalPath:checked,
 pythonExecutable:path.join(ROOT,'.venv/Scripts/python.exe'),
 integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu',`${W*9525},${H*9525}`,'--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:caseOnly?1:11,requiredNativeChartOwnerSlides:caseOnly?[1]:[2,3,5,6,7,8,11],
 materializeLiteralChartWorkbooks:true,nativeChartTargetApplication:'portable',
 fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,`validation-${stamp}.json`)});
await fs.copyFile(checked,DECK);
console.log(`ppt stage=finalized slides=${figures.length}`);
await fs.writeFile(path.join(OUT,caseOnly?'case-typography-export.json':'style-and-export.json'),JSON.stringify({fontFamily:FONT,fontSizePx:FS,tickSizePx:SM,panelSizePx:caseOnly?30*W/1448:PANEL,widthPx:W,slideHeightPx:H,palette:C,pptx:path.relative(ROOT,DECK),figures:figures.map(({name,height})=>({name,height})),renderSource:'finalized PPTX',illustrations:'original raster art with editable text overlays',rasterScale:3,newScientificExperiments:0},null,2)+'\n');
clearInterval(heartbeat);
console.log('ppt done '+DECK);
