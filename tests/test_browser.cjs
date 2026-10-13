"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const {evaluateTask} = require("../web/audit.js");

const base = () => ({
  task_id: "TASK-01", target_identifier: "TARGET-01",
  primary_metric: 25, secondary_metric: 12,
  status_descriptor: "NOMINAL", is_critical_flag: false
});
test("boundary values are nominal", () => {
  const d = evaluateTask(base());
  assert.equal(d.overall_urgency, "ROUTINE");
  assert.equal(d.total_alerts, 0);
  assert.equal(d.signed, false);
});
test("elevated threshold and descriptor match", () => {
  const d = evaluateTask({...base(), primary_metric: 25.1, secondary_metric: 12.1, status_descriptor: "violation"});
  assert.equal(d.overall_urgency, "ELEVATED_RISK");
  assert.equal(d.total_alerts, 3);
  assert.equal(d.critical_alerts_count, 0);
});
test("critical flag overrides elevation", () => {
  const d = evaluateTask({...base(), is_critical_flag: true});
  assert.equal(d.overall_urgency, "CRITICAL_STAT_PANIC");
  assert.equal(d.total_alerts, 1);
  assert.equal(d.integrity_status, "RECALIBRATION_REQUIRED");
});
test("bad input is rejected", () => {
  assert.throws(() => evaluateTask({...base(), primary_metric: "NaN"}), /finite/);
  assert.throws(() => evaluateTask({...base(), secondary_metric: "Infinity"}), /finite/);
  assert.throws(() => evaluateTask({...base(), task_id: ""}), /required/);
  assert.throws(() => evaluateTask({...base(), is_critical_flag: "false"}), /boolean/);
});
