"use strict";

/**
 * Deterministic browser-only demonstration of the legacy threshold audit rules.
 * This is NOT a quantum circuit, a cryptographic audit or a server evaluation.
 */
function evaluateTask(input) {
  if (typeof input !== "object" || input === null) {
    throw new TypeError("A task payload is required.");
  }
  const taskId = String(input.task_id ?? "").trim();
  const targetId = String(input.target_identifier ?? "").trim();
  const descriptor = String(input.status_descriptor ?? "").trim();
  const primary = Number(input.primary_metric);
  const secondary = Number(input.secondary_metric);
  if (!taskId || !targetId || taskId.length > 128 || targetId.length > 128) {
    throw new Error("Task ID and target ID are required (maximum 128 characters).");
  }
  if (descriptor.length > 256) throw new Error("Status descriptor is too long.");
  if (input.primary_metric === "" || input.secondary_metric === "" ||
      !Number.isFinite(primary) || !Number.isFinite(secondary)) {
    throw new Error("Both metrics must be finite numbers.");
  }
  if (typeof input.is_critical_flag !== "boolean") {
    throw new Error("The critical flag must be a boolean.");
  }

  const alerts = [];
  function add(worker, urgency, summary, details) {
    alerts.push({origin_worker: worker, urgency, summary, technical_details: details});
  }
  if (primary > 25) {
    add("InvariantQCWorker", "ELEVATED_RISK", "Primary Metric Threshold Exceeded",
        "Primary measurement " + primary.toFixed(2) + " exceeds reference limit 25.00.");
  }
  if (input.is_critical_flag || secondary > 12) {
    add("SafetyEscalationWorker", input.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
        "Safety Interlock Triggered",
        "CriticalFlag=" + input.is_critical_flag + "; secondary index " + secondary.toFixed(2) + ".");
  }
  if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"]
      .some(term => descriptor.toUpperCase().includes(term))) {
    add("ProtocolConformanceWorker", "ELEVATED_RISK", "Protocol Conformance Discordance Detected",
        "Status descriptor matches a configured anomaly keyword.");
  }
  const critical = alerts.filter(a => a.urgency === "CRITICAL_STAT_PANIC").length;
  const urgency = critical ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
  return {
    evaluation_mode: "LOCAL_RULE_BASED_DEMO",
    signed: false,
    task_id: taskId,
    target_identifier: targetId,
    overall_urgency: urgency,
    integrity_status: critical ? "RECALIBRATION_REQUIRED" :
      alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
    total_alerts: alerts.length,
    critical_alerts_count: critical,
    alerts,
    notice: "This is an unsigned local rule evaluation, not quantum computation, clinical decision support, or a cryptographic audit."
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {evaluateTask};
}

if (typeof document !== "undefined") {
  const form = document.getElementById("audit-form");
  const output = document.getElementById("output");
  const status = document.getElementById("status");
  const count = document.getElementById("count");
  const download = document.getElementById("download");
  let latest = null;
  let completed = 0;

  form.addEventListener("submit", event => {
    event.preventDefault();
    try {
      const result = evaluateTask({
        task_id: document.getElementById("task_id").value,
        target_identifier: document.getElementById("target_id").value,
        primary_metric: document.getElementById("primary").value,
        secondary_metric: document.getElementById("secondary").value,
        status_descriptor: document.getElementById("descriptor").value,
        is_critical_flag: document.getElementById("critical").checked
      });
      latest = result;
      completed += 1;
      count.textContent = String(completed);
      status.textContent = result.overall_urgency;
      output.textContent = JSON.stringify(result, null, 2);
      download.disabled = false;
    } catch (error) {
      latest = null;
      status.textContent = "INPUT ERROR";
      output.textContent = String(error.message || error);
      download.disabled = true;
    }
  });

  download.addEventListener("click", () => {
    if (!latest) return;
    const blob = new Blob([JSON.stringify(latest, null, 2) + "\n"], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "qnn-rule-evaluation.json";
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  });
}
