// Source-checked reconstruction of the reviewed W04 Figure 2 concept.
// Pictorial entities are generated raster assets; data, labels and arrows stay editable.
// Source assays and actions come from the formal summary. The intermediate
// particle-size readout was checked against source trajectory step 97.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

export async function addSingleCrystalCase(ctx,name='figure02-research-paths-typography'){
  const {slide,ROOT,txt,shape,line}=ctx;
  const source=JSON.parse(await fs.readFile(path.join(ROOT,'workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/summary.json'),'utf8'));
  const result=source.results.find(r=>r.id==='C-W04-B12-E-MisIndexed');
  if(!result||result.status!=='completed'||result.source.batches.length!==12||result.recommendation.selected_experiment_index!==8)throw Error('W04 source or selection changed');
  const rows=result.source.batches,actions=rows[7].actions;
  const fines=rows.map(r=>100*r.metrics.crystal_fines_fraction);
  const recovery=rows.map(r=>100*r.metrics.crystal_yield);
  const purity=rows.map(r=>100*r.metrics.crystal_purity);
  const feasible=rows.map((r,i)=>fines[i]<=50&&purity[i]>=80);
  const operations=['add_reagent','add_solvent','add_catalyst','heat','cool_crystallize','seed_crystals','cool_crystallize','wait','measure','filter_crystals','terminate','measure'];
  if(actions.map(a=>a.operation).join(',')!==operations.join(',')||feasible.slice(0,4).some(Boolean)||!feasible[4]||feasible[10]||!feasible[11])throw Error('W04 sequence or feasibility changed');
  const at=(i,op)=>{const a=actions[i];if(a.operation!==op)throw Error(`B8 action ${i+1}`);return a;};
  const same=(a,b)=>Math.abs(a-b)<1e-8;
  if(!same(at(0,'add_reagent').amount_mol,.04)||!same(at(1,'add_solvent').volume_L,.08)||at(1,'add_solvent').solvent!==2||!same(at(2,'add_catalyst').catalyst_amount_mol,.005)||at(2,'add_catalyst').catalyst!==1||at(3,'heat').target_temperature_K!==355||at(3,'heat').duration_s!==3600||at(3,'heat').stirring_speed_rpm!==300||at(4,'cool_crystallize').target_temperature_K!==325||at(4,'cool_crystallize').duration_s!==7200||!same(at(5,'seed_crystals').seed_mass_g,.001)||at(6,'cool_crystallize').target_temperature_K!==250||at(6,'cool_crystallize').duration_s!==14400||at(7,'wait').duration_s!==14400||at(7,'wait').stirring_speed_rpm!==100||at(8,'measure').instrument!=='particle_size'||at(11,'measure').instrument!=='final_assay')throw Error('B8 recipe changed');
  if(rows.slice(0,4).some(r=>!r.actions.some(a=>a.operation==='quench'))||rows[4].actions.some(a=>a.operation==='quench')||rows[10].actions.find(a=>a.operation==='add_solvent')?.volume_L!==.04||JSON.stringify(rows[11].actions)!==JSON.stringify(actions))throw Error('W04 process comparison changed');
  const retest=result.recommendation_retest.batches[0].metrics;
  const intermediate=0.2661595046520233;
  // Local formal trajectory is intentionally outside Git. Verify it when present;
  // the reviewed readout above keeps the publication build portable.
  const trajectory=path.join(ROOT,'runs/formal/work-ii-c-five-world-20260920-v3-auto/sources/C-W04-B12-E-MisIndexed/trajectory.jsonl');
  try{
    const records=(await fs.readFile(trajectory,'utf8')).trim().split(/\r?\n/).map(JSON.parse);
    const reading=records.find(r=>r.experiment_index===7&&r.action?.operation==='measure'&&r.action?.instrument==='particle_size');
    if(!reading||reading.step!==97||!same(reading.observation.crystal_fines_fraction,intermediate))throw Error('B8 intermediate measurement changed');
  }catch(e){if(e.code!=='ENOENT')throw e;}
  const F=v=>v.toFixed(1);
  const s=slide(name,1080,'Figure 2. W04/MisIndexed twelve-batch concept. Pictorial instruments and thinking Agent are ImageGen assets; labels, data and arrows remain editable. Final assays and operations are generated from the formal summary. The in-process particle-size reading at source step 97 is distinct from the final assay. Agent questions are author reconstructions, not contemporaneous quotations; K1 followed all batches. Early quench effects are confounded.');
  const sharp=(await import(pathToFileURL(path.join(process.env.RUNTIME_NODE_MODULES,'sharp/dist/index.cjs')).href)).default;
  const asset=name=>path.join(ROOT,'paper/figures/final-ppt/assets',name);
  const ink='#27323A',black='#111820',muted='#596B78',border='#8295A2',teal='#087F97',rust='#C85A3A';
  function T(t,x,y,w,h=30,size=18,bold=false,color=ink,align='left'){return txt(s,t,x,y,w,h,size,bold,color,align);}
  function L(x1,y1,x2,y2,color=ink,width=1.4,dash=false){return line(s,x1,y1,x2,y2,color,width,dash);}
  function dot(x,y,color=teal,r=6){shape(s,'ellipse',x-r,y-r,r*2,r*2,color,color,1);}
  function arrow(x1,y,x2,color=ink){L(x1,y,x2,y,color,1.8);L(x2-7,y-5,x2,y,color,1.8);L(x2-7,y+5,x2,y,color,1.8);}
  function panel(y,h,id,title){shape(s,'rect',7,y,1426,h,'#FFFFFF',border,1.1);T(id,22,y+7,35,38,29,true,black);T(title,67,y+7,1340,39,24,true,ink);}

  // a: retain the two aligned trajectories and every printed source value.
  panel(6,367,'a','Twelve-batch history: fines and recovery');
  const x0=216,x1=1300,xx=i=>x0+(x1-x0)*i/11;
  const fy=v=>188-v/105*96,ry=v=>310-v/75*99;
  T('Fines (%)',27,139,132,34,19,false,ink);
  T('Recovery (%)',17,241,144,29,19,false,ink);
  T('(seed-excluded)',17,267,144,26,16,false,ink);
  L(165,93,165,188);L(165,188,1352,188);L(165,211,165,310);L(165,310,1352,310);
  for(const [v,y] of [[0,fy(0)],[50,fy(50)],[100,fy(100)]]){L(159,y,165,y);T(String(v),115,y-12,39,24,16,false,ink,'right');}
  for(const [v,y] of [[0,ry(0)],[25,ry(25)],[50,ry(50)],[75,ry(75)]]){L(159,y,165,y);T(String(v),115,y-12,39,24,16,false,ink,'right');}
  L(165,fy(50),1351,fy(50),'#88A9BA',1.5,true);
  T('Quality limit\n(≤ 50%)',1342,fy(50)-17,95,46,15,false,muted);
  for(let i=0;i<11;i++){
    L(xx(i),fy(fines[i]),xx(i+1),fy(fines[i+1]),feasible[i+1]?teal:rust,2.1);
    L(xx(i),ry(recovery[i]),xx(i+1),ry(recovery[i+1]),feasible[i+1]?teal:rust,2.1);
  }
  rows.forEach((_,i)=>{
    dot(xx(i),fy(fines[i]),feasible[i]?teal:rust,6);
    dot(xx(i),ry(recovery[i]),feasible[i]?teal:rust,6);
    T(F(fines[i]),xx(i)-31,fy(fines[i])-31,62,24,16,false,feasible[i]?teal:black,'center');
    T(F(recovery[i]),xx(i)-31,ry(recovery[i])-30,62,24,16,false,ink,'center');
    L(xx(i),310,xx(i),317,border,1);
    T(String(i+1),xx(i)-20,319,40,27,17,false,ink,'center');
  });
  T('Batch',666,342,100,27,17,false,ink,'center');
  T('B5\nfirst feasible',xx(4)-83,53,166,42,17,true,ink,'center');L(xx(4),97,xx(4),fy(fines[4])-36,ink,1.1);
  T('B8\nselected',xx(7)-65,53,130,42,17,true,ink,'center');L(xx(7),97,xx(7),fy(fines[7])-36,ink,1.1);
  T(`B11\nfines ${F(fines[10])}%`,xx(10)-72,16,144,45,17,true,ink,'center');L(xx(10),62,xx(10),fy(fines[10])-36,ink,1.1);
  T('B12\nrepeat',xx(11)-65,53,130,42,17,true,ink,'center');L(xx(11),97,xx(11),fy(fines[11])-36,ink,1.1);

  // b: ten ImageGen entities represent every one of the twelve recorded calls.
  panel(383,298,'b','Batch 8 (B8) experiment in full detail');
  const centres=[88,241,391,538,670,806,948,1080,1211,1355];
  const labels=[
    'Charge reagent\n+ S2 solvent\n+ C1 catalyst',
    'Heat toward\n355 K for 1 h\nat 300 rpm',
    'Controlled cool\ntoward 325 K\nfor 2 h',
    'Add 1 mg\nseed',
    'Cool toward\n250 K for 4 h',
    'Hold 4 h\nat 100 rpm',
    'Particle-size\ncheck',
    'Filter',
    'Terminate',
    'Final assay'
  ];
  centres.forEach((c,i)=>T(labels[i],c-(i===0?78:75),426,i===0?156:150,62,16,false,ink,'center'));
  // The transparent sprite sheet was generated as a whole. Crop only its
  // individual entities and place them without stretching; no instrument is
  // reconstructed from primitive PowerPoint shapes.
  const sheet=await fs.readFile(asset('figure02-b-instruments-imagegen.png'));
  const cuts=[0,210,430,650,870,1080,1300,1535,1730,1950,2172];
  const icons=[];
  for(let i=0;i<10;i++){
    const left=cuts[i],width=cuts[i+1]-left;
    const slice=await sharp(sheet).extract({left,top:175,width,height:350}).png().toBuffer();
    const segment=await sharp(slice).trim({background:'#00000000',threshold:8}).png().toBuffer();
    const {width:w,height:h}=await sharp(segment).metadata();
    const scale=Math.min(.46,130/h,95/w);
    icons.push({blob:segment,width:w*scale,height:h*scale});
  }
  const iconBottom=[632,632,632,632,632,632,606,632,610,596];
  icons.forEach((icon,i)=>s.images.add({blob:icon.blob,contentType:'image/png',fit:'contain',
    position:{left:centres[i]-icon.width/2,top:iconBottom[i]-icon.height,width:icon.width,height:icon.height},
    alt:`ImageGen illustration of B8 procedure stage ${i+1}: ${labels[i].replaceAll('\n',' ')}`}));
  T(`fines\n${F(100*intermediate)}%`,906,611,84,43,18,false,ink,'center');
  T(`recovery ${F(recovery[7])}%\npurity ${F(purity[7])}%\nfines ${F(fines[7])}%`,1268,605,161,62,17,false,ink,'center');
  for(let i=0;i<9;i++)arrow(centres[i]+54,574,centres[i+1]-54,black);

  // c: four columns and one directed path per row; the thinking Agent is raster artwork.
  panel(691,385,'c','Key observations, questions, and next tests');
  T('Observed',114,735,198,28,19,true,ink);
  T('Agent question*',441,735,252,28,19,true,ink);
  T('Next tested action',785,735,286,28,19,true,ink);
  T('Outcome',1210,735,180,28,19,true,ink);
  L(25,766,1414,766,border,1.4);
  L(25,850,1414,850,border,1.1);L(25,937,1414,937,border,1.1);
  const cases=[
    {y:776,ob:`B1–4:\nfines ${F(Math.min(...fines.slice(0,4)))}–${F(Math.max(...fines.slice(0,4)))}%`,q:'Where are\nfines forming?',act:'B5: omit quench;\ncool before seeding',out:`fines ${F(fines[4])}%;\nfirst feasible`,obsColor:rust,outColor:teal},
    {y:861,ob:`B5: feasible;\nrecovery ${F(recovery[4])}%`,q:'Do colder endpoints\nimprove recovery?',act:'B6/B7: end at 265/250 K;\nB8: seed 5 → 1 mg',out:`recovery ${F(recovery[5])} → ${F(recovery[6])} → ${F(recovery[7])}%;\nfines < 30%`,obsColor:teal,outColor:teal},
    {y:947,ob:'B8 best so far;\nB9–10 additional probes',q:'Does higher\nconcentration help?',act:'B11: S2 0.080 → 0.040 L',out:`B11 fines ${F(fines[10])}%, rejected;\nB12 repeats B8: ${F(fines[11])}%`,obsColor:teal,outColor:rust}
  ];
  const thought=await sharp(await fs.readFile(asset('figure02-c-agent-thought-imagegen.png')))
    .extract({left:55,top:45,width:2090,height:670}).png().toBuffer();
  cases.forEach(r=>{
    T(r.ob,42,r.y+4,236,62,19,false,r.obsColor);
    arrow(291,r.y+31,333,ink);
    s.images.add({blob:thought,contentType:'image/png',fit:'contain',
      position:{left:382,top:r.y-3,width:256,height:82},
      alt:'ImageGen illustration of an Agent writing notes and thinking'});
    T(r.q,479,r.y+11,151,49,16,false,ink,'center');
    arrow(692,r.y+31,731,ink);
    T(r.act,772,r.y+4,271,62,19,true,teal);
    arrow(1060,r.y+31,1100,ink);
    T(r.out,1134,r.y+4,271,62,18,true,r.outColor);
  });
  shape(s,'roundRect',25,1031,1389,36,'#F7FAFB',border,1);
  T('* Questions reconstructed from recorded actions, not contemporaneous model quotes. K1 was written after research; quench mechanism not isolated.',45,1036,1353,26,15,false,ink,'center');
}
