import assert from "node:assert/strict";
import test from "node:test";
import { extent, drawChart } from "./charts.js";

test("zero signal has nonzero axis range; missing is not zero", () => {
  assert.deepEqual(
    extent(
      [
        [0, 0],
        [1, 0],
      ],
      1,
    ),
    [-0.5, 0.5],
  );
  assert.deepEqual(
    extent(
      [
        [0, NaN],
        [1, Infinity],
      ],
      1,
    ),
    [0, 1],
  );
  assert.deepEqual(
    extent(
      [
        [1, 2],
        [9, 7],
      ],
      0,
    ),
    [1, 9],
  );
});
test("plot retains negative samples, units, reverse axis and accessible label", () => {
  const nodes = [];
  globalThis.document = {
    createElementNS: (ns, tag) => {
      const node = {
        tag,
        attrs: {},
        children: [],
        setAttribute(k, v) {
          this.attrs[k] = v;
        },
        append(...args) {
          this.children.push(...args);
        },
        addEventListener() {},
      };
      nodes.push(node);
      return node;
    },
  };
  const container = {
    replaceChildren(...nodes) {
      this.children = nodes;
    },
  };
  drawChart(container, {
    label: "NMR",
    points: [
      [0, -2],
      [1, 3],
      [2, 0],
    ],
    x_label: "shift",
    x_unit: "ppm",
    y_label: "signal",
    y_unit: "a.u.",
    reverse_x: true,
  });
  assert.match(container.children[0].attrs["aria-label"], /ppm/);
  const path = nodes.find((n) => n.tag === "path").attrs.d;
  assert.match(path, /^M618\.00,/);
  assert.equal((path.match(/L/g) || []).length, 2);
  delete globalThis.document;
});
