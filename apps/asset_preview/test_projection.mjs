import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import test from 'node:test';
import {frameAsset,visibleMetrics} from './static/projection.mjs';

const demo=JSON.parse(await readFile(new URL('../blender_lab/static/demo.json',import.meta.url),'utf8'));

test('existing public frames map only supported display categories',()=>{
  assert.equal(frameAsset(demo.frames[4]),'ika_plate_rctdigital');
  assert.equal(frameAsset(demo.frames[6]),'hach_dr6000');
  assert.equal(frameAsset(demo.frames[8]),null); // final assay must not masquerade as a UV measurement
  assert.equal(frameAsset({...demo.frames[6],status:'rollback'}),null);
  assert.equal(frameAsset({...demo.frames[6],status:'rejected'}),null);
});

test('seeking backward cannot expose later measurements or fabricate zeros',()=>{
  assert.deepEqual(visibleMetrics(demo.frames[0]),[]);
  const measured=visibleMetrics(demo.frames[6]);
  assert.ok(measured.length>0);
  assert.deepEqual(visibleMetrics(demo.frames[0]),[]);
  for (const [key,value] of measured) {
    assert.equal(demo.frames[6].observed_mask[key],true);
    assert.equal(value,demo.frames[6].observations[key]);
  }
});

test('unobserved, absent and nonfinite fields are not presented as instrument readouts',()=>{
  assert.deepEqual(visibleMetrics({observations:{a:4,b:0,c:null,d:Infinity,e:12},observed_mask:{a:false,b:true,c:true,d:true}}),[['b',0]]);
});
