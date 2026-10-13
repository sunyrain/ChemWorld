import assert from "node:assert/strict";
import test from "node:test";
import { explorationGraph, actionLines, graphLayout, eventSummary } from "./charts.js";

test("action graph preserves rejections and distinguishes chronology from material routing", () => {
  const events = [
    { event_id: "a", action: { operation: "heat" }, transaction_status: "committed" },
    { event_id: "b", action: { operation: "measure" }, transaction_status: "rejected" },
    { event_id: "c", action: { operation: "sample" }, transaction_status: "committed" },
  ];
  const graph = explorationGraph({ events, status: "running" });
  assert.equal(graph.nodes.length, 3);
  assert.equal(graph.nodes[1].state, "rejected");
  assert.match(graph.legend, /提交顺序/);
  assert.equal(graph.nodes[2].status, "已执行");
  assert(!graph.nodes.some((n) => n.status === "执行中"));
  assert.deepEqual(graph.edges, [{ source: "a", target: "b" }, { source: "b", target: "c" }]);
});

test("component network uses only published vessels and connections", () => {
  const graph = explorationGraph({
    view: { component_network: {
      active_vessel: "reactor",
      vessels: [{ id: "reactor", capacity_L: 2 }, { id: "collector", capacity_L: 1 }, { id: "isolated", capacity_L: 1 }],
      connections: [
        { source_vessel: "reactor", target_vessel: "collector" },
        { source_vessel: "reactor", target_vessel: "private-or-missing" },
      ],
    } },
  }, "network");
  assert.equal(graph.nodes.length, 3);
  assert.deepEqual(graph.edges, [{ source: "reactor", target: "collector" }]);
  assert.equal(graph.nodes[0].state, "active");
  assert.equal(graph.nodes[2].state, "neutral");
  assert.match(graph.legend, /不代表本次已转移/);
});

test("graph retains every event and original indexes; no records means no invented network", () => {
  const events = Array.from({ length: 20 }, (_, i) => ({
    event_id: String(i), action: { operation: "wait" }, transaction_status: "committed",
  }));
  const graph = explorationGraph({ events });
  assert.equal(graph.total, 20);
  assert.equal(graph.nodes.length, 20);
  assert.equal(graph.nodes[0].eventIndex, 0);
  assert.equal(graph.nodes.at(-1).eventIndex, 19);
  assert.deepEqual(explorationGraph({ events: [], view: {} }, "network").nodes, []);
});

test("campaign batch filter keeps global event indices and never links separate batches", () => {
  const events=Array.from({length:8},(_,i)=>({event_id:String(i),batch:i<3?1:2,action:{operation:'wait'},transaction_status:'committed'}));
  const graph=explorationGraph({events},'events',{},2);
  assert.deepEqual(graph.nodes.map(n=>n.eventIndex),[3,4,5,6,7]);
  assert.equal(graph.total,5);
  assert.equal(graph.edges.length,4);
  assert.deepEqual(graph.edges[0],{source:'3',target:'4'});
});

test("default layout has room for every node; saved positions are copied", () => {
  const graph={nodes:Array.from({length:39},(_,i)=>({id:String(i)}))};
  const points=[...graphLayout(graph).values()];
  for(let i=0;i<points.length;i++) for(let j=i+1;j<points.length;j++) {
    assert(Math.abs(points[i].x-points[j].x)>=208 || Math.abs(points[i].y-points[j].y)>=134);
  }
  const saved={'0':{x:-200,y:310},'1':{x:NaN,y:10}};
  const restored=graphLayout(graph,saved);
  assert.deepEqual(restored.get('0'),saved['0']);
  restored.get('0').x=99;
  assert.equal(saved['0'].x,-200);
  assert(Number.isFinite(restored.get('1').x));
});

test("event summary shows only committed measurements and retains zero without inventing missing results", () => {
  const event={transaction_status:'committed',action:{operation:'measure',instrument:'final_assay'},observation:{yield:0,purity:null,conversion:.7,selectivity:.9},observed_mask:{selectivity:false}};
  assert.deepEqual(eventSummary(event).metrics.map(m=>[m.key,m.value]),[['yield',0],['conversion',.7]]);
  assert.equal(eventSummary({...event,transaction_status:'rejected'}).metrics.length,0);
  assert.equal(eventSummary({...event,action:{operation:'wait'}}).metrics.length,0);
});

test("failures are concise and distinguish rejection from rollback without inferring overheating", () => {
  const rejected=eventSummary({transaction_status:'rejected',action:{operation:'seed_crystals'},validation:{invalid_reasons:['seed_crystals_requires_current_reaction_assay']}});
  assert.equal(rejected.status,'未执行');
  assert.match(rejected.summary,/测定/);
  const rollback=eventSummary({transaction_status:'rolled_back',action:{operation:'run_flow'},validation:{invalid_reasons:['constitution_failed']}});
  assert.equal(rollback.status,'已回滚');
  assert.match(rollback.summary,/未产生新的有效实验结果/);
  assert.doesNotMatch(rollback.summary,/过热|温度越界/);
});

test("apparatus labels convert public units but keep rejected missing fields explicit", () => {
  assert.deepEqual(actionLines({ operation: "heat", target_temperature_K: 353.15, duration_s: 480 }), ["80 °C", "8 min"]);
  assert.deepEqual(actionLines({ operation: "add_solvent", volume_L: 0.025, solvent: 2 }), ["25 mL", "溶剂 2"]);
  assert.deepEqual(actionLines({ operation: "heat" }), ["温度未提供", "时长未提供"]);
});
