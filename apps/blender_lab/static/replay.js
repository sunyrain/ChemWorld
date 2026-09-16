// Pure, seekable presentation state. No network calls or Core execution.
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
const smooth = (t) => t * t * (3 - 2 * t);
const turn = (a, b, t) => a + ((((b - a) % 360) + 540) % 360 - 180) * t;

export class ReplayClock {
  constructor(duration) {
    this.duration = duration;
    this.time = 0;
    this.rate = 1;
    this.playing = false;
    this.last = null;
  }
  tick(now) {
    if (this.playing && this.last !== null) {
      this.time = clamp(this.time + Math.max(0, now - this.last) * this.rate / 1000, 0, this.duration);
      if (this.time >= this.duration) this.playing = false;
    }
    this.last = now;
    return this.time;
  }
  play(now) {
    if (this.time >= this.duration) this.time = 0;
    this.last = now;
    this.playing = true;
  }
  pause(now) {
    this.tick(now);
    this.playing = false;
  }
  seek(time, now) {
    this.time = clamp(Number.isFinite(time) ? time : 0, 0, this.duration);
    this.last = now;
    if (this.time === this.duration) this.playing = false;
  }
  setRate(rate, now) {
    this.tick(now);
    this.rate = clamp(Number.isFinite(rate) ? rate : 1, 0.25, 4);
  }
}

export function sampleMotion(motion, requestedTime) {
  const time = clamp(requestedTime, 0, motion.duration);
  const segment = motion.segments.find((s) => time < s.end) || motion.segments.at(-1);
  const fraction = clamp((time - segment.start) / (segment.end - segment.start), 0, 1);
  const t = smooth(fraction), a = segment.from, b = segment.to;
  // Discrete grasp/custody changes occur at the END of their segment. Rewinding
  // evaluates these snapshots afresh, so no event replay or undo is necessary.
  const discrete = fraction >= 1 ? b : a;
  const position = mix(a.position, b.position, t);
  const yaw = turn(a.yaw, b.yaw, t);
  const extension = a.extension + (b.extension - a.extension) * t;
  const target = mix(a.target, b.target, t);
  const radians = yaw * Math.PI / 180;
  const home = [position[0] - 0.16 * Math.sin(radians), position[1] + 0.16 * Math.cos(radians), position[2] + 0.86];
  const tcp = mix(home, target, extension);
  const samplePosition = discrete.holder === "robot_01"
    ? [tcp[0], tcp[1], tcp[2] - 0.17]
    : [...discrete.samplePosition];
  const frameIndex = motion.stepEnds.reduce((last, end, index) => time >= end ? index : last, 0);
  return {
    time, step: segment.step, frameIndex,
    label: segment.label, asset: segment.asset, effect: segment.effect,
    complete: time >= motion.duration,
    holder: discrete.holder,
    sampleVisible: discrete.sampleVisible,
    poses: { robot_01: position, sample_tube_01: samplePosition },
    robot: {
      base_yaw_deg: yaw,
      arm_extension: extension,
      arm_target_m: target,
      gripper_open: discrete.gripperOpen,
      held_asset_id: discrete.holder === "robot_01" ? "sample_tube_01" : "",
    },
  };
}
