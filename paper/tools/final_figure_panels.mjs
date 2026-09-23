// Additional retained-data panels and compacted approved artwork for the final draft.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const {default:sharp}=await import(pathToFileURL('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.cjs').href);

export function addPriorFinal(ctx,name='figureS2-prior-detail'){
 const {slide,panel,chart,axis,series,seg,txt,legend,DATA,C,ARMS,mean}=ctx;
 const s=slide(name,1135,'RX parameter-prior positive controls and post hoc EQ dilution groups. Five worlds per arm. All retained values, no new scientific experiments.');
 for(let i=0;i<2;i++){
  const x=25+i*720,goal=i?'optimization':'discovery';
  panel(s,String.fromCharCode(97+i),x,12,`Reaction processing: ${goal}`);
  const rr=DATA.macro_campaigns.filter(r=>r.system==='RX'&&r.locus==='P'&&r.goal===goal&&r.metric==='macro');
  if(rr.length!==15)throw Error('RX denominator');
  const worlds=[...new Set(rr.map(r=>r.world))].sort(),ser=worlds.map(w=>seg(w,[0,1,2],ARMS.map(a=>rr.find(r=>r.world===w&&r.arm===a).mae),C.grid,1));
  ARMS.forEach((a,j)=>{const vals=rr.filter(r=>r.arm===a).map(r=>r.mae);ser.push(series(a,vals.map(()=>j),vals,C[a]));ser.push(seg('Mean '+a,[j-.12,j+.12],[mean(vals),mean(vals)],C[a],3));});
  chart(s,ser,x+20,70,665,365,axis('',-.45,2.45,1,'0',false),axis('Macro MAE',0,.25,.05,'0.00'));
  ARMS.forEach((a,j)=>txt(s,a,x+103+j*173,443,165,30,18,false,C.ink,'center'));
  txt(s,'Aligned improves over Opaque in 4/5 worlds',x+65,484,620,32,18);
 }
 for(let i=0;i<2;i++){
  const x=25+i*720,key=i?'coverage':'mae',sc=i?100:1,ser=[];
  panel(s,i?'d':'c',x,565,'Equilibrium: parameter prior');
  ['other_nine','three_most_dilute'].forEach((g,gi)=>ARMS.forEach((a,ai)=>{
   const xx=gi+1+(ai-1)*.18,rr=DATA.regimes.cells.filter(r=>r.arm===a),m=mean(rr.map(r=>r.groups[g][key]*sc));
   ser.push(series(a+' '+g,rr.map((_,j)=>xx+(j-2)*.018),rr.map(r=>r.groups[g][key]*sc),C[a]));
   ser.push(seg('Mean '+a+' '+g,[xx-.065,xx+.065],[m,m],C[a],3));
  }));
  if(i)ser.unshift(seg('Nominal 80%',[.5,2.5],[80,80],C.muted,1.3));
  chart(s,ser,x+20,615,670,365,axis('',.5,2.5,1,'0',false),axis(i?'Interval coverage (%)':'Macro MAE',0,i?100:.2,i?20:.05,i?'0':'0.00'));
  txt(s,'Other nine',x+156,985,200,32,18,false,C.ink,'center');txt(s,'Dilute three',x+438,985,200,32,18,false,C.ink,'center');
 }
 legend(s,ARMS.map(a=>[a,C[a]]),1040,440);
 txt(s,'Points: five worlds per arm; short lines: means. EQ grouping is exploratory.',85,1090,1280,32,18,false,C.muted,'center');
}

export function addEqFinal(ctx){
 const {slide,panel,chart,axis,series,seg,txt,legend,DATA,C,ARMS,line}=ctx;
 const s=slide('figure05-eq-evidence',1335,'All 15 original EQ/P autonomous sessions. Source concentrations are sum(reagent)/sum(solvent). Source observations and sealed Q08 values from EQ_AUTONOMOUS_PROCESS.json. W02 is the selected example; weak-acid extrapolation becomes explicit in Q, not K1.');
 const rows=[...DATA.eq_process].sort((a,b)=>a.world.localeCompare(b.world)||ARMS.indexOf(a.arm)-ARMS.indexOf(b.arm));
 if(rows.length!==15||rows.reduce((n,r)=>n+r.batches.length,0)!==180)throw Error('EQ coverage');
 panel(s,'a',25,10,'Acquired concentration coverage');
 const ser=[];
 [-4.875061263,-3.875061263,-3.77815125].forEach((c,j)=>ser.push(seg('Dilute query '+j,[c,c],[.5,15.5],C.grid,1.5)));
 rows.forEach((r,j)=>{const y=15-j,vals=r.batches.map(b=>Math.log10(b.nominal_concentration_mol_L));ser.push(seg(r.id,[Math.min(...vals),Math.max(...vals)],[y,y],C[r.arm],2));ser.push(series(r.id+' batches',vals,vals.map(()=>y),C[r.arm]));});
 chart(s,ser,90,67,610,483,axis('log10 concentration (mol/L)',-5,1,1,'0'),axis('',.5,15.5,1,'0',false));
 rows.forEach((r,j)=>txt(s,`${r.world.replace('W0','')}/${r.arm==='Opaque'?'O':r.arm==='Aligned'?'A':'M'}`,30,82+j*25.8,72,25,16,false,C.ink,'right'));
 txt(s,'Dilute tests',173,51,175,25,17,false,C.muted);txt(s,'All 180 source batches remain above the dilute tests',55,568,665,34,18);
 panel(s,'b',755,10,'One matched world: observed response');
 const rr=rows.filter(r=>r.world==='W02'&&r.arm!=='MisIndexed');
 const ser2=rr.map(r=>series(r.arm,r.batches.map(b=>Math.log10(b.nominal_concentration_mol_L)),r.batches.map(b=>b.final_responses.acid_dissociation_fraction),C[r.arm]));
 chart(s,ser2,757,67,650,398,axis('log10 concentration (mol/L)',-2,.5,.5,'0.0'),axis('Observed dissociation',0,.12,.03,'0.00'));
 txt(s,'Aligned: 90-fold range; Opaque: 4-fold range',806,484,601,32,18);
 txt(s,'K1: both qualify extrapolation beyond observations.',780,528,630,32,18);
 txt(s,'Q: weak-acid extrapolation (O); weak local trend (A).',780,565,630,32,18);
 legend(s,ARMS.map(a=>[a,C[a]]),620,440);
 line(s,25,674,1415,674,C.grid);
 txt(s,'Sealed predictions at the most dilute condition',65,695,1200,38,22,true);
 const worlds=[...new Set(rows.map(r=>r.world))];
 worlds.forEach((world,j)=>{const x=25+j*284;panel(s,String.fromCharCode(99+j),x,755,`World ${j+1}`);const rr=ARMS.map(a=>rows.find(r=>r.world===world&&r.arm===a)),ss=[];
  const target=rr[0].q08.reference_means.acid_dissociation_fraction;ss.push(seg('Reference',[-.3,2.3],[target,target],C.ink,2));
  rr.forEach((r,i)=>{const v=r.q08.predictions.acid_dissociation_fraction;ss.push(seg('Source range '+r.arm,[i,i],r.source_dissociation_range,C.grid,14));ss.push(seg('80% interval '+r.arm,[i,i],[v.lower80,v.upper80],C[r.arm],2));ss.push(series(r.arm,[i],[v.estimate],C[r.arm]));});
  chart(s,ss,x,808,275,340,axis('',-.45,2.45,1,'0',false),axis(j===0?'Dissociation fraction':'',0,1,.25,'0.00'));
 });
 line(s,75,1203,117,1203,C.ink,2);txt(s,'Reference mean',130,1183,285,36,18);line(s,440,1203,484,1203,C.grid,12);txt(s,'Observed source range',499,1183,365,36,18);txt(s,'Prediction and 80% interval',970,1183,440,36,18);
 txt(s,'Original research context retained during Q; no reference feedback.',70,1250,1300,34,18,false,C.ink,'center');
 txt(s,'Source coverage, public accounts and predictions describe the complete autonomous process.',50,1295,1340,30,18,false,C.muted,'center');
}

export async function addCaseFinal(ctx,name='figure02-research-paths'){
 const {slide,ROOT,W,panel,chart,axis,series,txt,shape,line,C}=ctx;
 const data=JSON.parse(await fs.readFile(path.join(ROOT,'output/figures/research-case-v16/data.json'),'utf8'));
 const art=await fs.readFile(path.join(ROOT,'output/imagegen/c-w05-research-paths-v15.png'));
 const s=slide(name,1825,'Selected original W05 Aligned independent sessions, preserved v16/v15 artwork and retained batch values. Regular-weight editable typography; lowercase Arial bold panel letters match supplied Figure 1. Progress is best feasible observed recovery; no values before first feasible batch. All 36 batch results retained in source CSV. K1 reflections are later accounts. Figure footnotes moved to the manuscript caption. The illustration is not a population budget effect.');
 async function crop(left,top,width,height,x,y,w){const blob=await sharp(art).extract({left,top,width,height}).png().toBuffer();s.images.add({blob,contentType:'image/png',position:{left:x,top:y,width:w,height:height*w/width},fit:'contain',alt:'Approved case artwork, uniformly scaled and reflowed'});}
 const scale=W/1143;
 // Retain original icons and process geometry; replace only raster text with native text.
 function label(t,x,y,w,h,top=0,outY=0,size=22,background='#FFFFFF',color=C.ink,align='left'){
  const px=x*scale,py=(y-top)*scale+outY;
  shape(s,'rect',px,py,w*scale,h*scale,background,'none',0);
  txt(s,t,px+2,py,w*scale-4,h*scale,size,false,color,align);
 }
 function casePanel(id,y,title){
  // Figure 1 uses 22.5 pt Arial bold on a 1,448 px-wide slide.
  txt(s,id,17,y,32,38,30*W/1448,true,'#000000');
  txt(s,title,64,y,1320,38,22,false,C.ink);
 }
 await crop(0,0,1143,250,0,0,W);
 label('',16,43,750,38);
 casePanel('a',55,'How the research budget was used');
 label('12 batches',30,82,533,29,0,0,26,'#EAF6FC');
 label('24 batches',604,82,527,29,0,0,26,'#EAF7FA');
 for(let i=0;i<2;i++){
  const session=data.pair[i],rows=session.rows,x=15+i*720,col=i?'#009BB5':'#0066DB',best=rows.filter(r=>r.best_feasible_recovery_pct!==null),xx=[],yy=[];
  best.forEach((r,j)=>{if(j){xx.push(r.batch);yy.push(best[j-1].best_feasible_recovery_pct);}xx.push(r.batch);yy.push(r.best_feasible_recovery_pct);});
  txt(s,`${session.budget}-batch session`,x+75,319,600,32,20,false,col);
  const good=rows.filter(r=>r.quality_feasible),bad=rows.filter(r=>!r.quality_feasible);
  const ser=[series('Best feasible recovery',xx,yy,col,'none',2.5),series('Feasible observations',good.map(r=>r.batch),good.map(r=>r.recovery_pct),col),series('Infeasible observations',bad.map(r=>r.batch),bad.map(r=>r.recovery_pct),C.bad,'x')];
  chart(s,ser,x+8,357,680,220,axis('Batch',0,session.budget,i?4:3,'0'),axis('Recovery (%)',20,65,20,'0'));
  rows.forEach(r=>shape(s,'rect',x+115+(r.batch-1)*510/session.budget,584,Math.min(16,470/session.budget),12,r.quality_feasible?col:C.bad,'none',0));
  txt(s,`${session.feasible_batches}/${session.budget} quality-feasible; first feasible: batch ${session.first_feasible_batch}`,x+75,602,650,28,18);
 }
 line(s,25,683,1415,683,C.grid);
 casePanel('b',692,'Recorded changes between adjacent batches');
 await crop(0,340,1143,103,0,736,W);
 await crop(0,516,1143,412,0,867,W);
 label('Batches 9 → 10',30,343,530,28,340,736,26,'#EAF6FC');
 label('Batches 19 → 20',600,343,521,28,340,736,26,'#EAF7FA');
 for(const [x,obs,rec,fines,color,status] of [[0,'9','49.8%','42.4%','#009BB5','Pass'],[572,'19','49.0%','52.8%','#EC1C24','Fines fail']]){
  label(`Observation\n(batch ${obs})`,70+x,385,120,45,340,736,20);
  label(rec,213+x,401,84,32,340,736,29);
  label(fines,x?887:340,401,x?97:85,32,340,736,29,'#FFFFFF',x?'#EC1C24':C.ink);
  label(status,x?1038:503,393,x?94:52,39,340,736,21,'#FFFFFF',color);
 }
 label('Next experiment (batch 10)',70,517,350,24,516,867,20);
 label('Next experiment (batch 20)',642,517,410,24,516,867,20);
 label('260 K',108,582,103,33,516,867,24,'#F8FCFE',C.ink,'center');
 label('250 K',272,582,100,33,516,867,24,'#F8FCFE',C.ink,'center');
 label('Heating:',650,545,124,26,516,867,21);
 label('Cooling targets:',874,545,220,26,516,867,21);
 label('260 K',900,636,76,23,516,867,23,'#FFFFFF',C.ink,'center');
 for(const [x,batch,rec,fines,status] of [[0,'10','51.2%','45.7%','Pass'],[568,'20','52.9%','21.5%','First quality-\nfeasible batch']]){
  label(`Outcome (batch ${batch})`,70+x,873,123,40,516,867,19);
  label(rec,219+x,884,78,34,516,867,28,'#FFFFFF','#0066DB');
  label(fines,x?882:338,884,x?98:82,34,516,867,28,'#FFFFFF',x?'#009BB5':C.ink);
  label(status,x?1027:503,873,x?105:58,47,516,867,20,'#FFFFFF',x?C.ink:'#009BB5');
 }
 label('',195,831,342,28,516,867);
 label('',768,837,347,27,516,867);
 // Remove obsolete step numbers after omitting unrecorded immediate considerations.
 for(const x of [20,743]){
  for(const [y,n] of [[784,'1'],[858,'2'],[1309,'3']]){
   shape(s,'rect',x,y,59,66,'#FFFFFF','none',0);
   shape(s,'ellipse',x+6,y+8,40,40,'#E7F7FC','none',0);
   txt(s,n,x+6,y+8,40,40,24,false,C.ink,'center');
  }
 }
 line(s,25,1425,1415,1425,C.grid);
 casePanel('c',1433,'Selected procedures, later K1 accounts and independent retests');
 for(let i=0;i<2;i++){
  const x=25+i*720,col=i?'#009BB5':'#0066DB';
  txt(s,i?'Selected batch 23 (24-batch session)':'Selected batch 10 (12-batch session)',x+10,1474,680,31,20,false);
  await crop(30,1052,65,72,x+5,1511,67);
  txt(s,i?'Hotter, shorter heating + staged cooling.\nBatches 22–24 formed a broad recovery plateau.':'Batch 12 had fewer fines; batch 10 led in recovery.\nThe small recovery gap remained unresolved.',x+93,1514,599,63,18);
 }
 await crop(0,1149,1143,88,0,1595,W);
 label('Selected recipe (batch 10)',23,1149,400,23,1149,1595,20);
 label('Selected recipe (batch 23)',596,1149,474,23,1149,1595,20);
 label('S1 / C3',35,1204,67,21,1149,1595,21,'#FFFFFF',C.ink,'center');
 label('S2 / C1',599,1204,74,21,1149,1595,21,'#FFFFFF',C.ink,'center');
 for(let i=0;i<2;i++){
  const x=25+i*720,col=i?'#009BB5':'#0066DB';
  txt(s,i?'Observed: recovery 57.0% | purity 100% | fines 14.2%':'Observed: recovery 51.2% | purity 97.8% | fines 45.7%',x+7,1710,695,27,17);
  txt(s,'Independent retest',x+12,1746,670,29,19,false,C.ink,'center');
  txt(s,i?'Recovery 58.1%     Fines 19.3%':'Recovery 50.4%     Fines 46.2%',x+12,1780,670,39,24,false,col,'center');
 }
}

export function addSecondaryFinal(ctx){
 const {slide,panel,chart,axis,series,seg,txt,legend,DATA,C,ARMS,groupedPoints}=ctx;
 const s=slide('figureS5-secondary-outcomes',670,'Retained secondary outcomes moved from main Figures 2 and 6. Purification has 15 recommendations; crystallization has all 30 original campaigns including its source shortfall.');
 panel(s,'a',25,16,'Purification');const rr=DATA.campaigns.filter(r=>r.system==='P'&&r.goal==='delivery'&&r.metric==='recovery');
 const ss=[seg('Purity threshold',[0,.9],[.8,.8],C.ink),...ARMS.map(a=>{const r=rr.filter(v=>v.arm===a);return series(a,r.map(v=>v.retest),r.map(v=>v.retest_purity),C[a]);})];
 chart(s,ss,30,80,435,425,axis('Original-charge recovery',0,.9,.3,'0.0'),axis('Retested purity',0,1,.2,'0.0'));
 txt(s,'Eligible: 0/5, 3/5, 0/5 (O, A, M)',50,532,420,31,18);
 [['crystal_size','Size index',.22,.1],['crystal_fines_fraction','Fines',.55,.25]].forEach(([m,label,lim,step],i)=>{
  const x=505+i*460;panel(s,i?'c':'b',x,16,label);const xx=r=>r.public_baselines.mae.public_mean[m],yy=r=>r.agent_mae[m];
  chart(s,[seg('Equal error',[0,lim],[0,lim],C.grid),...groupedPoints(DATA.crystal,xx,yy)],x,80,445,425,axis('Source-mean MAE',0,lim,step,'0.00'),axis('Agent MAE',0,lim,step,'0.00'));
  txt(s,`${DATA.crystal.filter(r=>yy(r)<xx(r)).length}/30 lower agent error`,x+65,532,395,31,18);
 });
 legend(s,ARMS.map(a=>[a,C[a]]),616,440);
}
