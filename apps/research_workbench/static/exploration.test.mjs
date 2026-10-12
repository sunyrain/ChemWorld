import assert from "node:assert/strict";
import test from "node:test";
import { explorationGraph } from "./charts.js";

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
  assert.equal(graph.nodes[2].status, "已提交");
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

test("bounded graph retains original event indexes; no records means no invented network", () => {
  const events = Array.from({ length: 20 }, (_, i) => ({
    event_id: String(i), action: { operation: "wait" }, transaction_status: "committed",
  }));
  const graph = explorationGraph({ events });
  assert.equal(graph.total, 20);
  assert.equal(graph.nodes.length, 12);
  assert.equal(graph.nodes[0].eventIndex, 8);
  assert.equal(graph.nodes.at(-1).eventIndex, 19);
  assert.deepEqual(explorationGraph({ events: [], view: {} }, "network").nodes, []);
});
