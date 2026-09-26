// Reuse scientific SVG text and data marks as editable slide objects.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const BUILD=process.argv[2];
if(!BUILD || !path.isAbsolute(BUILD)) throw new Error('Pass an absolute private build directory');
const RUNTIME='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(RUNTIME,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const f=JSON.parse(await fs.readFile(path.join(BUILD,'vector.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1440,height:1200}});
const slide=p.slides.add();
slide.background.fill='#FFFFFF';
const k=Math.min(1368/f.width,1128/f.height),dx=(1440-f.width*k)/2,dy=(1200-f.height*k)/2;
function fill(c,a=1){return c==='none'?'none':a>=.999?c:`${c}/${Math.round(a*100)}`;}
for(let j=0;j<f.objects.length;j++){
  const o=f.objects[j],name=`vector-0-${j}`;
  if(o.kind==='text'){
    const s=slide.shapes.add({geometry:'textbox',name,
      position:{left:dx+o.x*k,top:dy+o.y*k,width:o.w*k,height:o.h*k,rotation:o.rotation||0},
      fill:'none',line:{fill:'none',width:0}});
    s.text=o.text;
    s.text.style={typeface:'Times New Roman',fontSize:o.fontSize*k,bold:o.bold,italic:o.italic,
      color:o.fill,autoFit:'none',wrap:'none',verticalAlignment:'top',alignment:'left',
      insets:{top:0,bottom:0,left:0,right:0}};
  }else{
    const points=o.commands.flatMap(c=>c.slice(1));
    if(!points.length)continue;
    const xs=points.map(a=>a[0]),ys=points.map(a=>a[1]);
    const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(.001,Math.max(...xs)-x),h=Math.max(.001,Math.max(...ys)-y);
    const commands=o.commands.map(c=>c[0]==='Z'?{close:{}}:{[c[0]==='M'?'moveTo':'lineTo']:{x:(c.at(-1)[0]-x)*k,y:(c.at(-1)[1]-y)*k}});
    slide.shapes.add({geometry:'custom',name,position:{left:dx+x*k,top:dy+y*k,width:w*k,height:h*k},
      customPaths:[{width:w*k,height:h*k,commands}],fill:fill(o.fill,o.opacity*o.fillOpacity),
      line:{fill:fill(o.stroke,o.opacity*o.strokeOpacity),width:o.lineWidth*k,style:o.dash!=='none'?'dashed':'solid'}});
  }
}
await (await PresentationFile.exportPptx(p)).save(path.join(BUILD,'figure05-native.pptx'));
console.log(`Figure 5: native export complete, objects=${f.objects.length}`);
