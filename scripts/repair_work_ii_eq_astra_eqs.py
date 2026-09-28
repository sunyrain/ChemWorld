"""Resume the single user-authorized EQS turn lost to HTTP 503."""

from __future__ import annotations

import copy
import hashlib
import os
import shutil
from types import SimpleNamespace

from run_work_ii_eq_astra_matrix import MODEL, ROOT, emit, read, write

CELL = "EQ-W05--Opaque"
RUN = ROOT / "runs/development/eq-astra-medium-20260927"


def main():
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq
    from scripts.run_work_ii_eq_rx_p_cross_model_v0_1 import provider

    source = RUN / "conditions" / MODEL / "sources" / CELL
    private = source / "private-provider"
    result = read(source / "RESULT.json")
    failed = read(private / "EQS/receipt.json")
    assert result["source_status"] == "completed" and result["exact_replay"]["verified"]
    assert all(result["posttest_validation"][s]["valid"] for s in ("K1", "Q", "K2"))
    assert not result["posttest_validation"]["EQS"]["valid"]
    assert failed["failure"] == "provider_failure" and failed["payload"] is None
    assert "503 Service Unavailable" in (private / "EQS/stdout.jsonl").read_text(encoding="utf-8")
    assert failed["tool_event_count"] == 0 and failed["numerics_attempts"] == 0
    assert (private / "EQS/prompt.txt").read_text(encoding="utf-8") == eq.EQS
    receipts = read(private / "source-receipts.json")
    thread_id = receipts[-1]["thread_id"]
    assert hashlib.sha256(thread_id.encode()).hexdigest() == result["thread_id_sha256"]
    assert failed["thread_id"] == thread_id
    for stage in ("K1", "Q", "K2"):
        assert read(private / stage / "receipt.json")["thread_id"] == thread_id
    intact = [
        source / "trajectory.jsonl",
        source / "public-input-binding.json",
        *(source / "sealed" / f"{s}.json" for s in ("K1", "Q", "K2")),
    ]
    before = {p: p.read_bytes() for p in intact}
    recovery = private / "EQS-recovery-01"
    recovery.mkdir(exist_ok=False)
    shutil.copyfile(source / "RESULT.json", recovery / "original-result.json")
    shutil.copyfile(source / "sealed/EQS.json", recovery / "original-sealed-EQS.json")
    configured = provider({"model": MODEL, "reasoning_effort": "medium"})
    eq.PROVIDER = eq.v1.PROVIDER = eq.shared.PROVIDER = eq.provider_shared.PROVIDER = configured
    config = eq.load_config()
    eq.configure_provider_helpers(config)
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(private / "home/codex-home")
    agent = SimpleNamespace(home_root=private / "home", followup_environment=environment)
    raw = eq.run_posttest(
        agent,
        recovery,
        recovery / "private-provider",
        "EQS",
        thread_id,
        {"stage": CELL, "completed": 0, "total": 1, "repair": "HTTP503_EQS_only"},
        eq.queries(config),
    )
    validation = eq.validate_posttest("EQS", raw.get("payload"), eq.queries(config))
    recovered_receipt = read(recovery / "private-provider/EQS/receipt.json")
    assert all(p.read_bytes() == contents for p, contents in before.items())
    assert recovered_receipt["thread_id"] == thread_id
    if not validation["valid"] or raw.get("failure"):
        emit({"status": "recovery_failed", "validation": validation, "failure": raw.get("failure")})
        raise SystemExit(1)
    effective = copy.deepcopy(result)
    effective["posttests"]["EQS"] = raw
    effective["posttest_validation"]["EQS"] = validation
    effective["posttest_chain_sealed"] = True
    effective["status"] = "completed"
    effective["posttest_recoveries"] = [
        {
            "stage": "EQS",
            "classification": "runtime_transport_loss",
            "failure": "HTTP 503 Service Unavailable before response or tool use",
            "same_thread_verified": True,
            "model": MODEL,
            "reasoning_effort": "medium",
            "original_attempt_preserved": True,
            "recovery_valid": True,
            "recovery_elapsed_s": raw["elapsed_s"],
            "source_K1_Q_K2_unchanged": True,
        }
    ]
    assert effective["posttests"]["Q"] == result["posttests"]["Q"]
    write(source / "sealed/EQS.json", raw)
    write(source / "RESULT.json", effective)
    emit(
        {
            "status": "recovered",
            "cell_id": CELL,
            "stage": "EQS",
            "same_thread": True,
            "source_and_sealed_K1_Q_K2_unchanged": True,
        }
    )


if __name__ == "__main__":
    main()
