"""Regression coverage for audit integrity, input boundaries and CSV export."""
import csv

import pytest
from pydantic import ValidationError

from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from cli import main
from simulator import run_simulation


@pytest.mark.parametrize("field", ["actor", "timestamp", "event_type", "payload_hash", "current_hash"])
def test_signature_verification_rejects_field_tampering(field):
    trail = AuditTrail(secret_key="integration-test-only")
    trail.log("operator", "supervisor", "EVALUATE", {"task_id": "T1"})
    trail.log("operator", "supervisor", "EVALUATE", {"task_id": "T2"})
    assert trail.verify_integrity()
    trail.logs[0][field] = "malicious modification"
    assert not trail.verify_integrity()


def test_audit_trail_returns_detached_records():
    trail = AuditTrail(secret_key="integration-test-only")
    trail.log("operator", "supervisor", "EVALUATE", {"task_id": "T1"})
    snapshot = trail.get_trail()
    snapshot[0]["actor"] = "untrusted"
    snapshot.append({"fake": "entry"})
    assert len(trail.get_trail()) == 1
    assert trail.get_trail()[0]["actor"] == "operator"
    assert trail.verify_integrity()


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_metric_rejects_nonfinite(value):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T1", target_identifier="TARGET", primary_metric=value)


def test_guard_inspects_attributes_before_logging():
    supervisor = SystemSupervisor()
    payload = SystemTaskPayload(
        task_id="T1", target_identifier="TARGET", primary_metric=1.0,
        attributes={"contact": "test@example.com"},
    )
    with pytest.raises(SecurityException):
        supervisor.process_task(payload)


def test_csv_export_escapes_formula_cells(tmp_path):
    src = tmp_path / "data.csv"
    dst = tmp_path / "out.csv"
    src.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,status_descriptor,is_critical_flag\n"
        "T1,=1+2,25,12,NOMINAL,false\n"
        "T2,TARGET2,25.1,12.1,NOMINAL,true\n",
        encoding="utf-8",
    )
    assert main(["batch", "-i", str(src), "-o", str(dst)]) == 0
    with dst.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert rows[0]["target_identifier"] == "'=1+2"
    assert rows[0]["overall_urgency"] == "ROUTINE"
    assert rows[1]["overall_urgency"] == "CRITICAL_STAT_PANIC"
    assert rows[1]["total_alerts"] == "2"


def test_simulator_rejects_zero_iterations():
    with pytest.raises(ValueError, match="positive"):
        run_simulation(0)


def test_csv_export_preserves_signed_numeric_columns(tmp_path):
    src = tmp_path / "negative.csv"
    dst = tmp_path / "negative-out.csv"
    src.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,status_descriptor\n"
        "T1,TARGET,-4.5,-12.1,NOMINAL\n", encoding="utf-8"
    )
    assert main(["batch", "-i", str(src), "-o", str(dst)]) == 0
    with dst.open(newline="", encoding="utf-8") as stream:
        row = next(csv.DictReader(stream))
    assert row["primary_metric"] == "-4.5"
    assert row["secondary_metric"] == "-12.1"


def test_qnn_coordinator_rejects_nonfinite_metrics():
    from qnn_pqc_agent.agents import QNNCoordinator
    from qnn_pqc_agent.models import FrontierPayload
    with pytest.raises(ValueError, match="finite"):
        QNNCoordinator().process(
            FrontierPayload("T1", "TARGET", float("nan"), 1, "NOMINAL")
        )


def test_qnn_batch_false_flag_is_not_critical(tmp_path):
    from qnn_pqc_agent.cli import main as qnn_main
    src = tmp_path / "qnn.csv"
    dst = tmp_path / "qnn-out.csv"
    src.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,status_descriptor,is_critical_flag\n"
        "T1,TARGET,1,1,NOMINAL,False\n", encoding="utf-8"
    )
    assert qnn_main(["batch", "-i", str(src), "-o", str(dst)]) == 0
    with dst.open(newline="", encoding="utf-8") as stream:
        row = next(csv.DictReader(stream))
    assert row["overall_status"] == "NOMINAL_OPTIMAL"
    assert row["critical_count"] == "0"
