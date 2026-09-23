// Editable figure masters for the English article. No generated raster artwork.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';

const ROOT=path.resolve(import.meta.dirname,'../..');
const RUNTIME=process.env.CODEX_NODE_MODULES || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=RUNTIME;
const SKILL='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(path.join(RUNTIME,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const {default:sharp}=await import(pathToFileURL(path.join(RUNTIME,'sharp/dist/index.cjs')).href);
const DATA=JSON.parse(await fs.readFile(path.join(ROOT,'paper/figures/academic-ppt/retained-figure-data.json'),'utf8'));
const BUILD=path.join(os.tmpdir(),'chemworld-academic-ppt');
const OUT=path.join(ROOT,'paper/figures/academic-ppt');
const DECK=path.join(ROOT,'output/pptx/chemworld-academic-figures.pptx');
await fs.mkdir(BUILD,{recursive:true}); await fs.mkdir(path.dirname(DECK),{recursive:true});
// The packaging helper needs bundled lxml; expose only that package to the locked Python.
const pythonSupport=path.join(BUILD,'python-support');
await fs.mkdir(pythonSupport,{recursive:true});
await fs.symlink('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages/lxml',path.join(pythonSupport,'lxml'),'junction').catch(e=>{if(e.code!=='EEXIST')throw e;});
process.env.PYTHONPATH=[pythonSupport,process.env.PYTHONPATH].filter(Boolean).join(path.delimiter);
const W=1440,H=1360,FONT='Arial',FS=23,SM=20,PANEL=29;
const C={ink:'#24292D',muted:'#6A737B',grid:'#D7DDE1',light:'#EEF1F3',Opaque:'#637482',Aligned:'#277F8A',MisIndexed:'#BC7850',b12:'#416B92',b24:'#277F8A',bad:'#A35F42'};
const ARMS=['Opaque','Aligned','MisIndexed'];
const p=Presentation.create({slideSize:{width:W,height:H}});
const figures=[];
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

// Figure 1: the framework is a functional diagram, without pictorial decoration.
{
const s=slide('figure01-framework',950,'Figure 1. Original agent research and independent assessment. Source: English article Methods and retained 240-campaign programme. No internal reasoning is reconstructed.');
panel(s,'a',30,20);
const q=box(s,'Research\nquestion',75,120,170,100);
agent(s,295,130);txt(s,'Agent',278,203,96,30,FS,false,C.ink,'center');
box(s,'Choose\nconditions',418,120,192,100);box(s,'Execute\noperations',677,120,192,100);box(s,'Observe\nresponses',936,120,192,100);
arrow(s,245,170,285,170);arrow(s,358,170,418,170);arrow(s,610,170,677,170);arrow(s,869,170,936,170);
line(s,1032,120,1032,75,C.Aligned,2);line(s,1032,75,325,75,C.Aligned,2);arrow(s,325,75,325,123,C.Aligned,2);txt(s,'Next experiment',564,32,270,35,FS,false,C.Aligned,'center');
txt(s,'Persistent physical state',423,270,550,35,FS,true);
txt(s,'Composition     Phase     Thermal history     Remaining material',423,309,850,38,FS);
line(s,430,355,1300,355,C.grid,1);txt(s,'Private process laws',450,375,400);txt(s,'Public operations and instruments',450,420,520);txt(s,'Resource ledger and exact replay',450,465,520);
txt(s,'Evaluator only',1040,375,270,38,SM,false,C.muted);txt(s,'Agent access',1040,420,270,38,SM,false,C.muted);txt(s,'Recorded history',1040,465,270,38,SM,false,C.muted);
panel(s,'b',30,550);txt(s,'Information',75,550,300);legend(s,ARMS.map(a=>[a,C[a]]),599,80);txt(s,'Same physical world',75,650,440,35,FS);
txt(s,'Independent resource conditions',690,550,690);txt(s,'12 batches',727,610,250,45,FS,false,C.b12);txt(s,'24 batches',1050,610,260,45,FS,false,C.b24);txt(s,'Experimental and computational allowances',690,657,685,35,FS);
panel(s,'c',30,743);box(s,'Seal recommendation',75,798,330,68);arrow(s,405,832,454,832);box(s,'Independent retest',455,798,290,68,C.Aligned);
box(s,'K1\nAccount',785,753,165,108);box(s,'Q\nPredictions',994,753,165,108);box(s,'K2\nReflection',1203,753,165,108);arrow(s,950,808,994,808);arrow(s,1159,808,1203,808);
txt(s,'Operating performance',163,885,480,35,FS,false,C.Aligned);txt(s,'Full original context; no target feedback; Q remains sealed',776,885,620,35,SM);
}

// Figure 2: matched goal changes, and the separate purification constraint.
{
const s=slide('figure02-operation-prediction',700,'Figure 2. Retained complete strategy comparisons. EC and RX have 30 matched pairs each. P has 15 recommendations. Source: integrated-results/analysis.json and campaign_metrics.csv.');
for(const [i,sys,minx,maxx,maxy,miny,xstep]of [[0,'EC',-.3,.6,.25,-.25,.3],[1,'RX',-.08,.08,.2,-.1,.04]]){
const x=25+i*480;panel(s,String.fromCharCode(97+i),x,16,sys==='EC'?'Electrochemistry':'Reaction processing');
const points=DATA.goals.goal_contrasts[sys];
const ser=[seg('zero x',[0,0],[miny,maxy],C.grid),seg('zero y',[minx,maxx],[0,0],C.grid),...ARMS.map(a=>{const rr=points.filter(r=>r.arm===a);return series(a,rr.map(r=>r.delta_retest),rr.map(r=>r.delta_mae),C[a]);})];
chart(s,ser,x+5,90,455,440,axis('Retest-score change',minx,maxx,xstep,'0.00'),axis('Prediction MAE change',miny,maxy,.1,'0.00'));
const n=DATA.goals.goal_counts[sys];txt(s,`Retest improves: ${n.better_retest}/30`,x+77,548,370,32,SM);txt(s,`Prediction improves: ${n.lower_mae}/30`,x+77,580,370,32,SM);
}
panel(s,'c',985,16,'Purification');const rr=rowdata('P','delivery','recovery');
const ser=[seg('Purity threshold',[-.02,.9],[.8,.8],C.ink),...ARMS.map(a=>{const r=rr.filter(v=>v.arm===a);return series(a,r.map(v=>v.retest),r.map(v=>v.retest_purity),C[a]);})];
chart(s,ser,990,90,430,440,axis('Original-charge recovery',0,.9,.3,'0.0'),axis('Retested purity',0,1,.2,'0.0'));
txt(s,'Purity threshold = 0.80',1033,548,390,32,SM);txt(s,'Eligible: 0/5, 3/5, 0/5',1033,580,390,32,SM);legend(s,ARMS.map(a=>[a,C[a]]),644,440);
}

// Figure 3: aligned paired changes. Native editable marks retain all 90 comparisons.
{
const s=slide('figure03-research-envelope',1060,'Figure 3. All 90 response comparisons in 15 matched independent 12/24 pairs per panel. Positive change denotes lower MAE, higher coverage or higher recovery. Native editable data marks. Source shortfalls are retained and crossed. Source: campaign_metrics.csv.');
const defs=[['EC','discovery','score','mae','Electrochemistry\nDiscovery','Score MAE'],['EC','optimization','score','mae','Electrochemistry\nOptimization','Score MAE'],['PA','discovery','product_in_organic','mae','Partitioning','Organic-fraction\nMAE'],['C','delivery','crystal_yield','mae','Crystallization\nRecovery prediction','Recovery MAE'],['C','delivery','crystal_fines_fraction','coverage','Crystallization\nInterval coverage','Fines coverage (%)'],['C','delivery','crystal_yield','retest','Crystallization\nOperating delivery','Retested recovery']];
txt(s,'Mean, 12',20,173,125,30,SM);txt(s,'Mean, 24',20,212,125,30,SM);txt(s,'Improved',20,252,125,30,SM,true);
const yy=j=>350+Math.floor(j/3)*98+(j%3)*26;
for(let w=0;w<5;w++){txt(s,`World ${w+1}`,15,yy(w*3)+14,103,35,SM);ARMS.forEach((a,j)=>txt(s,['O','A','M'][j],119,yy(w*3+j)-16,30,32,SM));line(s,15,yy(w*3)+74,1410,yy(w*3)+74,C.grid,1);}
txt(s,'Mean change',15,855,138,32,SM,true);
defs.forEach(([sys,g,m,field,cond,label],i)=>{
const x=163+i*207,w=180,mid=x+w/2;txt(s,String.fromCharCode(97+i),x,12,40,36,PANEL,true);txt(s,cond,x-8,52,w+16,69,SM,true,C.ink,'center');txt(s,label,x-8,119,w+16,48,SM,false,C.muted,'center');
const pairs=new Map();rowdata(sys,g,m).forEach(r=>{const key=r.world+r.arm;if(!pairs.has(key))pairs.set(key,{});pairs.get(key)[r.budget]=r;});
const vals=[...pairs.values()].sort((a,b)=>a[12].world.localeCompare(b[12].world)||ARMS.indexOf(a[12].arm)-ARMS.indexOf(b[12].arm));if(vals.length!==15)throw Error('pair count');
const sc=field==='coverage'?100:1,dir=field==='mae'?-1:1,changes=vals.map(a=>dir*(a[24][field]-a[12][field])*sc),means=[12,24].map(b=>mean(vals.map(a=>a[b][field]*sc))),fmt=v=>field==='coverage'?v.toFixed(1)+'%':v.toFixed(4);
txt(s,fmt(means[0]),x,172,w,32,FS,false,C.b12,'center');txt(s,fmt(means[1]),x,211,w,32,FS,false,C.b24,'center');txt(s,`${changes.filter(v=>v>1e-12).length}/15`,x,251,w,32,FS,true,C.ink,'center');line(s,x,300,x+w,300,C.grid);
const step=field==='coverage'?25:.1,lim=i<2?.3:Math.ceil(Math.max(...changes.map(Math.abs))/step)*step,px=v=>mid+(v/lim)*(w/2-10);
line(s,mid,330,mid,895,C.muted,1.2);
changes.forEach((d,j)=>{const color=d>1e-12?C.Aligned:d< -1e-12?C.bad:C.muted,y=yy(j);line(s,mid,y,px(d),y,color,2);marker(s,px(d),y,color,4.5,(!vals[j][12].conforming||!vals[j][24].conforming)?'x':'circle');});
line(s,mid,871,px(mean(changes)),871,C.ink,2.5);shape(s,'diamond',px(mean(changes))-6,865,12,12,C.ink,C.ink,1);
line(s,x,905,x+w,905,C.ink,1.3);[-lim,0,lim].forEach(v=>{line(s,px(v),905,px(v),913,C.ink,1);txt(s,v===0?'0':(v>0?'+':'')+v.toFixed(field==='coverage'?0:1),px(v)-35,917,70,30,SM,false,C.ink,'center');});
txt(s,field==='mae'?'MAE reduction':field==='coverage'?'Coverage gain\n(percentage points)':'Recovery gain',x-8,950,w+16,58,SM,false,C.ink,'center');
});
legend(s,[['Favorable',C.Aligned],['Unfavorable',C.bad],['Source shortfall',C.muted,'x']],1020,350);
}

// Figure 4: retained case, editable operation diagrams rather than an image poster.
{
const s=slide('figure04-research-paths',1245,'Figure 4. Retrospectively selected C-W05 Aligned pair. Separate 12/24 sessions. Source: C-W05-B12-E-Aligned.md and C-W05-B24-E-Aligned.md. Considerations marked * are illustrative reconstructions, not logged contemporaneous reasons. Recovery excludes seed mass. Heating temperatures are requested targets.');
panel(s,'a',30,18);txt(s,'12 batches',93,18,530,40,FS,true,C.b12);txt(s,'24 batches',804,18,530,40,FS,true,C.b24);
const phases=[[[1,4,'Catalysts'],[5,7,'Solvents'],[8,10,'Cooling'],[11,11,'Seed'],[12,12,'Measure']],[[1,6,'Materials'],[7,18,'Process'],[19,19,'Heating'],[20,20,'Heat + cool'],[21,24,'Refine']]];
for(let k=0;k<2;k++){const x=90+k*712,col=k?C.b24:C.b12;line(s,x+15,118,x+547,118,col,2);phases[k].forEach(([a,b,t],j)=>{const px=x+j*128;marker(s,px+18,118,col);txt(s,a===b?String(a):`${a}-${b}`,px-10,69,94,32,SM,false,C.ink,'center');txt(s,t,px-20,135,120,32,SM,false,C.ink,'center');});txt(s,k?'5/24 quality-feasible':'10/12 quality-feasible',x,195,550,34,FS);txt(s,k?'First feasible: batch 20':'First feasible: batch 1',x,232,550,34,SM);}
line(s,30,292,1410,292,C.grid);
panel(s,'b',30,319);txt(s,'Batches 9-10',95,319,500,38,FS,true);txt(s,'Batches 19-20',807,319,500,38,FS,true);
for(let k=0;k<2;k++){const x=90+k*712,col=k?C.b24:C.b12;txt(s,'Observed',x,373,160,36,SM,true);txt(s,k?'Recovery 49.0%    Fines 52.8%':'Recovery 49.8%    Fines 42.4%',x+160,373,480,36,FS);txt(s,k?'Fines exceed limit':'Quality passes',x+160,414,460,32,SM,false,k?C.bad:col);agent(s,x+10,479,col);txt(s,k?'Change heating and cooling?*':'Try a colder endpoint?*',x+104,483,535,42,FS);arrow(s,x+55,551,x+55,587,col);
txt(s,'Next batch',x,604,195,36,SM,true);
if(!k){txt(s,'Cooling endpoint',x+190,593,390,32,SM);txt(s,'260 K',x+190,638,135,38,FS);arrow(s,x+320,658,x+375,658,col);txt(s,'250 K',x+394,638,160,38,FS,true,col);txt(s,'Other settings unchanged',x+190,688,430,33,SM);}
else{txt(s,'Heating: 390 K / 30 min to 410 K / 20 min',x+10,652,620,35,SM);txt(s,'Cooling: direct to staged',x+10,695,630,35,SM);const xx=x+390,yy=707;line(s,xx,yy-33,xx+40,yy-33,col,2);line(s,xx+40,yy-33,xx+40,yy-12,col,2);line(s,xx+40,yy-12,xx+90,yy-12,col,2);line(s,xx+90,yy-12,xx+90,yy+10,col,2);line(s,xx+90,yy+10,xx+145,yy+10,col,2);txt(s,'320 / 290 / 260 K',xx-15,739,236,32,SM);}
const ops=k?['Heat','Quench','Seed','Cool','Hold','Filter','Assay']:['Cool','Hold','Filter','Assay'];const step=610/ops.length;line(s,x+step/2,797,x+610-step/2,797,col,1.3);ops.forEach((op,j)=>{marker(s,x+(j+.5)*step,797,col,3);txt(s,op,x+j*step,805,step,30,SM,false,C.ink,'center');});txt(s,k?'Recovery 52.9%    Fines 21.5%':'Recovery 51.2%    Fines 45.7%',x,858,625,38,FS,true,col);}
txt(s,'* Illustrative consideration; immediate decision reasons were not recorded.',91,913,1290,35,SM,false,C.muted);line(s,30,969,1410,969,C.grid);
panel(s,'c',30,990);txt(s,'Selected batch 10',95,990,610,38,FS,true);txt(s,'Selected batch 23',807,990,610,38,FS,true);
txt(s,'S1 / C3     360 K, 60 min     Seed 20 mg',91,1040,630,33,SM);txt(s,'Direct cooling to 250 K',91,1081,630,33,SM);
txt(s,'S2 / C1     450 K, 15 min     Seed 50 mg',803,1040,630,33,SM);txt(s,'Staged cooling: 310 / 280 / 250 K',803,1081,630,33,SM);
txt(s,'Independent retest',91,1130,630,33,SM);txt(s,'Independent retest',803,1130,630,33,SM);txt(s,'Recovery 50.4%    Fines 46.2%',91,1175,630,38,FS,true,C.b12);txt(s,'Recovery 58.1%    Fines 19.3%',803,1175,630,38,FS,true,C.b24);
}

// Figure 5: all fifteen original EQ sessions remain visible, not a replacement reader task.
{
const s=slide('figure05-prior-regimes',1140,'Figure 5. Post hoc dilution groups and all 15 original EQ/P sessions. Source: STORY_WORLD_ANALYSIS.json and EQ_AUTONOMOUS_PROCESS.json. Q08 references are five-observation means. Source ranges use public dissociation observations.');
for(let i=0;i<2;i++){const x=25+i*720;panel(s,i?'b':'a',x,20);const key=i?'coverage':'mae',scale=i?100:1,ser=[];
['other_nine','three_most_dilute'].forEach((g,gi)=>ARMS.forEach((a,ai)=>{const xx=gi+1+(ai-1)*.18,rr=DATA.regimes.cells.filter(r=>r.arm===a),mm=mean(rr.map(r=>r.groups[g][key]*scale));ser.push(series(a+' '+g,rr.map((_,j)=>xx+(j-2)*.018),rr.map(r=>r.groups[g][key]*scale),C[a]));ser.push(seg('Mean '+a+' '+g,[xx-.065,xx+.065],[mm,mm],C[a],3));}));
if(i)ser.unshift(seg('Nominal 80%',[.5,2.5],[80,80],C.muted,1.3));
chart(s,ser,x+20,65,670,410,axis('',.5,2.5,1,'0',false),axis(i?'Interval coverage (%)':'Macro MAE',0,i?100:.2,i?20:.05,i?'0':'0.00'));
txt(s,'Other nine',x+156,480,200,32,SM,false,C.ink,'center');txt(s,'Dilute three',x+438,480,200,32,SM,false,C.ink,'center');
if(i)txt(s,'Reference line: nominal 80%',x+130,522,540,32,SM);else txt(s,'Points: five worlds; short lines: means',x+130,522,560,32,SM);
}
legend(s,ARMS.map(a=>[a,C[a]]),560,440);
const worlds=[...new Set(DATA.eq_process.map(r=>r.world))].sort();
worlds.forEach((world,j)=>{const x=25+j*284;panel(s,String.fromCharCode(99+j),x,637,`World ${j+1}`);const rows=ARMS.map(a=>DATA.eq_process.find(r=>r.world===world&&r.arm===a)),ser=[];
const target=rows[0].q08.reference_means.acid_dissociation_fraction;ser.push(seg('Reference',[-.3,2.3],[target,target],C.ink,2));
rows.forEach((r,i)=>{const v=r.q08.predictions.acid_dissociation_fraction;ser.push(seg('Source range '+r.arm,[i,i],r.source_dissociation_range,C.grid,14));ser.push(seg('80% interval '+r.arm,[i,i],[v.lower80,v.upper80],C[r.arm],2));ser.push(series(r.arm,[i],[v.estimate],C[r.arm]));});
chart(s,ser,x,699,275,338,axis('',-.45,2.45,1,'0',false),axis(j===0?'Dissociation fraction':'',0,1,.25,'0.00'));
});
txt(s,'Information conditions use the same colors throughout',55,1040,1320,35,SM,false,C.ink,'center');
line(s,75,1100,117,1100,C.ink,2);txt(s,'Reference mean',130,1080,285,36,SM);line(s,440,1100,484,1100,C.grid,12);txt(s,'Observed source range',499,1080,365,36,SM);txt(s,'Prediction and 80% interval',970,1080,440,36,SM);
}

// Figure 6: quantitative errors and a clearly conceptual applicability matrix.
{
const s=slide('figure06-preserve-revise',1090,'Figure 6. All 30 crystallization campaigns. Public-mean references use each original campaign only. Source: BASELINE_REANALYSIS.json. The applicability matrix is conceptual, not a measured classifier or frequency estimate.');
const defs=[['crystal_yield','Recovery',.45,.15],['crystal_purity','Purity',.14,.05],['crystal_size','Size index',.22,.1],['crystal_fines_fraction','Fines',.55,.25]];
defs.forEach(([m,label,lim,step],i)=>{const x=25+i*350;panel(s,String.fromCharCode(97+i),x,20,label);
const rr=DATA.crystal,xx=r=>r.public_baselines.mae.public_mean[m],yy=r=>r.agent_mae[m];const ser=[seg('Equal error',[0,lim],[0,lim],C.grid),...groupedPoints(rr,xx,yy)];
chart(s,ser,x+5,80,340,388,axis('Source-mean MAE',0,lim,step,'0.00'),axis('Agent MAE',0,lim,step,'0.00'));
txt(s,`${rr.filter(r=>yy(r)<xx(r)).length}/30 lower error`,x+77,482,290,32,SM);
});
panel(s,'e',25,575);const groups=[DATA.crystal.map(r=>r.response_diagnostics.crystal_purity.source_observed_mean),DATA.crystal.map(r=>r.response_diagnostics.crystal_purity.reference_mean),...([12,24].map(b=>DATA.crystal.filter(r=>r.budget===b).map(r=>r.response_diagnostics.crystal_purity.prediction_mean)))];
const col=[C.muted,C.ink,C.b12,C.b24],ser=[];groups.forEach((v,i)=>{ser.push(series('Purity group '+i,v.map((_,j)=>i+(j/(v.length-1)-.5)*.26),v,col[i]));ser.push(seg('Mean '+i,[i-.2,i+.2],[mean(v),mean(v)],col[i],3));});
chart(s,ser,40,630,655,347,axis('',-.5,3.5,1,'0',false),axis('Campaign mean purity',.84,1,.04,'0.00'));
['Source','Reference','12 batches','24 batches'].forEach((label,i)=>txt(s,label,135+i*137,970,137,35,SM,false,C.ink,'center'));txt(s,'335/360 point forecasts below reference',92,1028,610,34,SM);
panel(s,'f',745,575);txt(s,'Forecast preserves',930,644,235,54,SM,false,C.ink,'center');txt(s,'Forecast changes',1180,644,235,54,SM,false,C.ink,'center');
txt(s,'Reference\nstays near\nsource',752,725,166,110,SM);txt(s,'Reference\nleaves source\nregime',752,875,166,110,SM);
line(s,920,705,1410,705,C.grid);line(s,920,850,1410,850,C.grid);line(s,920,1000,1410,1000,C.grid);line(s,920,705,920,1000,C.grid);line(s,1165,705,1165,1000,C.grid);line(s,1410,705,1410,1000,C.grid);
txt(s,'Appropriate\npreservation',932,739,221,79,FS,false,C.Aligned,'center');txt(s,'Unnecessary change\nCrystal purity',1180,735,220,88,SM,false,C.bad,'center');txt(s,'Unwarranted extension\nDilute equilibrium',928,887,235,88,SM,false,C.bad,'center');txt(s,'Appropriate\nchange',1190,887,210,88,FS,false,C.Aligned,'center');txt(s,'Conceptual interpretation',952,1028,423,34,SM,false,C.muted,'center');
legend(s,ARMS.map(a=>[a,C[a]]),528,440);
}

// Figure 7: retain the order Q -> K2, and distinguish a proposed test from truth.
{
const s=slide('figure07-posttest-reflection',1210,'Figure 7. Same selected C-W05 original sessions. Q predicts fines 17% to 12% and 49% to 35%. Later K2 notes are condensed public answers, without reference feedback. The cooling substitution is proposed, not executed. Evaluator reference 35% to 100% concerns the reheating question only.');
panel(s,'a',30,18);txt(s,'Low-temperature hold',120,20,530,38,FS);txt(s,'Reheat and recool',840,20,530,38,FS);
line(s,145,153,660,153,C.b12,2);txt(s,'278.15 K',300,105,310,36,FS);txt(s,'2 h',303,172,250,34,SM);
line(s,843,153,984,153,C.b24,2);line(s,984,153,1105,90,C.b24,2);line(s,1105,90,1226,153,C.b24,2);line(s,1226,153,1368,153,C.b24,2);txt(s,'315 K target',1040,56,250,32,SM);txt(s,'Heat 1 h',941,182,190,32,SM);txt(s,'Recool 1 h',1160,182,225,32,SM);
txt(s,'Common preceding crystallization recipe',130,232,1250,36,SM,false,C.muted,'center');
line(s,30,292,1410,292,C.grid);panel(s,'b',30,312);
txt(s,'12-batch session',97,312,555,38,FS,true,C.b12);txt(s,'24-batch session',810,312,555,38,FS,true,C.b24);
txt(s,'Predicted fines',97,369,575,34,SM);txt(s,'Predicted fines',810,369,575,34,SM);
txt(s,'17%',120,413,145,45,29,true,C.b12);arrow(s,292,436,420,436,C.b12,2);txt(s,'12%',454,413,145,45,29,true,C.b12);
txt(s,'49%',840,413,145,45,29,true,C.b24);arrow(s,1010,436,1138,436,C.b24,2);txt(s,'35%',1172,413,145,45,29,true,C.b24);
line(s,90,489,1360,489,C.grid);txt(s,'Predictions sealed',250,511,420,36,FS,true);arrow(s,690,529,772,529);txt(s,'K2 without reference feedback',820,511,560,36,FS);
agent(s,100,595,C.b12);txt(s,'Thermal cycling was untested.\nSeed survival was assumed.',202,589,500,80,FS);agent(s,812,595,C.b24);txt(s,'Batch 8 gave no improvement.\nThis evidence was underused.',914,589,478,80,FS);
txt(s,'Recorded retrospective answers, condensed',120,686,1210,36,SM,false,C.muted,'center');
line(s,30,745,1410,745,C.grid);panel(s,'c',30,767);txt(s,'Proposed experiment, not executed',99,767,1260,36,FS,true);
txt(s,'Keep batch 23 upstream conditions',95,822,635,38,FS);txt(s,'Change cooling only',820,822,535,38,FS);
let xx=158,yy=926;line(s,xx,yy-22,xx+75,yy-22,C.b24,2);line(s,xx+75,yy-22,xx+75,yy,C.b24,2);line(s,xx+75,yy,xx+150,yy,C.b24,2);line(s,xx+150,yy,xx+150,yy+22,C.b24,2);line(s,xx+150,yy+22,xx+225,yy+22,C.b24,2);txt(s,'Staged cooling',440,904,310,39,FS);arrow(s,753,927,839,927);line(s,892,904,1134,948,C.b24,2);txt(s,'Direct to 250 K',1140,907,278,39,FS);
txt(s,'Recovery and quality retained',96,987,480,34,SM);txt(s,'Recovery retained; fines rise',588,987,480,34,SM);txt(s,'Both worsen',1140,987,250,34,SM);
txt(s,'Upstream effect',96,1023,470,34,SM,false,C.muted);txt(s,'Cooling effect',588,1023,460,34,SM,false,C.muted);txt(s,'Interaction possible',1140,1023,280,34,SM,false,C.muted);
line(s,30,1080,1410,1080,C.grid);panel(s,'d',30,1103);txt(s,'Evaluator reference for panel a',100,1103,640,38,FS);txt(s,'Fines: 35% to 100%',817,1103,550,38,FS,true,C.bad);txt(s,'Unavailable to the agent during Q and K2',100,1155,1250,32,SM,false,C.muted);
}

// Extended figure S1: native editable infrastructure diagram and qualification table.
{
const s=slide('figureS1-infrastructure',860,'Extended Figure S1. Frozen finite-domain platform qualification, separate from 240 agent campaigns. Source: first-paper qualification and Methods. Counts 64, 1786, 192, 52; generated cases 18 + 8 + 26.');
panel(s,'a',30,20);const labels=[['Physical process model','State, laws, instruments, private parameters'],['Experimental runtime','Validate, commit, measure, account, replay'],['Task and evaluation contract','Objectives, operations, budgets, termination']];
labels.forEach(([a,b],i)=>{const y=83+i*138;box(s,a,92,y,840,65);txt(s,b,105,y+70,835,37,SM);});box(s,'External researcher',1040,202,333,90);arrow(s,932,246,1035,246,C.Aligned,2);txt(s,'Agent, optimizer\nor human',1040,311,333,76,FS,false,C.ink,'center');
panel(s,'b',30,543);const vals=[['Task-world units','64'],['Boundary and categorical recipes','1,786'],['Invalid-action probes','192'],['Generated compositions','52']];
vals.forEach(([a,b],i)=>{const x=94+(i%2)*680,y=599+Math.floor(i/2)*71;txt(s,a,x,y,520,40,FS);txt(s,b,x+530,y,90,40,FS,true,C.Aligned,'right');line(s,x,y+49,x+620,y+49,C.grid);});
txt(s,'Generated: 18 new topologies + 8 new identities + 26 coverage cases',94,768,1240,34,SM);txt(s,'Additional: 32 module probes, 7 valid interfaces, 7 invalid compositions',94,811,1240,34,SM);
}

// Extended figure S2: the same 16 system-specific panels as the existing supplement.
{
const s=slide('figureS2-prior-overview',1350,'Extended Figure S2. Complete prior overview, retaining the existing 16 selected readouts. Five matched worlds per panel, with all 240 campaigns retained in the tables. Source: campaign_metrics.csv. Scales differ.');
const defs=[['EC','E','discovery',12,'score'],['EC','E','discovery',24,'score'],['EC','E','optimization',12,'score'],['EC','E','optimization',24,'score'],['PA','E','discovery',12,'product_in_organic'],['PA','E','discovery',24,'product_in_organic'],['RX','P','discovery',12,'macro'],['RX','S','discovery',12,'macro'],['RX','P','optimization',12,'macro'],['RX','S','optimization',12,'macro'],['EQ','P','characterization',12,'macro'],['EQ','S','characterization',12,'macro'],['C','E','delivery',12,'crystal_fines_fraction'],['C','E','delivery',24,'crystal_fines_fraction'],['P','E','delivery',12,'purity'],['P','E','delivery',12,'recovery']];
defs.forEach(([sys,locus,goal,b,metric],i)=>{const x=20+(i%4)*358,y=12+Math.floor(i/4)*325;const rr=(metric==='macro'?DATA.macro_campaigns:DATA.campaigns).filter(r=>r.system===sys&&r.locus===locus&&r.goal===goal&&r.budget===b&&r.metric===metric);const worlds=[...new Set(rr.map(r=>r.world))].sort();if(rr.length!==15)throw Error('prior overview denominator');
txt(s,`${sys}/${locus}, ${goal==='optimization'?'opt.':goal==='discovery'?'disc.':goal==='characterization'?'char.':'delivery'}, ${b}`,x+35,y,318,32,SM);const lab=metric==='macro'?'Macro MAE':metric==='product_in_organic'?'Organic-fraction MAE':metric==='crystal_fines_fraction'?'Fines MAE':metric==='score'?'Score MAE':metric==='purity'?'Purity MAE':'Recovery MAE';txt(s,lab,x+35,y+34,318,30,SM,false,C.muted);
const ser=worlds.map(w=>seg(w,[0,1,2],ARMS.map(a=>rr.find(r=>r.world===w&&r.arm===a).mae),C.grid,1.2));
ARMS.forEach((a,j)=>{const vv=worlds.map(w=>rr.find(r=>r.world===w&&r.arm===a).mae);ser.push(series(a,vv.map(()=>j),vv,C[a]));});
const max=Math.max(...rr.map(r=>r.mae))*1.1;chart(s,ser,x,y+68,346,205,axis('',-.5,2.5,1,'0',false),axis('',0,max,undefined,'0.00'));
['O','A','M'].forEach((a,j)=>txt(s,a,x+83+j*88,y+286,52,30,SM,false,C.ink,'center'));
});legend(s,ARMS.map(a=>[a,C[a]]),1310,440);
}

const stamp=Date.now(); const candidate=path.join(BUILD,`candidate-${stamp}.pptx`);
console.log(`ppt stage=export slides=${figures.length}`);
await (await PresentationFile.exportPptx(p)).save(candidate);
// Explicit marker fills prevent PowerPoint from inheriting a no-line fill for points.
const repaired=spawnSync(path.join(ROOT,'.venv/Scripts/python.exe'),[path.join(ROOT,'paper/tools/repair_figure_chart_markers.py'),candidate],{encoding:'utf8'});
if(repaired.status!==0)throw Error(repaired.stderr||'Chart marker repair failed');
await fs.writeFile(path.join(BUILD,'figures.proto.json'),JSON.stringify(p.toProto()));
// The native package is the editing master. Finalizer preserves editable chart data.
const checked=path.join(BUILD,'final',`checked-${stamp}.pptx`);
await fs.mkdir(path.dirname(checked),{recursive:true});
await finalizePresentation({workspaceDir:BUILD,candidatePath:candidate,finalPath:checked,
 pythonExecutable:path.join(ROOT,'.venv/Scripts/python.exe'),
 integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu',`${W*9525},${H*9525}`,'--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:9,requiredNativeChartOwnerSlides:[2,5,6,9],
 materializeLiteralChartWorkbooks:true,nativeChartTargetApplication:'portable',
 fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,`validation-${stamp}.json`)});
await fs.copyFile(checked,DECK);
console.log('ppt stage=finalized slides=9');
// Render the finalized PPTX, not the pre-export authoring model.
const imported=await PresentationFile.importPptx(await FileBlob.load(DECK));
for(let i=0;i<figures.length;i++){
 const {name,height}=figures[i];const sl=imported.slides.getItem(i);
 const blob=await imported.export({slide:sl,format:'png',scale:3});
 const buf=Buffer.from(await blob.arrayBuffer());
 await sharp(buf).extract({left:0,top:0,width:W*3,height:height*3}).png().toFile(path.join(OUT,name+'.png'));
 await sharp(buf).extract({left:0,top:0,width:W*3,height:height*3}).resize(W,height).png().toFile(path.join(BUILD,name+'.png'));
 await fs.writeFile(path.join(BUILD,name+'.layout.json'),await (await sl.export({format:'layout'})).text());
 console.log(`ppt stage=render completed=${i+1}/9 figure=${name}`);
}
await fs.writeFile(path.join(OUT,'style-and-export.json'),JSON.stringify({fontFamily:FONT,fontSizePx:FS,tickSizePx:SM,panelSizePx:PANEL,widthPx:W,slideHeightPx:H,palette:C,pptx:path.relative(ROOT,DECK),figures:figures.map(({name,height})=>({name,height})),renderSource:'finalized PPTX',rasterScale:3,newScientificExperiments:0},null,2)+'\n');
console.log('ppt done '+DECK);
