import test from "node:test";
import assert from "node:assert/strict";
import {
  parseLocal,
  observations,
  snapshot,
  metricSeries,
  datasets,
  numericMetrics,
  csv,
  experiments,
  stepIO,
  changedConditions,
  classify,
} from "./static/replay.mjs";

test("import classification uses recorded task IDs and preserves multiple categories", () => {
  const categories = [
    { id: "crystallization", tasks: ["reaction-to-crystallization"] },
    { id: "distillation", tasks: ["reaction-to-distillation"] },
  ];
  assert.deepEqual(
    classify(
      [
        { task_id: "reaction-to-crystallization" },
        { task_id: "reaction-to-distillation" },
      ],
      categories,
    ),
    ["crystallization", "distillation"],
  );
  assert.deepEqual(classify({ name: "crystal-v99" }, categories), ["other"]);
});

test("step IO never borrows a future trace or previous experiment context", () => {
  const records = [
    {
      step: 1,
      campaign_id: "same",
      experiment_index: 0,
      action: { operation: "heat" },
      observation: { purity: 0.9 },
    },
    {
      step: 2,
      campaign_id: "same",
      experiment_index: 1,
      action: { operation: "heat" },
      agent_trace: [
        {
          expected_step: 3,
          action: { operation: "heat" },
          prompt: "future prompt",
          decision_audit: { expected_effect: "future explanation" },
        },
      ],
    },
  ];
  const io = stepIO(records, 1);
  assert.equal(io.input, null);
  assert.equal(io.audit, null);
  assert.equal(io.trace, null);
});

test("campaign splits by lifecycle and committed assay, never by terminate alone", () => {
  const rows = [
    {
      step: 1,
      campaign_id: "a",
      experiment_index: 5,
      action: { operation: "heat" },
      transaction_status: "committed",
    },
    {
      step: 2,
      campaign_id: "a",
      experiment_index: 5,
      action: { operation: "terminate" },
      transaction_status: "committed",
    },
    {
      step: 3,
      campaign_id: "a",
      experiment_index: 5,
      action: { operation: "measure", instrument: "final_assay" },
      transaction_status: "validation_failed",
    },
    {
      step: 4,
      campaign_id: "a",
      experiment_index: 5,
      action: { operation: "measure", instrument: "final_assay" },
      transaction_status: "committed",
      observation: { score: 0.7 },
    },
    {
      step: 5,
      campaign_id: "a",
      experiment_index: 6,
      action: { operation: "heat" },
      transaction_status: "committed",
    },
  ];
  const groups = experiments(rows);
  assert.equal(groups.length, 2);
  assert.equal(groups[0].steps, 4);
  assert.equal(groups[0].failed, 1);
  assert.equal(groups[0].identity, 5);
  assert.equal(groups[0].ordinal, 1);
  assert.equal(groups[0].status, "assayed");
  assert.equal(groups[1].status, "prefix");
  assert.equal(groups[1].metrics.score, undefined);
});
test("single-experiment trajectories stay single and campaign resets stay distinct", () => {
  assert.equal(experiments(records).length, 1);
  assert.equal(
    experiments([
      { ...records[0], campaign_id: "first", experiment_index: 0 },
      { ...records[1], campaign_id: "second", experiment_index: 0 },
    ]).length,
    2,
  );
});
test("per-step IO uses pre-action context and the matching current trace", () => {
  const audit = {
    status: "provided",
    diagnostic_target: "Test temperature",
    expected_effect: "Higher conversion",
  };
  const rows = [...records];
  rows[1] = {
    ...rows[1],
    explanation: {
      decision_context: { step: 2, visible_metrics: { purity: 0.1 } },
      decision_audit: audit,
    },
    agent_trace: [
      { expected_step: 1, action: records[0].action },
      {
        expected_step: 2,
        action: records[1].action,
        decision_audit: audit,
        outcome: { observation: { purity: 0.6 } },
      },
    ],
  };
  const io = stepIO(rows, 1);
  assert.equal(io.input.visible_metrics.purity, 0.1);
  assert.equal(io.tool.observation.purity, 0.6);
  assert.equal(io.trace.expected_step, 2);
  assert.equal(io.exactPrompt, false);
  assert.equal(io.audit.diagnostic_target, "Test temperature");
});
test("missing explanations are not synthesized from action or post-action observation", () => {
  const row = {
    ...records[0],
    explanation: {
      decision_audit: {
        status: "not_provided",
        expected_effect: "not provided",
      },
    },
    agent_metadata: { requires_online_model: false },
  };
  const io = stepIO([row], 0);
  assert.equal(io.input, null);
  assert.equal(io.inputKind, "missing");
  assert.equal(io.audit, null);
  assert.equal(io.output, null);
  assert.equal(io.scripted, true);
});
test("saved request messages and provider output are displayed without reconstruction", () => {
  const row = {
    ...records[0],
    agent_trace: [
      {
        expected_step: 1,
        messages: [{ role: "user", content: "Original input" }],
        response: { content: "Original output" },
        action: records[0].action,
      },
    ],
  };
  const io = stepIO([row], 0);
  assert.equal(io.exactPrompt, true);
  assert.equal(io.inputKind, "recorded_request");
  assert.equal(io.input[0].content, "Original input");
  assert.equal(io.output.content, "Original output");
});
test("condition comparison preserves heating order and removed parameters", () => {
  const rows = [
    { action: { operation: "heat", target_temperature_K: 300 } },
    { action: { operation: "heat", target_temperature_K: 350 } },
    { action: { operation: "heat", target_temperature_K: 350 } },
    { action: { operation: "heat", target_temperature_K: 300 } },
  ];
  const differences = changedConditions(
    rows,
    { indices: [2, 3] },
    { indices: [0, 1] },
  );
  assert.deepEqual(differences[0].previous, [300, 350]);
  assert.deepEqual(differences[0].value, [350, 300]);
});

const records = [
  {
    step: 1,
    action: { operation: "add_reagent" },
    observation: { purity: 0.8, cost: 0.1 },
    observed_mask: { purity: false, cost: true },
    transaction_status: "committed",
  },
  {
    step: 2,
    action: { operation: "measure", instrument: "hplc" },
    observation: { purity: 0.6, cost: 0.2 },
    observed_mask: { purity: true, cost: true },
    transaction_status: "committed",
  },
  {
    step: 3,
    action: { operation: "heat" },
    observation: { purity: 0.6, cost: 0.2 },
    transaction_status: "validation_failed",
    rollback_reason: "temperature limit",
  },
];

test("JSONL errors retain the contiguous prefix and line number", () => {
  const result = parseLocal(
    "\uFEFF" +
      JSON.stringify(records[0]) +
      "\n{bad\n" +
      JSON.stringify(records[2]),
    "trial.jsonl",
  );
  assert.equal(result.records.length, 1);
  assert.equal(result.errors[0].line, 2);
  assert.throws(() => parseLocal("", "empty.jsonl"), /没有可回放/);
});
test("JSON arrays, wrapped trajectories and report files remain distinct", () => {
  assert.equal(
    parseLocal(JSON.stringify(records), "record.json").kind,
    "trajectory",
  );
  assert.equal(
    parseLocal(JSON.stringify({ records }), "record.json").records.length,
    3,
  );
  assert.equal(
    parseLocal('{"counts":{"failed":2}}', "summary.json").kind,
    "report",
  );
});
test("unknown observations and future records never turn into zero or a visible point", () => {
  assert.deepEqual(observations(records[0]), { purity: null, cost: 0.1 });
  assert.deepEqual(
    metricSeries(records, "purity", 1).map((x) => x.value),
    [null, 0.6, null],
  );
  assert.equal(observations({ observation: { purity: NaN } }).purity, null);
});
test("random seeking restores exact snapshots including failed actions", () => {
  const before = JSON.stringify(records);
  assert.equal(snapshot(records, 2).status, "validation_failed");
  assert.equal(snapshot(records, 0).observations.purity, null);
  assert.equal(snapshot(records, 1).action.instrument, "hplc");
  assert.equal(snapshot(records, 900).index, 2);
  assert.equal(JSON.stringify(records), before);
});
test("resource accounting keeps physical cost distinct from observation cost", () => {
  const r = {
    ...records[0],
    agent_view: {
      tool_json: { operational_state: { temperature_K: 300 } },
      lab_report: {
        campaign_state: {
          campaign_resources: {
            state: {
              report_only: { physical_cost: 1.25 },
              remaining: { final_assays: 1 },
            },
          },
        },
      },
    },
  };
  const s = snapshot([r], 0);
  assert.equal(s.resources.physical_cost, 1.25);
  assert.equal(s.observations.cost, 0.1);
  assert.equal(s.remaining.final_assays, 1);
  assert.equal(s.operational.temperature_K, 300);
});
test("report tables preserve failed rows, exact denominators and nulls", () => {
  const report = {
    counts: { planned: 3, failed: 1, not_started: 1 },
    cells: [
      { cell: "a", quality_passed: false, purity: null },
      { cell: "b", purity: 0.8 },
    ],
  };
  assert.equal(datasets(report)[0].rows.length, 2);
  assert.equal(datasets(report)[0].rows[0].purity, null);
  assert.deepEqual(
    numericMetrics(report).map((m) => m.value),
    [3, 1, 1],
  );
});
test("CSV preserves numeric zero, missing cells and quoted strings", () => {
  const output = csv(
    [
      { name: 'a,"b', value: 0 },
      { name: "missing", value: null },
    ],
    ["name", "value"],
  );
  assert.match(output, /"a,""b","0"/);
  assert.match(output, /"missing",""/);
});
