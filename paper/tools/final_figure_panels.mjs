// Additional retained-data panels and compacted approved artwork for the final draft.
import fs from 'node:fs/promises';
import path from 'node:path';

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
 const {slide,ROOT,panel,chart,axis,series,txt,shape,line,C}=ctx;
 const data=JSON.parse(await fs.readFile(path.join(ROOT,'output/figures/research-case-v16/data.json'),'utf8'));
 const s=slide(name,1580,'Figure 2: same W05 crystallization world and Aligned information; two independent original sessions. Charts retain all 36 batch outcomes and running best quality-feasible recovery. B19 to B20 changes heating, cooling and an intermediate particle-size check, so no single-operation effect is inferred. K1 text condenses subsequent public accounts, not contemporaneous thoughts.');
 const blue=C.b12,teal=C.b24,accent='#B86D3D';
 function heading(id,y,title){txt(s,id,18,y,35,40,30,true,'#111111');txt(s,title,62,y,1330,40,23,false,C.ink);}
 function rule(y){line(s,24,y,1415,y,C.grid,1.4);}
 function key(x,y){
  shape(s,'ellipse',x,y+7,13,13,C.ink,C.ink,1);
  txt(s,'quality-feasible',x+22,y,195,31,18);
  line(s,x+236,y+7,x+251,y+22,C.bad,2);line(s,x+236,y+22,x+251,y+7,C.bad,2);
  txt(s,'infeasible',x+260,y,150,31,18);
  line(s,x+424,y+14,x+465,y+14,C.ink,2.6);
  txt(s,'best feasible so far',x+474,y,220,31,18);
 }
 heading('a',15,'Independent research paths in one matched world');
 txt(s,'Same physical world and Aligned information; separate sessions',63,56,1290,35,20,false,C.muted);
 for(let i=0;i<2;i++){
  const d=data.pair[i],x=25+i*720,col=i?teal:blue,rows=d.rows;
  txt(s,`${d.budget}-batch session`,x+28,112,650,41,27,true,col);
  line(s,x+28,160,x+682,160,col,3);
  txt(s,i?'Materials → process variation → heating and staged cooling → refinement':'Catalysts → solvents → cooling endpoint → refinement',x+28,172,650,35,17,false,C.ink);
  const best=rows.filter(r=>r.best_feasible_recovery_pct!==null),bx=[],by=[];
  best.forEach((r,j)=>{if(j){bx.push(r.batch);by.push(best[j-1].best_feasible_recovery_pct);}bx.push(r.batch);by.push(r.best_feasible_recovery_pct);});
  const good=rows.filter(r=>r.quality_feasible),bad=rows.filter(r=>!r.quality_feasible);
  const ser=[series('Best feasible recovery',bx,by,col,'none',2.9),series('Quality-feasible',good.map(r=>r.batch),good.map(r=>r.recovery_pct),col),series('Infeasible',bad.map(r=>r.batch),bad.map(r=>r.recovery_pct),C.bad,'x')];
  chart(s,ser,x+12,225,675,450,axis('Batch',0,d.budget,i?4:3,'0'),axis('Net recovery (%)',20,65,10,'0'));
  txt(s,`First feasible  B${d.first_feasible_batch}`,x+38,687,294,38,21,true,C.ink);
  txt(s,`Best feasible  B${d.best_feasible_batch} · ${d.best_feasible_recovery_pct.toFixed(1)}%`,x+330,687,355,38,21,true,col,'right');
 }
 key(357,750);
 rule(803);
 heading('b',820,'What changed at the critical transitions');
 const changes=[
  {x:25,col:blue,title:'B9 → B10',before:'49.8% recovery · 42.4% fines',after:'51.2% recovery · 45.7% fines',lines:[['Cooling endpoint','260 K','250 K']],note:'Other settings unchanged; both batches meet quality constraints.'},
  {x:745,col:teal,title:'B19 → B20',before:'49.0% recovery · 52.8% fines',after:'52.9% recovery · 21.5% fines',lines:[['Heating','390 K / 30 min','410 K / 20 min'],['Cooling','Direct to 260 K','Staged 320 → 290 → 260 K'],['Size measurement','Performed','Omitted']],note:'First quality-feasible batch; multiple changes were made together.'}
 ];
 for(const q of changes){
  txt(s,q.title,q.x+25,874,630,44,27,true,q.col);
  txt(s,q.before,q.x+25,926,630,35,21);
  line(s,q.x+25,971,q.x+660,971,C.grid,1.2);
  q.lines.forEach((a,j)=>{const y=991+j*55;txt(s,a[0],q.x+25,y,165,35,19,false,C.muted);txt(s,a[1],q.x+200,y,174,35,19);txt(s,'→',q.x+383,y,39,35,23,false,accent,'center');txt(s,a[2],q.x+428,y,235,39,19,true,C.ink);});
  txt(s,q.after,q.x+25,1165,630,40,23,true,q.col);
  txt(s,q.note,q.x+25,1208,640,34,18,false,C.ink);
 }
 rule(1265);
 heading('c',1280,'Sealed recommendation and independent retest');
 const selections=[
  {x:25,col:blue,rec:'B10',source:'51.2%',retest:'50.4%',fines:'46.2%',account:'B10 led in recovery; the small gap from B12\nremained unresolved.'},
  {x:745,col:teal,rec:'B23',source:'57.0%',retest:'58.1%',fines:'19.3%',account:'Hotter, shorter heating with staged cooling;\nB22–B24 formed a recovery plateau.'}
 ];
 for(const q of selections){
  txt(s,`Selected ${q.rec}`,q.x+25,1335,290,39,24,true,q.col);
  txt(s,`Observed ${q.source}`,q.x+306,1335,352,39,22,false,C.ink,'right');
  line(s,q.x+25,1386,q.x+665,1386,C.grid,1.2);
  txt(s,`Independent retest   ${q.retest} recovery · ${q.fines} fines`,q.x+25,1400,640,43,23,true,q.col);
  txt(s,'Later public K1 account',q.x+25,1458,640,30,18,true,C.muted);
  txt(s,q.account,q.x+25,1490,640,64,19,false,C.ink);
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
