import assert from 'node:assert/strict';
import test from 'node:test';
import {campaignModel, recipeChanges, noteChanges, campaignPlot} from './charts.js';

const event = (batch, action, observation = {}, status = 'committed') => ({batch,action,observation,transaction_status:status});
const assay = (batch, value, status) => event(batch,{operation:'measure',instrument:'final_assay'},{crystal_yield:value},status);
const revision = (revision, cursor) => ({revision,public_cursor:{event_count:cursor}});

test('campaign outcomes use only committed final measurements and preserve zero, masks and absent batches',()=>{
  const model=campaignModel({batch_count:4,design:{task_id:'reaction-to-crystallization'},events:[
    assay(1,0), event(2,{operation:'wait'},{crystal_yield:.9}), assay(2,.9,'rolled_back'),
    {...assay(3,.8),observed_mask:{crystal_yield:false}},
  ]});
  assert.equal(model.batches.length,4);
  assert.deepEqual(model.batches.map(b=>b.values.crystal_yield),[0,null,null,null]);
  assert.equal(model.batches[1].failures.length,1);
  assert.equal(model.batches[1].assay,undefined);
  assert.equal(model.batches[3].events.length,0);
});

test('notebook boundaries retain pre-experiment, in-batch, after-batch and unplaced versions without future leakage',()=>{
  const model=campaignModel({batch_count:3,events:[
    event(1,{operation:'heat'}),assay(1,.4),event(2,{operation:'heat'}),assay(2,.5),assay(3,.6),
  ],model_notebook:{revisions:[revision(6,99),revision(5,5),revision(4,3),revision(3,2),revision(2,1),revision(1,0)]}});
  assert.deepEqual(model.initial.map(v=>v.revision),[1]);
  assert.deepEqual(model.batches.map(b=>b.revisions.map(v=>v.revision)),[[2,3],[4],[5]]);
  assert.deepEqual(model.batches.map(b=>b.beforeRevision.revision),[1,3,4]);
  assert.deepEqual(model.unplaced.map(v=>v.revision),[6]);
  assert.equal(model.batches[1].startCursor,3);
});

test('recipe comparison excludes rejected requests and measurement-only differences',()=>{
  const model=campaignModel({batch_count:2,events:[
    event(1,{operation:'heat',duration_s:100}),event(1,{operation:'measure',instrument:'particle_size'}),assay(1,.4),
    event(2,{operation:'heat',duration_s:100}),event(2,{operation:'seed_crystals',seed_mass_g:1},{},'rejected'),assay(2,.5),
  ]});
  assert.deepEqual(recipeChanges(model.batches[0].recipe,model.batches[1].recipe),{changes:[],reordered:false});
});

test('recipe changes retain repeated operations, added/removed fields and changed order',()=>{
  const a=[{operation:'heat',duration_s:10},{operation:'wait',duration_s:20},{operation:'heat',duration_s:30}];
  const b=[{operation:'wait',duration_s:20},{operation:'heat',duration_s:10},{operation:'heat',duration_s:40,stirring_speed_rpm:500}];
  const changes=recipeChanges(a,b);
  assert.equal(changes.reordered,true);
  assert.equal(changes.changes.length,1);
  assert.deepEqual(changes.changes[0].fields,['duration_s','stirring_speed_rpm']);
  assert.equal(changes.changes[0].before.duration_s,30);
});

test('notebook text diff preserves exact added/deleted paragraphs, including a withdrawn expectation',()=>{
  const diff=noteChanges('# Hypothesis\r\n\r\nMore seed will help.\r\n\r\nKeep solvent fixed.','# Hypothesis\n\nMore seed did not help.\n\nKeep solvent fixed.');
  assert.deepEqual(diff.added,['More seed did not help.']);
  assert.deepEqual(diff.removed,['More seed will help.']);
  assert.deepEqual(diff.unchanged,['# Hypothesis','Keep solvent fixed.']);
  assert.deepEqual(noteChanges('Still uncertain.','Still uncertain.').added,[]);
  assert.deepEqual(noteChanges('Withdraw this.','').removed,['Withdraw this.']);
});

test('trend breaks at missing outcomes and exposes each observed batch as a labelled keyboard target',()=>{
  const model=campaignModel({batch_count:4,design:{task_id:'reaction-to-crystallization'},events:[assay(1,0),assay(3,.5),assay(4,.7)]});
  const svg=campaignPlot(model.batches,model.metrics[0]);
  const path=svg.match(/<path d="([^"]+)"/)[1];
  assert.equal((path.match(/M/g)||[]).length,2);
  assert.equal((svg.match(/tabindex="0"/g)||[]).length,3);
  assert.match(svg,/第 1 批，晶体回收 0%/);
  assert.doesNotMatch(svg,/data-campaign-jump="2"/);
});

test('equilibrium and electrochemistry use distinct units and do not borrow crystallization channels',()=>{
  assert.deepEqual(campaignModel({design:{task_id:'equilibrium-characterization'}}).metrics.map(m=>[m.key,m.scale]),[
    ['pH_normalized',1],['acid_dissociation_fraction',100],['precipitation_signal',1],
  ]);
  assert.equal(campaignModel({design:{task_id:'electrochemical-conversion'}}).metrics[0].key,'score');
});
