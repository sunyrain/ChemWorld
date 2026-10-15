import * as THREE from 'three';
import { GLTFLoader } from '/vendor/loaders/GLTFLoader.js';
import { OrbitControls } from '/vendor/controls/OrbitControls.js';
import { frameAsset, visibleMetrics, OPERATIONS, METRICS } from './projection.mjs';

const $ = id => document.getElementById(id);
const state = {slug:null, bundle:null, generation:0, selected:null, wire:false, records:false, step:0, demo:null};
let renderer, scene, camera, orbit, assembly, sourceFrame, model, bounds;
let meshes = [], components = new Map(), joints = new Map(), nodeComponent = new Map();
const raycaster = new THREE.Raycaster();
const originalMaterials = new Map();
const baseName = name => name.replace(/\.\d{3}$/, '');
const ancestor = (a, node) => { for (let p = node.parent; p; p = p.parent) if (p === a) return true; return false; };

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text != null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

async function json(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url} · HTTP ${response.status}`);
  return response.json();
}

function initializeRenderer() {
  const viewport = $('viewport');
  renderer = new THREE.WebGLRenderer({antialias:true, alpha:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.3;
  viewport.append(renderer.domElement);
  scene = new THREE.Scene();
  scene.background = new THREE.Color('#ffffff');
  camera = new THREE.PerspectiveCamera(33, 1, .001, 100);
  orbit = new OrbitControls(camera, renderer.domElement);
  orbit.enableDamping = true;
  orbit.dampingFactor = .09;
  orbit.autoRotateSpeed = .7;
  orbit.maxPolarAngle = Math.PI * .86;
  scene.add(new THREE.HemisphereLight(0xffffff, 0xb5c5bd, 2.8));
  for (const [position, intensity] of [[[2,4,3],3],[[-3,2,-2],2],[[0,1,-4],1]]) {
    const light = new THREE.DirectionalLight(0xffffff, intensity);
    light.position.fromArray(position);
    scene.add(light);
  }
  // Small generated studio environment: local, no image downloads or external renderer.
  const pixels = new Uint8Array(128 * 64 * 4);
  for (let y = 0; y < 64; y++) for (let x = 0; x < 128; x++) {
    const lightPanel = y < 35 && ((x > 15 && x < 27) || (x > 76 && x < 102));
    const value = lightPanel ? 255 : Math.round(175 - y * 1.2);
    const i = (y * 128 + x) * 4;
    pixels.set([value, value, value, 255], i);
  }
  const texture = new THREE.DataTexture(pixels,128,64);
  texture.mapping = THREE.EquirectangularReflectionMapping;
  texture.needsUpdate = true;
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromEquirectangular(texture).texture;
  texture.dispose(); pmrem.dispose();
  new ResizeObserver(() => {
    const {width,height} = viewport.getBoundingClientRect();
    renderer.setSize(width,height);
    camera.aspect = width / Math.max(1,height);
    camera.updateProjectionMatrix();
  }).observe(viewport);
  renderer.setAnimationLoop(() => {
    if (!document.hidden) {orbit.update(); renderer.render(scene,camera);}
  });
  let down = null;
  renderer.domElement.addEventListener('pointerdown', event => {down=[event.clientX,event.clientY];});
  renderer.domElement.addEventListener('pointerup', event => {
    if (!down || event.button !== 0 || Math.hypot(event.clientX-down[0],event.clientY-down[1]) > 5) return;
    const r = viewport.getBoundingClientRect();
    raycaster.setFromCamera(new THREE.Vector2((event.clientX-r.left)/r.width*2-1,-(event.clientY-r.top)/r.height*2+1),camera);
    const hit = raycaster.intersectObjects(meshes,false)[0];
    selectComponent(hit ? nodeComponent.get(hit.object) : null);
  });
}

function disposeAssembly() {
  if (!assembly) return;
  scene.remove(assembly);
  const disposed = new Set();
  assembly.traverse(node => {
    node.geometry?.dispose();
    for (const mat of node.material ? [node.material].flat() : []) {
      for (const value of Object.values(mat)) if (value?.isTexture && !disposed.has(value)) {value.dispose();disposed.add(value);}
      mat.dispose();
    }
  });
  meshes=[]; components.clear(); joints.clear(); nodeComponent.clear(); originalMaterials.clear();
}

function mapComponents(bundle) {
  const names = new Map();
  model.traverse(node => {names.set(node.name,node);if (!names.has(baseName(node.name))) names.set(baseName(node.name),node);});
  for (const component of bundle.components) {
    const objects = (component.objects ?? []).map(name => names.get(name) ?? names.get(baseName(name))).filter(Boolean);
    const tops = objects.filter(node => !objects.some(other => other!==node && ancestor(other,node)));
    const parts = [];
    tops.forEach(top => top.traverse(node => {if (node.isMesh) parts.push(node);}));
    components.set(component.id,{tops,parts,component});
  }
  // Specific components win over aggregate components such as the entire pH meter.
  for (const [id,entry] of [...components].sort((a,b) => b[1].parts.length-a[1].parts.length)) {
    for (const part of entry.parts) nodeComponent.set(part,id);
  }
}

// Adapted from ChemLab-Assets Explorer (MIT): retain world transforms when creating joint pivots.
function buildJoints(bundle) {
  const byChild = new Map(bundle.joints.map(joint => [joint.child,joint]));
  const visited = new Set();
  function make(joint) {
    if (joints.has(joint.name)) return joints.get(joint.name).pivot;
    if (visited.has(joint.name)) return sourceFrame;
    visited.add(joint.name);
    const parentJoint = byChild.get(joint.parent);
    const parent = parentJoint && parentJoint!==joint ? make(parentJoint) : sourceFrame;
    const pivot = new THREE.Group();
    parent.updateWorldMatrix(true,false);
    pivot.position.copy(parent.worldToLocal(sourceFrame.localToWorld(new THREE.Vector3(...joint.origin_m))));
    parent.add(pivot);
    pivot.updateWorldMatrix(true,false);
    const id = [joint.child,joint.child.replace(/_link$/,''),joint.child.replace(/_joint$/,'')].find(key=>components.has(key));
    let tops = components.get(id)?.tops ?? [];
    if (!tops.length) {
      const matches=[];
      const linkNames=[joint.child,joint.child.replace(/_link$/,'')];
      // The pH instrument uses URDF-only button links; its GLB has named key meshes instead.
      const key=bundle.slug==='metrohm_914'?joint.name.match(/^btn_keypad_key_(pwr|cal|back)$/)?.[1]:null;
      const keyNames=key?[`metrohm_914__key_${key}`,`metrohm_914__key_label_${key.toUpperCase()}_glb_mesh`]:[];
      model.traverse(node=>{
        if(linkNames.includes(node.name) || linkNames.includes(node.name.split('__')[1]) || keyNames.includes(node.name)) matches.push(node);
      });
      tops=matches.filter(node=>!matches.some(other=>other!==node&&ancestor(other,node)));
    }
    tops.forEach(top => pivot.attach(top));
    joints.set(joint.name,{pivot,rest:pivot.position.clone(),joint,id,available:tops.length>0});
    return pivot;
  }
  bundle.joints.forEach(make);
}

function fitView() {
  if (!bounds) return;
  const center=bounds.getCenter(new THREE.Vector3());
  const size=bounds.getSize(new THREE.Vector3());
  const diagonal=size.length();
  const distance=diagonal/Math.tan(THREE.MathUtils.degToRad(camera.fov/2))*.63 / Math.min(1,camera.aspect);
  camera.position.copy(center).add(new THREE.Vector3(.85,.8,1.2).normalize().multiplyScalar(distance));
  camera.near=Math.max(.0001,diagonal/200);
  camera.far=diagonal*60;
  camera.updateProjectionMatrix();
  orbit.target.copy(center);
  orbit.minDistance=diagonal*.45;
  orbit.maxDistance=diagonal*8;
  orbit.update();
}

function setupModel(bundle,root) {
  disposeAssembly();
  assembly=new THREE.Group();
  sourceFrame=new THREE.Group();
  sourceFrame.rotation.x=-Math.PI/2;
  assembly.add(sourceFrame);
  const orientation=new THREE.Group();
  model=root;
  orientation.add(model);
  // Compare both frames to the declared metric dimensions; some upstream flags disagree.
  function error(rotation) {
    orientation.rotation.x=rotation;
    orientation.updateMatrixWorld(true);
    const size=new THREE.Box3().setFromObject(orientation).getSize(new THREE.Vector3()).toArray();
    return Math.max(...size.map((v,i)=>Math.abs(v-bundle.size_m[i])));
  }
  const flat=error(0),rotated=error(Math.PI/2);
  orientation.rotation.x=rotated+.002<flat?Math.PI/2:flat+.002<rotated?0:bundle.glb_up==='y'?Math.PI/2:0;
  sourceFrame.add(orientation);
  // Before the root joins the scene, object bounds above are in the asset frame.
  model.traverse(node=>{
    if (!node.isMesh) return;
    node.material=Array.isArray(node.material)?node.material.map(m=>m.clone()):node.material.clone();
    meshes.push(node);
    for (const mat of [node.material].flat()) originalMaterials.set(mat,{emissive:mat.emissive?.clone(),intensity:mat.emissiveIntensity});
  });
  mapComponents(bundle);
  scene.add(assembly);
  assembly.updateMatrixWorld(true);
  buildJoints(bundle);
  bounds=new THREE.Box3().setFromObject(assembly);
  const size=bounds.getSize(new THREE.Vector3()),center=bounds.getCenter(new THREE.Vector3());
  const grid=new THREE.GridHelper(Math.max(size.x,size.z)*2.4,24,0xc9dcd4,0xeaf1ed);
  grid.position.set(center.x,bounds.min.y-.001,center.z);
  assembly.add(grid);
  fitView();
  fillInspector(bundle);
  applyMaterials();
  $('model-status').textContent=`已载入 · ${meshes.length} 个网格`;
  $('model-status').dataset.loaded=state.slug;
  $('loading').hidden=true;
  $('model-stats').replaceChildren(
    element('span',`${bundle.components.length} 个部件`),
    element('span',`${[...joints.values()].filter(j=>j.available).length}/${bundle.joints.length} 个关节可动`),
    element('span',`${bundle.size_m.map(v=>Math.round(v*1000)).join(' × ')} mm`));
}

function applyMaterials() {
  for (const mesh of meshes) for (const material of [mesh.material].flat()) {
    material.wireframe=state.wire;
    const original=originalMaterials.get(material);
    if (material.emissive && original?.emissive) {
      const selected=state.selected && nodeComponent.get(mesh)===state.selected;
      material.emissive.copy(selected?new THREE.Color('#28a488'):original.emissive);
      material.emissiveIntensity=selected ? 0.45 : original.intensity;
    }
  }
}

function selectComponent(id) {
  state.selected=id??null;
  $('component').value=id??'';
  const entry=components.get(id);
  $('component-description').textContent=entry?.component.function_zh??'选择一个部件，查看上游提供的用途说明。';
  $('pick-label').hidden=!entry;
  $('pick-label').textContent=entry?.component.name_zh??'';
  applyMaterials();
}

function setJoint(entry,value) {
  const axis=new THREE.Vector3(...entry.joint.axis).normalize();
  if (entry.joint.type==='prismatic') entry.pivot.position.copy(entry.rest).addScaledVector(axis,value);
  else entry.pivot.quaternion.setFromAxisAngle(axis,value);
  entry.pivot.updateMatrixWorld(true);
}

function fillInspector(bundle) {
  $('component').replaceChildren(new Option('点击模型或在这里选择',''));
  for (const c of bundle.components) if (components.get(c.id)?.parts.length) $('component').add(new Option(c.name_zh||c.id,c.id));
  $('joints').replaceChildren();
  for (const [index,entry] of [...joints.values()].entries()) {
    const joint=entry.joint;
    const label=element('label');
    const component=components.get(entry.id)?.component;
    label.append(element('span',component?.name_zh||joint.name));
    const output=element('output','0');
    label.append(output);
    const input=element('input');
    input.type='range';input.id=`joint-${index}`;label.htmlFor=input.id;
    const slide=joint.type==='prismatic';
    input.min=joint.lower??(slide?0:-Math.PI);
    input.max=joint.upper??(slide ? 0.05 : Math.PI);
    input.step=(Number(input.max)-Number(input.min))/200||.001;
    input.value='0';input.disabled=!entry.available;
    const update=()=>{
      const value=Number(input.value);
      output.textContent=!entry.available?'暂无部件绑定':slide?`${(value*1000).toFixed(1)} mm`:`${THREE.MathUtils.radToDeg(value).toFixed(0)}°`;
      if (entry.available) setJoint(entry,value);
    };
    input.addEventListener('input',update);
    entry.input=input;entry.update=update;update();
    const row=element('div',null,'joint');row.append(label,input);$('joints').append(row);
  }
  selectComponent(null);
}

async function selectInstrument(slug) {
  if (slug===state.slug && $('model-status').dataset.loaded===slug) return;
  state.slug=slug;
  const generation=++state.generation;
  $('loading').hidden=false;
  $('loading').textContent='正在读取本地模型…';
  $('model-status').textContent='载入中';
  delete $('model-status').dataset.loaded;
  $('joints').replaceChildren();
  $('component').disabled=true;
  document.querySelectorAll('.instrument').forEach(button=>{
    button.classList.toggle('active',button.dataset.slug===slug);
    button.setAttribute('aria-pressed',String(button.dataset.slug===slug));
  });
  history.replaceState(null,'',`#${slug}`);
  try {
    const bundle=await json(`/data/${slug}/bundle.json`);
    if (generation!==state.generation) return;
    state.bundle=bundle;
    $('maker').textContent=bundle.maker.toUpperCase();
    $('model-title').textContent=bundle.model;
    const gltf=await new GLTFLoader().loadAsync(`/data/${slug}/model.glb`,event=>{
      if (generation===state.generation && event.total) $('loading').textContent=`正在读取本地模型 · ${Math.round(event.loaded/event.total*100)}%`;
    });
    if (generation!==state.generation) {
      gltf.scene.traverse(node=>{node.geometry?.dispose();for(const m of node.material?[node.material].flat():[]) m.dispose();});
      return;
    }
    setupModel(bundle,gltf.scene);
    $('component').disabled=false;
    if (state.records) renderRecord(false);
  } catch(error) {
    if (generation!==state.generation) return;
    $('model-status').textContent='载入失败';
    $('loading').textContent=`模型未能载入：${error.message}。刷新页面可重试。`;
    console.error(error);
  }
}

function renderRecord(follow=true) {
  const frame=state.demo.frames[state.step];
  $('timeline').value=String(state.step);
  $('step-label').textContent=`${state.step} / ${state.demo.frames.length-1}`;
  $('operation').textContent=`${OPERATIONS[frame.operation]??'初始状态'}${frame.instrument?` · ${frame.instrument}`:''}`;
  const asset=frameAsset(frame);
  if (follow && asset && asset!==state.slug) selectInstrument(asset);
  $('mapping').textContent=asset===state.slug?'当前设备用于对应操作类别的外观示意；原实验没有指定此品牌或型号。':asset?'这一步对应其他设备类别；当前仪器仅供外观浏览。':'此步不映射到首批三台仪器，保留公开记录。';
  $('observations').replaceChildren();
  const metrics=visibleMetrics(frame);
  if (!metrics.length) $('observations').append(element('p','截至本步没有已观测的数值；不以零补填。'));
  for (const [key,value] of metrics) {
    const metric=element('div',METRICS[key]??key,'metric');
    metric.append(element('strong',value.toPrecision(5)));$('observations').append(metric);
  }
  $('public-report').textContent=frame.report_text??'没有保存公开报告。';
  $('previous').disabled=state.step===0;
  $('next').disabled=state.step===state.demo.frames.length-1;
}

async function main() {
  const catalog=await json('/api/catalog');
  catalog.instruments.forEach((item,index)=>{
    const button=element('button',null,'instrument');button.dataset.slug=item.slug;
    button.append(element('span',`0${index+1}`,'number'),element('strong',item.title),element('small',item.subtitle));
    button.addEventListener('click',()=>selectInstrument(item.slug));$('instruments').append(button);
  });
  initializeRenderer();
  $('fit').onclick=fitView;
  $('wire').onclick=()=>{state.wire=!state.wire;$('wire').setAttribute('aria-pressed',String(state.wire));applyMaterials();};
  $('rotate').onclick=()=>{orbit.autoRotate=!orbit.autoRotate;$('rotate').setAttribute('aria-pressed',String(orbit.autoRotate));};
  $('component').onchange=()=>selectComponent($('component').value||null);
  $('reset-joints').onclick=()=>{for(const entry of joints.values()){entry.input.value='0';entry.update();}selectComponent(null);};
  $('record-toggle').onclick=async()=>{
    try {
      state.demo??=await json('/api/demo');
      state.records=!state.records;
      $('record-body').hidden=!state.records;
      $('record-toggle').textContent=state.records?'收起公开记录':'查看公开记录';
      $('record-toggle').setAttribute('aria-expanded',String(state.records));
      $('timeline').max=String(state.demo.frames.length-1);
      if(state.records) renderRecord();
    } catch(error) {$('record-toggle').textContent=`读取失败：${error.message}`;}
  };
  $('timeline').oninput=()=>{state.step=Number($('timeline').value);renderRecord();};
  $('previous').onclick=()=>{state.step=Math.max(0,state.step-1);renderRecord();};
  $('next').onclick=()=>{state.step=Math.min(state.demo.frames.length-1,state.step+1);renderRecord();};
  const requested=location.hash.slice(1);
  await selectInstrument(catalog.instruments.some(item=>item.slug===requested)?requested:catalog.instruments[0].slug);
}

main().catch(error=>{$('loading').hidden=false;$('loading').textContent=`预览暂不可用：${error.message}`;console.error(error);});
