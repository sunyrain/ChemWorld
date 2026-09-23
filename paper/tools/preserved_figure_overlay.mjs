import fs from 'node:fs/promises';
import path from 'node:path';
import {illustrations} from './preserved_figure_labels.mjs';
import {pathToFileURL} from 'node:url';
const {default:sharp}=await import(pathToFileURL('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.cjs').href);

export async function addPreservedFigure(p, name, root, width) {
 const spec=illustrations[name], scale=width/spec.width;
 const slide=p.slides.add(); slide.background.fill='#FFFFFF';
 const source=path.join(root,'paper/figures/ncs-full',name+'.png');
 const cropped=await sharp(await fs.readFile(source)).extract({left:0,top:spec.cropTop,width:spec.width,height:spec.height-spec.cropTop}).png().toBuffer();
 slide.images.add({blob:cropped,contentType:'image/png',
  position:{left:0,top:0,width,height:(spec.height-spec.cropTop)*scale},
  fit:'contain',
  alt:'Approved original illustration; overall title cropped; editable typography overlays'});
 const sizes={body:20,small:18,micro:16,tiny:14,heading:27,value:30,panel:30};
 // Compact legends and qualification details have a consistent smaller tier.
 // No automatic text shrink: the label specification contains explicit line breaks.
 for(const [text,x,y,w,h,role='body',align='left',background=null,color='#0b2450'] of spec.labels){
  const pos={left:x*scale,top:(y-spec.cropTop)*scale,width:w*scale,height:h*scale};
  const pad=role==='panel'?0:1.5;
  slide.shapes.add({geometry:'rect',position:{left:pos.left-pad,top:pos.top-pad,width:pos.width+2*pad,height:pos.height+2*pad},fill:background||'#FFFFFF',line:{fill:'none',width:0}});
  const box=slide.shapes.add({geometry:'textbox',position:pos,fill:'none',line:{fill:'none',width:0}});
  box.text=text;
  box.text.style={typeface:'Arial',fontSize:sizes[role],bold:['heading','value','panel'].includes(role),
   color,alignment:align,verticalAlignment:'middle',wrap:'none',autoFit:'none',
   insets:{left:0,right:0,top:0,bottom:0}};
 }
 // Restore only existing graphical marks that touch a text mask boundary.
 const regions=name==='figure04-research-paths'?[[958,752,132,28],[24,1090,1076,37]]:
  name==='figure07-posttest-reflection'?[[261,183,21,91],[512,703,4,68],[185,770,324,4],[747,766,326,4],[1073,704,4,62]]:[];
 for(const [x,y,w,h]of regions){
  const piece=await sharp(await fs.readFile(source)).extract({left:x,top:y,width:w,height:h}).png().toBuffer();
  slide.images.add({blob:piece,contentType:'image/png',fit:'contain',position:{left:x*scale,top:(y-spec.cropTop)*scale,width:w*scale,height:h*scale},alt:'Unchanged original graphical mark'});
 }
 slide.speakerNotes.textFrame.setText(
  `Retained artwork: ${path.relative(root,source)}. Only the overall title area and typography are edited. `+
  'Illustrations remain raster artwork; overlaid labels are editable PowerPoint text. '+
  (name.includes('research-paths')?'Original C-W05 Aligned independent 12/24 sessions. Starred considerations are illustrative; immediate thoughts were not recorded.':
   name.includes('posttest')?'Original C-W05 Q/K2. Reflection received no reference feedback. Proposed cooling experiment was not executed. Evaluator reference is for reheating only.':
   'ChemWorld framework and retained 240-campaign programme. No new evidence.'));
 return {name,height:Math.ceil((spec.height-spec.cropTop)*scale),slide};
}
