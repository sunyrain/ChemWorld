import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const ROOT=path.resolve(import.meta.dirname,'../..'),BUILD=process.argv[2];
if(!BUILD || !path.isAbsolute(BUILD)) throw new Error('Pass an absolute private build directory');
const SKILL='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
process.env.RUNTIME_NODE_MODULES='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const final=path.join(BUILD,`checked-${Date.now()}`,'chemworld-current-figures-editable.pptx');
await fs.mkdir(path.dirname(final),{recursive:true});
const heartbeat=setInterval(()=>console.log('Figure 5 collection: package validation active'),30000);
try{
  await finalizePresentation({workspaceDir:BUILD,candidatePath:path.join(BUILD,'assembled-candidate.pptx'),finalPath:final,
    pythonExecutable:path.join(ROOT,'.venv/Scripts/python.exe'),
    integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu','13716000,11430000'],
    explicitTotalSlideCount:7,requiredNativeChartOwnerSlides:[],materializeLiteralChartWorkbooks:false,
    fontPolicy:{basis:'user_request',families:['Times New Roman']},
    verifyArtifactToolImport:true,
    receiptPath:path.join(BUILD,`${path.basename(path.dirname(final))}.validation.json`)});
  await fs.writeFile(path.join(BUILD,'checked-path.txt'),final);
  console.log(`Figure 5 collection finalized: ${final}`);
}finally{clearInterval(heartbeat);}
