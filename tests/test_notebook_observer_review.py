from __future__ import annotations

import copy
import json
from html.parser import HTMLParser

import pytest
from scripts import build_notebook_observer_review as review


def write_rows(root, arm, rows):
    path = root / arm / "interactions.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")


def event(batch, call, tool, arguments, result):
    return {"batch": batch, "call": call, "tool": tool, "arguments": arguments, "result": result}


def test_common_sources_ignore_note_content_and_rejected_reports(tmp_path):
    note = tmp_path / "N/research/experiment_documents/notebook_history/00000001.json"
    note.parent.mkdir(parents=True)
    note.write_text(json.dumps({"text": "NOTE_SENTINEL"}), encoding="utf-8")
    rows = [
        event(
            1,
            1,
            "lab_step",
            {"reason": "test", "action": {"operation": "heat"}},
            {"transaction_status": "committed", "private_state": "PRIVATE_SENTINEL"},
        ),
        event(1, 2, "notebook_write", {"text": "NOTE_SENTINEL"}, {"revision": 1}),
        event(
            1,
            3,
            "finish_batch",
            {"report": "accepted", "notebook_text": "NOTE_SENTINEL"},
            {"finished": True},
        ),
        event(
            1, 4, "notebook_write", {"text": "REJECTED_NOTE"}, {"error": "REJECTED_NOTE is invalid"}
        ),
        event(
            1,
            5,
            "finish_batch",
            {"report": "REJECTED_REPORT"},
            {"error": "REJECTED_REPORT is invalid"},
        ),
        event(1, 6, "finish_batch", {"report": "UNACCEPTED"}, {"finished": False}),
        event(1, 7, "lab_artifact", {"fields": ["action"]}, {"error": "unknown field"}),
    ]
    write_rows(tmp_path, "N", rows)
    sources, actions, errors, notes = review.collect(tmp_path, "N")
    common = json.dumps(sources)
    for text in (
        "NOTE_SENTINEL",
        "REJECTED_NOTE",
        "REJECTED_REPORT",
        "PRIVATE_SENTINEL",
        "UNACCEPTED",
    ):
        assert text not in common
    assert len(errors) == 3 and len(actions) == 1
    assert sources["N1-c7-error"]["body"]["result"]["error"] == "unknown field"
    assert notes[0]["body"] == "NOTE_SENTINEL"
    note.write_text(json.dumps({"text": "CHANGED_ONLY_NOTE"}), encoding="utf-8")
    assert review.collect(tmp_path, "N")[:3] == (sources, actions, errors)


def test_time_order_and_channel_boundaries():
    sources = {
        "reason": {"channel": "common", "arm": "H", "order": [3, 12, 0]},
        "result": {"channel": "common", "arm": "H", "order": [3, 12, 1]},
        "report": {"channel": "common", "arm": "H", "order": [3, 18, 1]},
        "note": {"channel": "notebook", "arm": "H", "order": [3, 11, 1]},
        "other_arm": {"channel": "common", "arm": "N", "order": [1, 1, 0]},
    }
    review.check_refs(["reason"], sources, "H", [3, 12, 0])
    review.check_refs(["report"], sources, "H", [3, 18, 1])
    for ref in ("result", "report", "note", "other_arm"):
        with pytest.raises(ValueError):
            review.check_refs([ref], sources, "H", [3, 12, 0])


def test_operation_comparison_detects_sampling_and_measurement_changes():
    left = [{"action": {"operation": "measure", "sample_volume": 1, "instrument": "HPLC"}}]
    right = [{"action": {"operation": "measure", "sample_volume": 2, "instrument": "NMR"}}]
    result = review.compare_actions(left, right)
    assert result["differences"][0]["fields"] == ["instrument", "sample_volume"]
    assert review.compare_actions(left, left)["differences"] == []
    assert review.compare_actions(left, [])["differences"][0]["right"] is None


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a" and values.get("href", "").startswith("#"):
            self.refs.append(values["href"][1:])


def synthetic_study(root):
    annotations = {"batches": [], "notebook_delta": [], "compare_pairs": [], "conclusions": []}
    for arm in ("H", "N"):
        rows = []
        for batch in range(1, 5):
            rows.append(
                event(
                    batch,
                    1,
                    "lab_step",
                    {"reason": "<script>bad()</script>"},
                    {"action": {"operation": "heat"}, "transaction_status": "committed"},
                )
            )
            rows.append(event(batch, 2, "finish_batch", {"report": "accepted"}, {"finished": True}))
            annotations["batches"].append(
                {
                    "arm": arm,
                    "batch": batch,
                    "title": "test",
                    "overview": "test",
                    "questions": [
                        {
                            "analysis": "test",
                            "status": "cited",
                            "sources": [f"{arm}{batch}-c1-reason"],
                            "cutoff": [batch, 1, 0],
                        }
                        for _ in range(5)
                    ],
                }
            )
        write_rows(root, arm, rows)
    return annotations


def test_export_preserves_sources_and_has_resolvable_escaped_links(tmp_path, monkeypatch):
    annotations = synthetic_study(tmp_path)
    ann_path = tmp_path / "annotations.json"
    ann_path.write_text(json.dumps(annotations), encoding="utf-8")
    original_review = tmp_path / "review.md"
    original_review.write_text("KEEP ORIGINAL", encoding="utf-8")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    monkeypatch.setattr(
        "sys.argv", ["review", "--input", str(tmp_path), "--annotations", str(ann_path)]
    )
    review.main()
    assert all(p.read_bytes() == body for p, body in before.items())
    output = tmp_path / "observer-review"
    data = review.read_json(output / "review.json")
    assert data["summary"]["batches"] == 8
    assert data["summary"]["questions_with_sources"] == 40
    page = (output / "review.html").read_text(encoding="utf-8")
    assert "<script>bad()" not in page and "&lt;script&gt;bad()" in page
    parser = Links()
    parser.feed(page)
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.refs) <= set(parser.ids)


def test_duplicate_batch_cannot_replace_missing_batch(tmp_path):
    annotations = synthetic_study(tmp_path)
    annotations["batches"][-1] = copy.deepcopy(annotations["batches"][0])
    with pytest.raises(ValueError, match="exactly once"):
        review.build(tmp_path, annotations)
