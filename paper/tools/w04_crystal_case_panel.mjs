// Editable Figure 2: one complete, formally retained W04/MisIndexed source session.
// All quantitative labels are generated from the formal summary, not copied from concept art.
import fs from 'node:fs/promises';
import path from 'node:path';

export async function addSingleCrystalCase(ctx,name='figure02-research-paths-typography'){
  const {slide,ROOT,txt,shape,line,C}=ctx;
  const file=path.join(ROOT,'workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/summary.json');
  const result=JSON.parse(await fs.readFile(file,'utf8')).results.find(r=>r.id==='C-W04-B12-E-MisIndexed');
  if(!result||result.status!=='completed'||result.source.batches.length!==12||result.recommendation.selected_experiment_index!==8) throw Error('W04 source coverage or selection changed');
  const rows=result.source.batches;
  const fines=rows.map(r=>100*r.metrics.crystal_fines_fraction);
  const recovery=rows.map(r=>100*r.metrics.crystal_yield);
  const purity=rows.map(r=>100*r.metrics.crystal_purity);
  const feasible=rows.map((r,i)=>fines[i]<=50&&purity[i]>=80);
  const actions=rows[7].actions;
  const expected=['add_reagent','add_solvent','add_catalyst','heat','cool_crystallize','seed_crystals','cool_crystallize','wait','measure','filter_crystals','terminate','measure'];
  if(actions.map(a=>a.operation).join(',')!==expected.join(',')||!feasible[4]||feasible.slice(0,4).some(Boolean)||feasible[10]||!feasible[11])throw Error('W04 batch/process invariants changed');
  if(rows.slice(0,4).some(r=>!r.actions.some(a=>a.operation==='quench'))||rows[4].actions.some(a=>a.operation==='quench')||rows[10].actions.find(a=>a.operation==='add_solvent')?.volume_L!==.04||JSON.stringify(rows[11].actions)!==JSON.stringify(actions))throw Error('W04 process comparison changed');
  const a=(i,op)=>{if(actions[i].operation!==op)throw Error(`B8 action ${i+1}`);return actions[i];};
  const near=(x,y)=>Math.abs(x-y)<1e-8;
  if(!near(a(0,'add_reagent').amount_mol,.04)||!near(a(1,'add_solvent').volume_L,.08)||a(1,'add_solvent').solvent!==2||!near(a(2,'add_catalyst').catalyst_amount_mol,.005)||a(2,'add_catalyst').catalyst!==1||a(3,'heat').target_temperature_K!==355||a(3,'heat').duration_s!==3600||a(3,'heat').stirring_speed_rpm!==300||a(4,'cool_crystallize').target_temperature_K!==325||a(4,'cool_crystallize').duration_s!==7200||!near(a(5,'seed_crystals').seed_mass_g,.001)||a(6,'cool_crystallize').target_temperature_K!==250||a(6,'cool_crystallize').duration_s!==14400||a(7,'wait').duration_s!==14400||a(7,'wait').stirring_speed_rpm!==100||a(8,'measure').instrument!=='particle_size'||a(11,'measure').instrument!=='final_assay')throw Error('B8 operation details changed');
  const retest=result.recommendation_retest.batches[0].metrics;
  const s=slide(name,1160,'Figure 2. One complete W04/B12/MisIndexed research session. Quantities and operations are generated from the formal source and independent recommendation retest. Questions are author reconstructions from recorded actions, not contemporaneous quotations. K1 was written after all twelve batches. Quench has no isolated causal effect in this session.');
  const ink='#24292D',muted='#637079',teal=C.Aligned,rust=C.bad,grid='#D5DDE0',pale='#F3F7F8';
  const F=n=>n.toFixed(1);
  function T(t,x,y,w,h=28,size=18,bold=false,color=ink,align='left'){return txt(s,t,x,y,w,h,size,bold,color,align);}
  function L(x1,y1,x2,y2,color=grid,width=1.2,dash=false){return line(s,x1,y1,x2,y2,color,width,dash);}
  function dot(x,y,color,r=6){shape(s,'ellipse',x-r,y-r,2*r,2*r,color,color,1);}
  function arrow(x1,y1,x2,y2,color=ink){L(x1,y1,x2,y2,color,1.5);L(x2-7,y2-5,x2,y2,color,1.5);L(x2-7,y2+5,x2,y2,color,1.5);}
  function heading(letter,title,y){T(letter,23,y,42,34,29,true,'#111111');T(title,70,y,1320,35,25,true,ink);}
  heading('a','Twelve-batch history: observed fines and recovery',14);
  const x0=169,x1=1298,dx=(x1-x0)/11,xx=i=>x0+i*dx;
  function plot(values,top,bottom,max,ticks,label,threshold){
    const yy=v=>bottom-v/max*(bottom-top);
    if(label)T(label,24,top+(bottom-top)/2-20,133,40,20,false,ink);
    L(x0-18,top,x0-18,bottom,ink,1.2);L(x0-18,bottom,x1+20,bottom,ink,1.2);
    for(const v of ticks){const y=yy(v);L(x0-23,y,x0-18,y,ink);T(String(v),x0-72,y-12,45,26,16,false,muted,'right');}
    if(threshold!==undefined){L(x0-18,yy(threshold),x1+22,yy(threshold),'#8EA5B6',1.5,true);T('quality limit ≤ 50%',939,yy(threshold)-30,190,26,16,false,muted,'right');}
    for(let i=0;i<11;i++)L(xx(i),yy(values[i]),xx(i+1),yy(values[i+1]),feasible[i]&&feasible[i+1]?teal:rust,2.4);
    values.forEach((v,i)=>{dot(xx(i),yy(v),feasible[i]?teal:rust,6);T(F(v),xx(i)-31,yy(v)-(i===10&&threshold!==undefined?39:31),62,25,16,true,feasible[i]?teal:rust,'center');});
    return yy;
  }
  const yFine=plot(fines,112,272,105,[0,50,100],'Fines (%)',50);
  plot(recovery,329,448,60,[0,25,50],'');
  T('Recovery (%) · seed-excluded',24,295,325,27,17,false,ink);
  rows.forEach((_,i)=>{L(xx(i),448,xx(i),454,ink,1);T(String(i+1),xx(i)-20,456,40,26,17,false,ink,'center');});
  T('Batch',664,487,110,28,18,false,ink,'center');
  T('B5  first feasible',xx(4)-87,55,175,29,17,true,teal,'center');L(xx(4),85,xx(4),yFine(fines[4])-9,teal,1.1);
  T('B8  selected',xx(7)-73,55,146,29,17,true,teal,'center');L(xx(7),85,xx(7),yFine(fines[7])-9,teal,1.1);
  T('B11  rejected',1066,55,164,29,17,true,rust,'center');L(xx(10),85,xx(10),yFine(fines[10])-9,rust,1.1);
  T('B12  repeat',1272,55,138,29,17,true,ink,'center');L(xx(11),85,xx(11),yFine(fines[11])-9,ink,1.1);
  L(24,520,1416,520,grid);
  heading('b','Batch 8: the complete recorded procedure',534);
  // A two-line path keeps all twelve operation calls legible at print scale.
  const steps=[
    ['Charge','0.040 mol reagent\n0.080 L S2\n0.005 mol C1'],
    ['Heat','towards 355 K\n1 h · 300 rpm'],
    ['Cool','towards 325 K\n2 h'],
    ['Seed','1 mg'],
    ['Cool','towards 250 K\n4 h'],
    ['Hold','4 h · 100 rpm'],
    ['Measure','particle size'],
    ['Filter','crystals'],
    ['Terminate','run'],
    ['Final assay',`recovery ${F(recovery[7])}%\npurity ${F(purity[7])}%\nfines ${F(fines[7])}%`]
  ];
  const topX=[52,282,512,742,972],bottomX=[52,282,512,742,972],bw=190;
  function step(k,x,y){
    const [title,detail]=steps[k];
    shape(s,'roundRect',x,y,bw,84,'#FFFFFF',k===9?teal:grid,k===9?1.8:1.2);
    shape(s,'ellipse',x+11,y+13,29,29,k===9?teal:pale,k===9?teal:grid,1);
    T(String(k+1),x+12,y+13,27,28,16,true,k===9?'#FFFFFF':ink,'center');
    T(title,x+49,y+8,bw-55,28,18,true,k===9?teal:ink);
    T(detail,x+48,y+31,bw-54,48,k===0||k===9?14:16,false,ink);
  }
  for(let k=0;k<5;k++){step(k,topX[k],589);if(k<4)arrow(topX[k]+bw+6,631,topX[k+1]-10,631);}
  // Down then back along the second row; number order remains left to right.
  L(1202,631,1292,631,ink,1.5);L(1292,631,1292,705,ink,1.5);L(1292,705,65,705,ink,1.5);L(65,705,65,721,ink,1.5);
  L(60,714,65,721,ink,1.5);L(70,714,65,721,ink,1.5);
  for(let k=5;k<10;k++){step(k,bottomX[k-5],721);if(k<9)arrow(bottomX[k-5]+bw+6,763,bottomX[k-4]-10,763);}
  T(`Independent retest of the sealed B8 recipe: ${F(100*retest.crystal_yield)}% recovery · ${F(100*retest.crystal_purity)}% purity · ${F(100*retest.crystal_fines_fraction)}% fines`,30,816,1360,33,19,false,teal);
  L(24,860,1416,860,grid);
  heading('c','Evidence changed the next test',872);
  const cy=[932,1001,1070];
  T('Observed',40,911,245,25,16,true,muted);T('Agent question*',358,911,255,25,16,true,muted);T('Next tested action',683,911,340,25,16,true,muted);T('Outcome',1110,911,260,25,16,true,muted);
  function person(x,y){shape(s,'ellipse',x+8,y,17,17,'#FFFFFF',ink,1.5);L(x+16,y+17,x+16,y+39,ink,1.5);L(x+16,y+22,x,y+31,ink,1.5);L(x+16,y+22,x+32,y+31,ink,1.5);}
  const rdata=[
    [`B1–4: fines ${F(Math.min(...fines.slice(0,4)))}–${F(Math.max(...fines.slice(0,4)))}%`,'Where are fines forming?','B5: omit quench;\ncool before seeding',`fines ${F(fines[4])}% · first feasible`],
    [`B5: feasible; recovery ${F(recovery[4])}%`,'Can colder endpoints\nimprove recovery?','B6/B7: 265/250 K;\nB8: seed 5 → 1 mg',`recovery ${F(recovery[5])} → ${F(recovery[6])} → ${F(recovery[7])}%`],
    ['B8 leads; B9–10 probes','Does higher\nconcentration help?','B11: S2 0.080 → 0.040 L',`B11 fines ${F(fines[10])}%: rejected\nB12 repeats B8: ${F(fines[11])}%`]
  ];
  rdata.forEach((r,i)=>{
    const y=cy[i];if(i)L(35,y-9,1405,y-9,grid,1);
    T(r[0],42,y,275,50,17,i===0,rust);person(332,y+6);
    shape(s,'roundRect',376,y-1,260,54,'#FFFFFF',grid,1.1);T(r[1],389,y+3,237,45,17,false,ink);
    arrow(643,y+26,674,y+26);T(r[2],687,y,386,51,17,true,teal);
    arrow(1058,y+26,1093,y+26);T(r[3],1105,y,305,52,16,true,i===2?rust:teal);
  });
  T('* Questions are author reconstructions from actions, not contemporaneous model quotations. K1 followed all 12 batches; quench effects are confounded.',33,1130,1382,25,14,false,muted);
}
