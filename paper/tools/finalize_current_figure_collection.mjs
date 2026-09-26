import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const ROOT=path.resolve(import.meta.dirname,'../..');
const BUILD=path.join(os.tmpdir(),'chemworld-current-figure-collection');
const SKILL='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
process.env.RUNTIME_NODE_MODULES='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const FINAL=path.join(BUILD,`checked-${Date.now()}`,'chemworld-current-figures-editable.pptx');
await fs.mkdir(path.dirname(FINAL),{recursive:true});
const heartbeat=setInterval(()=>console.log('collection stage=package validation active'),30000);
try {
  await finalizePresentation({workspaceDir:BUILD,
    candidatePath:path.join(BUILD,'assembled-candidate.pptx'),finalPath:FINAL,
    pythonExecutable:path.join(ROOT,'.venv/Scripts/python.exe'),
    integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu','13716000,11430000'],
    explicitTotalSlideCount:17,requiredNativeChartOwnerSlides:[16],
    requiredEmbeddedWorkbookChartOwnerSlides:[16],materializeLiteralChartWorkbooks:false,
    verifyArtifactToolImport:true,receiptPath:path.join(BUILD,'validation.json'),
  });
  // The user-curated seven-slide source must not be replaced by this old selection.
  const output=path.join(ROOT,'output/pptx/chemworld-figure-collection-17.pptx');
  await fs.copyFile(FINAL,output);
  console.log(`collection stage=final complete output=${output}`);
} finally {clearInterval(heartbeat);}
