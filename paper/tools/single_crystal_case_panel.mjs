// One complete retained autonomous crystallization session for main Figure 2.
import fs from 'node:fs/promises';
import path from 'node:path';

export async function addSingleCrystalCase(ctx,name='figure02-research-paths-typography'){
 const {slide,ROOT,chart,axis,series,seg,txt,shape,line,C}=ctx;
 const pair=JSON.parse(await fs.readFile(path.join(ROOT,'output/figures/research-case-v16/data.json'),'utf8'));
 const detail=JSON.parse(await fs.readFile(path.join(ROOT,'output/figures/research-path-redesign/data.json'),'utf8'));
 const d=pair.pair.find(r=>r.session==='C-W05-B24-E-Aligned');
 const account=detail.find(r=>r.session===d?.session);
 if(!d||!account||d.rows.length!==24||d.first_feasible_batch!==20||d.best_feasible_batch!==23)throw Error('single-case coverage');
 d.rows.forEach((r,i)=>{
  const x=account.rows[i];
  if(r.batch!==x.batch||Math.abs(r.recovery_pct-x.recovery_pct)>1e-10||Math.abs(r.fines_pct-x.fines_pct)>1e-10||r.quality_feasible!==x.quality_feasible)throw Error(`case batch ${i+1} mismatch`);
 });
 const q7=account.public_accounts.forecast.Q07,q8=account.public_accounts.forecast.Q08;
 if(account.selected!==23||Math.abs(q7.estimate-.49)>1e-12||Math.abs(q8.estimate-.35)>1e-12)throw Error('selected case forecast mismatch');
 const s=slide(name,1700,'Selected complete W05 B24 Aligned autonomous session. All 24 source batches are retained. K1 followed the experiments and sealed recommendation, Q was sealed without laboratory or target feedback, and K2 followed Q without target feedback. Displayed K1/K2 text is author-condensed. The Q07/Q08 evaluator references were withheld. The source session is illustrative, not a cohort effect.');
 const ink='#24292D',muted='#657078',teal=C.b24,rust=C.bad,grid=C.grid;
 function heading(id,y,title){txt(s,id,18,y,35,40,30,true,'#111111');txt(s,title,62,y,1330,40,23,false,ink);}
 function rule(y){line(s,25,y,1410,y,grid,1.4);}
 function cross(x,y){line(s,x-7,y-7,x+7,y+7,rust,2);line(s,x-7,y+7,x+7,y-7,rust,2);}
 function legend(x,y){
  shape(s,'ellipse',x,y+8,13,13,teal,teal,1);txt(s,'quality-feasible',x+23,y,190,32,18);
  cross(x+242,y+14);txt(s,'infeasible',x+260,y,145,32,18);
  line(s,x+425,y+15,x+466,y+15,teal,2.8);txt(s,'best feasible so far',x+478,y,236,32,18);
 }
 heading('a',12,'A complete 24-batch experimental history');
 txt(s,'Materials (1–6)  →  process variation (7–18)  →  hotter reaction (19)  →  joint process change (20)  →  refinement (21–24)',63,57,1320,39,19,false,muted);
 const rows=d.rows,good=rows.filter(r=>r.quality_feasible),bad=rows.filter(r=>!r.quality_feasible),best=rows.filter(r=>r.best_feasible_recovery_pct!==null),bx=[],by=[];
 best.forEach((r,j)=>{if(j){bx.push(r.batch);by.push(best[j-1].best_feasible_recovery_pct);}bx.push(r.batch);by.push(r.best_feasible_recovery_pct);});
 chart(s,[series('Best feasible recovery',bx,by,teal,'none',2.8),series('Feasible',good.map(r=>r.batch),good.map(r=>r.recovery_pct),teal),series('Infeasible',bad.map(r=>r.batch),bad.map(r=>r.recovery_pct),rust,'x')],52,113,1338,353,axis('',0,24,4,'0'),axis('Net recovery (%)',20,65,10,'0'));
 chart(s,[seg('Fines limit',[0,24],[50,50],grid,1.6),series('Feasible fines',good.map(r=>r.batch),good.map(r=>r.fines_pct),teal),series('Infeasible fines',bad.map(r=>r.batch),bad.map(r=>r.fines_pct),rust,'x')],52,464,1338,292,axis('Batch',0,24,4,'0'),axis('Fines (%)',0,105,25,'0'));
 txt(s,'B8  Thermal-cycle probe; fines 52.8%',58,769,438,38,19,false,ink);
 txt(s,'B20  First quality-feasible batch',504,769,440,38,19,true,teal);
 txt(s,'B23  Best feasible; selected',1000,769,385,38,19,true,teal);
 legend(332,820);
 rule(873);
 heading('b',889,'From a failed batch to a retested procedure');
 txt(s,'B19 → B20  first feasible result',54,942,650,40,24,true,teal);
 txt(s,'Heating',56,989,175,34,19,false,muted);txt(s,'390 K / 30 min',225,989,185,34,20);txt(s,'→',411,989,37,34,22,false,rust,'center');txt(s,'410 K / 20 min',455,989,235,34,20,true);
 txt(s,'Cooling',56,1034,175,34,19,false,muted);txt(s,'Direct to 260 K',225,1034,185,34,20);txt(s,'→',411,1034,37,34,22,false,rust,'center');txt(s,'320 → 290 → 260 K',455,1034,235,34,19,true);
 txt(s,'Particle check',56,1079,175,34,19,false,muted);txt(s,'Performed',225,1079,185,34,20);txt(s,'→',411,1079,37,34,22,false,rust,'center');txt(s,'Omitted',455,1079,235,34,20,true);
 txt(s,'Recovery 49.0% → 52.9%   ·   fines 52.8% → 21.5%',56,1140,645,39,22,true,teal);
 txt(s,'Changes occurred together; their separate effects are not identified.',56,1183,645,36,18,false,muted);
 line(s,726,947,726,1225,grid,1.3);
 txt(s,'B23  sealed recommendation',760,942,630,40,24,true,teal);
 txt(s,'Charge S2/C1  →  heat 450 K / 15 min  →  quench  →  seed 50 mg',760,989,629,37,18);
 txt(s,'Cool 310 → 280 → 250 K (4 h each)  →  hold 4 h  →  filter + assay',760,1037,629,37,18);
 line(s,760,1092,1387,1092,grid,1.2);
 txt(s,'Source batch: 57.0% recovery · 14.2% fines',760,1105,630,37,20);
 txt(s,'Independent retest: 58.1% recovery · 19.3% fines',760,1153,630,42,22,true,teal);
 rule(1257);
 heading('c',1272,'What the original researcher inferred and predicted');
 txt(s,'K1 · after research',54,1325,405,34,21,true,teal);
 txt(s,'Upstream chemistry and cooling were\ninterpreted jointly; seed conditioning\nwas not directly measured.',54,1365,414,107,19);
 line(s,488,1325,488,1496,grid,1.2);
 txt(s,'Q · sealed forecast',518,1325,443,34,21,true,teal);
 txt(s,'Hold 2 h  →  reheat + recool',518,1365,443,34,20);
 txt(s,'Predicted fines: 49% → 35%',518,1403,443,38,22,true,teal);
 txt(s,'80% intervals: [28, 71] → [16, 59]%',518,1447,443,35,18,false,muted);
 line(s,987,1325,987,1496,grid,1.2);
 txt(s,'K2 · after sealed Q',1015,1325,373,34,21,true,teal);
 txt(s,'With no reference feedback, it said\nthe B8 negative result was underused\nand even the sign was uncertain.',1015,1365,372,107,19);
 rule(1514);
 txt(s,'Evaluator-only reference for the same hold → reheat contrast',54,1534,1320,34,19,false,muted);
 txt(s,'Fines: 35% → 100%',54,1570,510,47,29,true,rust);
 txt(s,'The sealed forecast had the opposite direction.',585,1572,792,44,22,true,ink);
 txt(s,'Reference outcomes were unavailable during K1, Q and K2.',54,1632,1320,31,18,false,muted);
}
