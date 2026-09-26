// Assemble an editable figure collection in manuscript order, preserving the artwork.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';

const RUNTIME = 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {Presentation, PresentationFile} = await import(pathToFileURL(path.join(RUNTIME, '@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const BUILD = path.join(os.tmpdir(), 'chemworld-current-figure-collection');
const figures = JSON.parse(await fs.readFile(path.join(BUILD, 'vectors.json'), 'utf8'));
const WIDTH = 1440, HEIGHT = 1200, MARGIN = 36;
const p = Presentation.create({slideSize: {width: WIDTH, height: HEIGHT}});
const heartbeat = setInterval(() => console.log('collection stage=PowerPoint export active'), 30000);

function text(slide, content, x, y, w, h, size, options={}) {
  const s = slide.shapes.add({geometry:'textbox', name:options.name || content.slice(0,70),
    position:{left:x,top:y,width:w,height:h,rotation:options.rotation || 0},
    fill:'none',line:{fill:'none',width:0}});
  s.text=content;
  s.text.style={typeface:options.font || 'Arial',fontSize:size,bold:!!options.bold,
    italic:!!options.italic,color:options.fill || '#24292D',autoFit:'none',wrap:'none',
    verticalAlignment:'top',alignment:'left',insets:{top:0,bottom:0,left:0,right:0}};
  return s;
}

const index=p.slides.add();
index.background.fill='#FFFFFF';
text(index,'ChemWorld manuscript figures',64,58,1280,68,48,{bold:true});
text(index,'Current main and supplementary figures',64,137,1240,44,27);
const descriptions=[
  'Controlled experimental worlds','Complete twelve-batch research session',
  'Goals, research paths and predictions','Six outcomes under larger research envelopes',
  'Equilibrium evidence and regime reversal','Crystallization prediction and calibration',
  'Prior overview: electrochemistry','Prior overview: partitioning and reaction discovery',
  'Prior overview: reaction optimization and equilibrium','Prior overview: crystallization and purification',
  'Prior differences: reaction','Prior differences: equilibrium regimes',
  'Complete six-outcome budget matrix','Sealed predictions and subsequent reflection',
  'Additional delivery and prediction outcomes','Goal comparisons within each world',
];
text(index,'FIGURE',64,218,270,32,20,{bold:true});
text(index,'CONTENT',350,218,960,32,20,{bold:true});
figures.forEach((f,i)=>{
  const y=269+i*49;
  text(index,f.name,64,y,280,34,22);
  text(index,descriptions[i],350,y,1000,34,22);
});
index.speakerNotes.textFrame.setText('Figures follow the current English manuscript and its supplementary information. Source: paper/venues/ncs/article.md and paper/tools/build_venue_manuscripts.py.');

function fill(color, opacity=1) {
  if (color==='none') return 'none';
  return opacity>=.999 ? color : `${color}/${Math.round(opacity*100)}`;
}

function drawPath(slide,o,k,dx,dy,name) {
  const points=o.commands.flatMap(c=>c.slice(1));
  if(!points.length)return;
  const xs=points.map(a=>a[0]),ys=points.map(a=>a[1]);
  const x=Math.min(...xs),y=Math.min(...ys);
  const w=Math.max(.001,Math.max(...xs)-x),h=Math.max(.001,Math.max(...ys)-y);
  // Placeholder segments are replaced with exact native Bezier commands during packaging.
  const commands=o.commands.map(c=>c[0]==='Z'?{close:{}}:{[c[0]==='M'?'moveTo':'lineTo']:{x:(c.at(-1)[0]-x)*k,y:(c.at(-1)[1]-y)*k}});
  slide.shapes.add({geometry:'custom',name,
    position:{left:dx+x*k,top:dy+y*k,width:w*k,height:h*k},
    customPaths:[{width:w*k,height:h*k,commands}],
    fill:fill(o.fill,o.opacity*o.fillOpacity),
    line:{fill:fill(o.stroke,o.opacity*o.strokeOpacity),width:o.lineWidth*k,
      style:o.dash!=='none'?'dashed':'solid'}});
}

for(let i=0;i<figures.length;i++) {
  const f=figures[i],s=p.slides.add();
  s.background.fill='#FFFFFF';
  s.speakerNotes.textFrame.setText(`${f.name}. ${descriptions[i]}. Source: ${f.source}.`);
  if(f.kind==='vector') {
    const k=Math.min((WIDTH-2*MARGIN)/f.width,(HEIGHT-2*MARGIN)/f.height);
    const dx=(WIDTH-f.width*k)/2,dy=(HEIGHT-f.height*k)/2;
    f.objects.forEach((o,j)=>{
      const name=`vector-${i}-${j}`;
      if(o.kind==='text')text(s,o.text,dx+o.x*k,dy+o.y*k,o.w*k,o.h*k,o.fontSize*k,{...o,name});
      else drawPath(s,o,k,dx,dy,name);
    });
  }
  console.log(`collection stage=author completed=${i+1}/${figures.length} figure=${f.name}`);
}
await (await PresentationFile.exportPptx(p)).save(path.join(BUILD,'vector-candidate.pptx'));
clearInterval(heartbeat);
console.log('collection stage=author complete');
