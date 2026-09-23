// Reader-facing views of retained results. No new experiments or fitted curves.
export function addEqEvidence(ctx) {
  const {slide,axis,txt,DATA,C,ARMS,shape,line}=ctx;
  const rows=DATA.eq_process, worlds=['W01','W02','W03','W04','W05'];
  if(rows.length!==15||rows.reduce((n,r)=>n+r.batches.length,0)!==180)throw Error('EQ denominator');
  const s=slide('figure05-eq-evidence',650,'Five-world reference versus original prediction comparison at Q08, 13.3 micromolar. All 15 predictions and 180 source assays retained. The shaded band is the pooled source minimum/maximum, not an uncertainty interval. Native manuscript Table 1 reports regime aggregates; Table F1 retains every original interval. No experiments or internal reasoning reconstructed.');
  const labels=['Withheld reference',...ARMS], colors=['#CBD5DC',C.Opaque,C.Aligned,C.MisIndexed];
  txt(s,'Same dilute recipe in each world: 13.3 µM',88,13,1240,36,22,true);
  let lx=88;
  labels.forEach((label,i)=>{shape(s,'rect',lx,68,22,16,colors[i],'none',0);txt(s,label,lx+33,56,280,38,20);lx+=i===0?325:255;});
  const x=40,y=115,w=1240,h=435,px=x+w*.098,py=y+h*.053,pw=w*.90,ph=h*.84;
  const obs=rows.flatMap(r=>r.batches.map(b=>100*b.final_responses.acid_dissociation_fraction));
  const lo=Math.min(...obs),hi=Math.max(...obs);
  shape(s,'rect',px,py+(82-hi)/82*ph,pw,(hi-lo)/82*ph,'#E9EDEF','none',0);
  const series=labels.map((name,j)=>({
    name:'EQ '+name,values:worlds.map(world=>{
      const rr=rows.filter(r=>r.world===world);
      if(rr.length!==3||new Set(rr.map(r=>r.q08.reference_means.acid_dissociation_fraction)).size!==1)throw Error('EQ reference mismatch');
      return Number((100*(j===0?rr[0].q08.reference_means.acid_dissociation_fraction:rr.find(r=>r.arm===name).q08.predictions.acid_dissociation_fraction.estimate)).toPrecision(12));
    }),fill:colors[j],line:{fill:'none',width:0},valuesFormatCode:'0.0'
  }));
  s.charts.add('bar',{
    position:{left:x,top:y,width:w,height:h},categories:worlds.map((_,i)=>'World '+(i+1)),series,
    titlePlacement:'none',hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:85},
    xAxis:{visible:true,tickLabelPosition:'nextTo',textStyle:{typeface:'Arial',fontSize:21,fill:C.ink},line:{fill:C.ink,width:1}},
    yAxis:{...axis('Dissociation (%)',0,82,20,'0'),majorGridlines:{fill:'#E3E8EB',width:.7}},
    dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:'Arial',fontSize:18,fill:C.ink}},
    chartFill:'none',plotAreaFill:'none',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}
  });
  txt(s,'Observed in',1274,400,145,30,18,false,C.muted);
  txt(s,'research',1274,429,145,30,18,false,C.muted);
  txt(s,`${lo.toFixed(1)}–${hi.toFixed(1)}%`,1274,473,145,32,20,true,C.muted);
  line(s,px+pw,py+(82-(lo+hi)/2)/82*ph,1260,py+(82-(lo+hi)/2)/82*ph,C.muted,1);
  txt(s,'Band: pooled range of 180 research observations. Reference outcomes were withheld.',88,571,1280,34,20,false,C.muted);
  txt(s,'Original 80% prediction intervals: Supplementary Table F1. Regime statistics: Table 1.',88,607,1280,30,18,false,C.muted);
}

export function addCrystalComparison(ctx) {
  const {slide,panel,chart,axis,series,seg,txt,legend,DATA,C,ARMS,mean,line}=ctx;
  const rows=DATA.crystal;
  if(rows.length!==30)throw Error('Crystallization denominator');
  const s=slide('figure06-purity-generalization',1110,'All 30 original crystallization campaigns, including the retained source-assay shortfall. Source: BASELINE_REANALYSIS.json, retained-figure-data.json. Error differences are agent MAE minus the public source-mean MAE in percentage points. No ratios or logarithmic errors. Vertical offsets in panels b/c only separate campaigns.');
  panel(s,'a',25,15,'Measured purity stays high; forecasts depart from it');
  const groups=[rows.map(r=>r.response_diagnostics.crystal_purity.source_observed_mean*100),rows.map(r=>r.response_diagnostics.crystal_purity.reference_mean*100),...[12,24].map(b=>rows.filter(r=>r.budget===b).map(r=>r.response_diagnostics.crystal_purity.prediction_mean*100))];
  const cols=[C.muted,C.ink,C.b12,C.b24],purity=[];
  groups.forEach((vv,i)=>{
    purity.push(series('Purity observations '+i,vv.map((_,j)=>i+(j/(vv.length-1)-.5)*.22),vv,cols[i]));
    purity.push(seg('Purity mean '+i,[i-.22,i+.22],[mean(vv),mean(vv)],cols[i],3));
  });
  chart(s,purity,70,79,1300,390,axis('',-.5,3.5,1,'0',false),axis('Campaign mean purity (%)',84,100,4,'0'));
  const labels=[['Measured in research','30 campaigns'],['Withheld outcomes','30 campaigns'],['Agent forecast: 12 batches','15 campaigns'],['Agent forecast: 24 batches','15 campaigns']];
  labels.forEach(([label,n],i)=>{
    const cx=70+1300*.075+(i+.5)/4*(1300*.90);
    txt(s,`${mean(groups[i]).toFixed(1)}%`,cx-125,49,250,40,28,true,cols[i],'center');
    txt(s,label,cx-147,472,294,34,20,true,C.ink,'center');
    txt(s,n,cx-147,507,294,30,18,false,C.muted,'center');
  });
  txt(s,'335 of 360 individual purity forecasts fall below the withheld reference.',95,557,1260,38,23,true,C.ink,'center');
  line(s,25,621,1415,621,C.grid);
  const defs=[['crystal_yield','Recovery',-30,40,10],['crystal_purity','Purity',-2,12,2]];
  defs.forEach(([metric,title,min,max,step],i)=>{
    const x=25+i*720;
    panel(s,i?'c':'b',x,639,`${title} prediction error`);
    const ordered=[...rows].sort((a,b)=>(a.agent_mae[metric]-a.public_baselines.mae.public_mean[metric])-(b.agent_mae[metric]-b.public_baselines.mae.public_mean[metric]));
    const packed=[];
    // Deterministic visual offsets keep nearby points apart without encoding a response.
    ordered.forEach(r=>{
      const d=100*(r.agent_mae[metric]-r.public_baselines.mae.public_mean[metric]);
      const options=[0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7];
      const level=options.find(k=>packed.every(p=>Math.abs(p.d-d)/(max-min)*560>13||Math.abs(p.level-k)>=1.4))??7;
      packed.push({r,d,level,y:.5+level*.05});
    });
    const ss=[seg('Equal accuracy '+metric,[0,0],[.05,.95],C.muted,1.6),...ARMS.map(a=>{
      const rr=packed.filter(p=>p.r.arm===a);
      return series('Error difference '+metric+' '+a,rr.map(p=>p.d),rr.map(p=>p.y),C[a]);
    })];
    chart(s,ss,x+10,738,670,245,axis('MAE difference (percentage points)',min,max,step,'0'),axis('',0,1,1,'0',false));
    const better=packed.filter(p=>p.d<0).length;
    txt(s,i?'Observed mean more accurate in 30/30 campaigns':`Agent more accurate in ${better}/30 campaigns`,x+30,686,650,38,22,true,i?C.bad:C.Aligned,'center');
    txt(s,'Negative: agent better. Positive: observed mean better.',x+40,991,620,32,18,false,C.muted,'center');
  });
  legend(s,ARMS.map(a=>[a,C[a]]),1054,440);
}
