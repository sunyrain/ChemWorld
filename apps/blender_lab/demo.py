"""Repeatable, inventory-aware API example. Does not reset existing experiments."""

import json
import urllib.request
from pathlib import Path


def run_demo(base="http://127.0.0.1:8877"):
    def req(path, data=None, method=None):
        request = urllib.request.Request(
            base + path,
            data=None if data is None else json.dumps(data).encode(),
            method=method,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
            request, timeout=3
        ) as r:
            return json.load(r)

    def action(id, **data):
        return req(f"/api/v1/assets/{id}/actions", data, "POST")

    def patch(id, **data):
        return req(f"/api/v1/assets/{id}", data, "PATCH")

    for target, source, amount in [
        ("beaker_01", "water_01", 180),
        ("beaker_01", "cuso4_01", 20),
        ("reactor_01", "water_01", 350),
        ("flask_01", "water_01", 80),
    ]:
        vessel = req(f"/api/v1/assets/{target}")
        # Seed only the missing individual ingredient in an existing vessel.
        if not any(c["reagent_id"] == source for c in vessel["state"]["contents"]):
            patch(source, cap_open=True)
            action(source, action="dispense", target_id=target, amount=amount, unit="ml")
            patch(source, cap_open=source == "water_01")
    patch("hood_01", fan_on=True, sash_open_pct=35)
    patch("hotplate_01", target_temperature_c=45, stir_rpm=180)
    action("hotplate_01", action="start")
    patch("reactor_01", target_temperature_c=40, stir_rpm=120)
    action("reactor_01", action="start")
    patch("chiller_01", target_temperature_c=18)
    action("chiller_01", action="start")
    results = []
    for id, method in [
        ("balance_01", "weigh"),
        ("ph_01", "measure"),
        ("uvvis_01", "measure"),
        ("ftir_01", "measure"),
    ]:
        results.append(action(id, action=method, sample_id="beaker_01"))
    action("reactor_01", action="select")
    result = {"status": "complete", "mode": "educational_simulation", "results": results}
    out = Path(__file__).resolve().parent / "runtime"
    out.mkdir(exist_ok=True)
    (out / "demo_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, indent=2))
