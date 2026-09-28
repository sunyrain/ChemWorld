import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const BUILD=process.argv[2];
if(!BUILD || !path.isAbsolute(BUILD)) throw new Error('Pass an absolute private build directory');
const RUNTIME='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(RUNTIME,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const p=Presentation.create({slideSize:{width:1440,height:1200}});
function fill(c,a=1){return c==='none'?'none':a>=.999?c:`${c}/${Math.round(a*100)}`;}
for(const [index,stem] of ['figure04','figure05'].entries()){
 const f=JSON.parse(await fs.readFile(path.join(BUILD,`${stem}-vector.json`),'utf8'));
 const slide=p.slides.add();slide.background.fill='#FFFFFF';
 const k=Math.min(1368/f.width,1128/f.height),dx=(1440-f.width*k)/2,dy=(1200-f.height*k)/2;
 for(let j=0;j<f.objects.length;j++){
  const o=f.objects[j],name=`vector-${index}-${j}`;
  if(o.kind==='text'){
   const s=slide.shapes.add({geometry:'textbox',name,position:{left:dx+o.x*k,top:dy+o.y*k,width:o.w*k,height:o.h*k,rotation:o.rotation||0},fill:'none',line:{fill:'none',width:0}});
   s.text=o.text;s.text.style={typeface:'Times New Roman',fontSize:o.fontSize*k,bold:o.bold,italic:o.italic,color:o.fill,autoFit:'none',wrap:'none',verticalAlignment:'top',alignment:'left',insets:{top:0,bottom:0,left:0,right:0}};
  }else{
   const points=o.commands.flatMap(c=>c.slice(1));if(!points.length)continue;
   const xs=points.map(a=>a[0]),ys=points.map(a=>a[1]),x=Math.min(...xs),y=Math.min(...ys),w=Math.max(.001,Math.max(...xs)-x),h=Math.max(.001,Math.max(...ys)-y);
   const commands=o.commands.map(c=>c[0]==='Z'?{close:{}}:{[c[0]==='M'?'moveTo':'lineTo']:{x:(c.at(-1)[0]-x)*k,y:(c.at(-1)[1]-y)*k}});
   slide.shapes.add({geometry:'custom',name,position:{left:dx+x*k,top:dy+y*k,width:w*k,height:h*k},customPaths:[{width:w*k,height:h*k,commands}],fill:fill(o.fill,o.opacity*o.fillOpacity),line:{fill:fill(o.stroke,o.opacity*o.strokeOpacity),width:o.lineWidth*k,style:o.dash!=='none'?'dashed':'solid'}});
  }
 }
 const imageMetadata=path.join(BUILD,`${stem}-image.json`);
 try{
  const meta=JSON.parse(await fs.readFile(imageMetadata,'utf8'));
  const pos=meta.position;
  slide.images.add({blob:await fs.readFile(meta.path),contentType:'image/png',
   alt:'Illustration of a researcher reviewing the completed public report',fit:'cover',
   position:{left:dx+pos.left*k,top:dy+pos.top*k,width:pos.width*k,height:pos.height*k},crop:meta.crop});
 }catch(error){if(error.code!=='ENOENT')throw error;}
 slide.speakerNotes.textFrame.setText(index===0?'Retained Sol evidence-closeout EQ_AUTONOMOUS_PROCESS.json and STORY_WORLD_ANALYSIS.json, plus the 60-cell eq-astra-medium-20260927/joint_cell_metrics.csv. Five reused worlds, three information arms, 12 source batches each. Other nine queries are not all in-distribution. Error bars are world sample SD, not confidence intervals.':'Retained EQ source trajectories and public K1/Q accounts. All 75 source minima include positive reagent loading only. Astra W03/MisIndexed: all 12 assays. K1 follows completion of experiments and precedes Q. The condensed K1 wording is not contemporaneous internal reasoning. Sol/Opaque preserves all five worlds and original intervals. Data sources: source-data.json alongside the final figures.');
 console.log(`Native figure ${index+4}: ${f.objects.length} objects`);
}
await (await PresentationFile.exportPptx(p)).save(path.join(BUILD,'new-figures-native.pptx'));
