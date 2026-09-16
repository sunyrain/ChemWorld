import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { ReplayClock, sampleMotion } from "./static/replay.js";

const motion = JSON.parse(readFileSync(new URL("./static/replay-motion.json", import.meta.url), "utf8"));
const distance = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));

test("pause/resume excludes paused wall time and seek discards the previous clock anchor", () => {
  const clock = new ReplayClock(60);
  clock.play(1000);
  assert.equal(clock.tick(4000), 3);
  clock.pause(5000);
  assert.equal(clock.tick(65000), 4);
  clock.play(65000);
  assert.equal(clock.tick(66000), 5);
  clock.seek(20, 67000);
  assert.equal(clock.tick(68000), 21);
});

test("speed changes account for elapsed time at the old speed; end and restart are exact", () => {
  const clock = new ReplayClock(10);
  clock.play(0);
  clock.setRate(2, 1000);
  assert.equal(clock.tick(2000), 3);
  assert.equal(clock.tick(20000), 10);
  assert.equal(clock.playing, false);
  clock.play(21000);
  assert.equal(clock.time, 0);
  clock.seek(-10, 21000);
  assert.equal(clock.time, 0);
});

test("public observations only advance after their operation finishes", () => {
  for (let step = 1; step < motion.stepEnds.length; step++) {
    assert.equal(sampleMotion(motion, motion.stepStarts[step]).frameIndex, step - 1);
    assert.equal(sampleMotion(motion, motion.stepEnds[step] - 1e-5).frameIndex, step - 1);
    assert.equal(sampleMotion(motion, motion.stepEnds[step]).frameIndex, step);
  }
  assert.equal(sampleMotion(motion, motion.duration).complete, true);
});

test("rewinding restores sample visibility, grip and custody without mutating the record", () => {
  const original = JSON.stringify(motion);
  const pick = motion.segments.find((s) => s.to.holder === "robot_01");
  const place = motion.segments.find((s) => s.to.holder === "analysis");
  const initial = sampleMotion(motion, 0);
  const held = sampleMotion(motion, pick.end + 0.3);
  assert.equal(initial.sampleVisible, false);
  assert.equal(held.holder, "robot_01");
  assert.equal(held.robot.gripper_open, false);
  assert.equal(sampleMotion(motion, place.end).holder, "analysis");
  assert.deepEqual(sampleMotion(motion, pick.end + 0.3), held);
  assert.deepEqual(sampleMotion(motion, 0), initial);
  assert.equal(JSON.stringify(motion), original);
});

test("cart and visible sample stay continuous across every segment including grasp and release", () => {
  for (const segment of motion.segments.slice(0, -1)) {
    const left = sampleMotion(motion, segment.end - 1e-6);
    const right = sampleMotion(motion, segment.end + 1e-6);
    assert.ok(distance(left.poses.robot_01, right.poses.robot_01) < 1e-4, segment.label);
    if (left.sampleVisible && right.sampleVisible) {
      assert.ok(distance(left.poses.sample_tube_01, right.poses.sample_tube_01) < 1e-4, segment.label);
    }
  }
});

test("the carried sample tracks the tool centre; final state parks without removing the sample", () => {
  for (let time = 0; time <= motion.duration; time += 0.05) {
    const p = sampleMotion(motion, time);
    assert.ok(Object.values(p.poses).flat().every(Number.isFinite));
    if (p.holder === "robot_01" && p.robot.arm_extension === 0) {
      assert.ok(Math.abs(p.poses.sample_tube_01[2] - p.poses.robot_01[2] - 0.69) < 1e-9);
    }
  }
  const end = sampleMotion(motion, motion.duration);
  assert.deepEqual(end.poses.robot_01, motion.stations.home.dock_m);
  assert.deepEqual(end.poses.sample_tube_01, motion.stations.analysis.sample_position_m);
  assert.equal(end.robot.arm_extension, 0);
  assert.equal(end.robot.gripper_open, true);
  assert.equal(end.sampleVisible, true);
});
