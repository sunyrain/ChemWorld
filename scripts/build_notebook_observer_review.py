"""Read-only R51 review exporter; analyst annotations are not model-authored notes."""

# Chinese review prose intentionally uses Chinese punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

ANNOTATIONS = (
    Path(__file__).resolve().parents[1]
    / "workstreams/arxiv_v1/experiments"
    / "development-notebook-utility-20261012-review-annotations.json"
)
QUESTIONS = (
    "事前问题与预期",
    "过程中的公开修订或保留",
    "随后实际执行的操作",
    "对照是否成立",
    "最终支持与边界",
)
BOUNDARY = (
    "H = history、公开操作理由及最终报告；N = 同样来源，另有版本笔记。"
    "本页是离线派生审查，不是原 Agent 的笔记或内部思维。中文为 Codex 事后分析注释，"
    "英文原话与工具数值可展开核对。共同视图的来源不含笔记正文；笔记增量另列。"
    "H 无专用笔记，并非无记忆；两组均被要求给出事前预期与关键行动的公开理由。"
    "纯动作日志不能恢复未表达的假设。"
    "两条各四批的自适应研究线不是八次独立重复，也不是笔记收益的因果估计。"
)
TIMING = (
    "原话时间指宿主记录的调用序号；request 在该调用的工具结果之前。"
    "在前序返回中出现不等于模型实际依赖。批末报告不能回填事前判断。"
    "文中 preregistered 是参与者的用词，不代表正式预注册。"
    "假设被保留、证据不足和未记录均为有效审查结果。"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def collect(root: Path, arm: str) -> tuple[dict, list, list, list]:
    """Allowlist public sources; do not load provider traces or private world state."""
    sources, actions, errors, notes = {}, [], [], []
    for line, row in enumerate(records(root / arm / "interactions.jsonl"), 1):
        batch, call, tool = row["batch"], row["call"], row["tool"]
        args, result = row["arguments"], row.get("result", {})
        prefix = f"{arm}{batch}-c{call}"
        common = {
            "arm": arm,
            "batch": batch,
            "call": call,
            "recorded_at_unix": row.get("recorded_at_unix"),
            "path": f"{arm}/interactions.jsonl",
            "line": line,
            "tool": tool,
        }

        def add(kind: str, body: Any, phase: int, prefix=prefix, common=common) -> str:
            key = f"{prefix}-{kind}"
            sources[key] = {
                **common,
                "id": key,
                "kind": kind,
                "body": body,
                "order": [common["batch"], common["call"], phase],
                "channel": "common",
            }
            return key

        if "error" in result:
            # Preserve the failure, but do not turn rejected notes/reports into evidence.
            if tool.startswith("notebook_") or tool == "finish_batch":
                body = {
                    "argument_keys": sorted(args),
                    "error_present": True,
                    "detail": "See original source line; unaccepted content omitted.",
                }
            else:
                body = {"arguments": args, "result": result}
            key = add("error", body, 1)
            errors.append(key)
            continue
        if tool == "lab_step":
            reason = add("reason", args.get("reason", ""), 0)
            returned = {
                k: result[k]
                for k in (
                    "event_id",
                    "action",
                    "transaction_status",
                    "observation",
                    "uncertainty",
                    "processed_estimate",
                    "terminal",
                    "failure",
                )
                if k in result
            }
            response = add("result", returned, 1)
            actions.append(
                {
                    "arm": arm,
                    "batch": batch,
                    "call": call,
                    "action": result.get("action", args.get("action", {})),
                    "event_id": result.get("event_id"),
                    "status": result.get("transaction_status"),
                    "reason": reason,
                    "result": response,
                }
            )
        elif tool == "finish_batch" and result.get("finished"):
            add("report", args.get("report", ""), 1)
        elif tool in {"lab_history", "lab_reports", "lab_artifact"}:
            # Retrieval occurrence is not proof of use; original body remains at source.
            add("lookup", {"arguments": args, "returned_keys": sorted(result)}, 1)
        revision = (
            result.get("notebook", {}).get("revision")
            if tool == "finish_batch"
            else result.get("revision")
        )
        if tool in {"notebook_write", "notebook_restore", "finish_batch"} and revision:
            relative = f"{arm}/research/experiment_documents/notebook_history/{revision:08d}.json"
            record = read_json(root / relative)
            notes.append(
                {
                    **common,
                    "id": f"{arm}-v{revision}",
                    "revision": revision,
                    "kind": "notebook",
                    "channel": "notebook",
                    "order": [batch, call, 1],
                    "body": record["text"],
                    "path": relative,
                    "line": 1,
                    "public_cursor": record.get("public_cursor"),
                }
            )
    return sources, actions, errors, notes


def check_refs(refs: list[str], sources: dict, arm: str, cutoff: list[int]) -> None:
    for ref in refs:
        source = sources[ref]
        if source["channel"] != "common" or source["arm"] != arm:
            raise ValueError(f"Non-common or cross-arm source: {ref}")
        if source["order"] > cutoff:
            raise ValueError(f"Future source {ref} beyond {cutoff}")


def compare_actions(left: list[dict], right: list[dict]) -> dict:
    """Compare committed operation arguments, not noise or scientific equivalence."""
    diffs = []
    for i in range(max(len(left), len(right))):
        a = left[i]["action"] if i < len(left) else None
        b = right[i]["action"] if i < len(right) else None
        if a != b:
            fields = sorted(
                k for k in set(a or {}) | set(b or {}) if (a or {}).get(k) != (b or {}).get(k)
            )
            diffs.append({"step": i + 1, "fields": fields, "left": a, "right": b})
    return {"left_steps": len(left), "right_steps": len(right), "differences": diffs}


def build(root: Path, annotations: dict) -> dict:
    expected = {(arm, batch) for arm in ("H", "N") for batch in range(1, 5)}
    actual = [(b["arm"], b["batch"]) for b in annotations["batches"]]
    if len(actual) != len(expected) or set(actual) != expected:
        raise ValueError("R51 review must cover each of H1-H4 and N1-N4 exactly once")
    sources, actions, errors, notes = {}, [], [], []
    for arm in ("H", "N"):
        src, steps, failures, revisions = collect(root, arm)
        sources.update(src)
        actions.extend(steps)
        errors.extend(failures)
        notes.extend(revisions)
    batches = []
    for index, entry in enumerate(annotations["batches"], 1):
        arm, batch = entry["arm"], entry["batch"]
        steps = [a for a in actions if a["arm"] == arm and a["batch"] == batch]
        if len(entry["questions"]) != len(QUESTIONS):
            raise ValueError("Exactly five review questions required")
        questions = []
        for title, question in zip(QUESTIONS, entry["questions"], strict=True):
            if question["cutoff"][0] != batch:
                raise ValueError("Question cutoff must belong to its reviewed batch")
            check_refs(question["sources"], sources, arm, question["cutoff"])
            if not question["sources"] and question["status"] != "未记录":
                raise ValueError("An answer must cite sources or explicitly mark missing")
            questions.append({"title": title, **question})
        batches.append({**entry, "questions": questions, "actions": steps})
        print(
            f"Review {index}/{len(annotations['batches'])}: {arm}{batch}, {len(steps)} actions",
            flush=True,
        )
    note_map = {n["revision"]: n for n in notes if n["arm"] == "N"}
    if sorted(note_map) != sorted(n["revision"] for n in annotations["notebook_delta"]):
        raise ValueError("Every N notebook revision needs an explicit disposition")
    deltas = []
    for delta in annotations["notebook_delta"]:
        note = note_map[delta["revision"]]
        check_refs(delta["contemporaneous"], sources, "N", note["order"])
        for ref in delta["later"]:
            if sources[ref]["channel"] != "common" or sources[ref]["arm"] != "N":
                raise ValueError(f"Invalid later comparison: {ref}")
            if sources[ref]["order"] <= note["order"]:
                raise ValueError(f"Later comparison is not later: {ref}")
        deltas.append({**delta, "note": note})
    comparisons = []
    for a, b in annotations["compare_pairs"]:
        left = [s for s in actions if f"{s['arm']}{s['batch']}" == a and s["status"] == "committed"]
        right = [
            s for s in actions if f"{s['arm']}{s['batch']}" == b and s["status"] == "committed"
        ]
        comparisons.append({"left": a, "right": b, **compare_actions(left, right)})
    summary = {
        "mode": "retrospective_development_review",
        "new_agent_runs": 0,
        "new_physical_actions": 0,
        "batches": len(batches),
        "questions": sum(len(b["questions"]) for b in batches),
        "questions_with_sources": sum(bool(q["sources"]) for b in batches for q in b["questions"]),
        "physical_requests": len(actions),
        "committed_actions": sum(a["status"] == "committed" for a in actions),
        "tool_errors": len(errors),
        "notebook_revisions_reviewed": len(deltas),
        "question_statuses": dict(Counter(q["status"] for b in batches for q in b["questions"])),
        "note_categories": dict(Counter(c for d in deltas for c in d["categories"])),
        "note_category_counting": "Labels overlap; versions are not independent samples.",
        "semantic_review": (
            "Analyst-authored, source-linked, not blinded or automatically verified."
        ),
        "conclusions": annotations["conclusions"],
    }
    return {
        "summary": summary,
        "batches": batches,
        "sources": sources,
        "errors": errors,
        "notebook_delta": deltas,
        "comparisons": comparisons,
    }


def body_text(source: dict) -> str:
    body = source["body"]
    return body if isinstance(body, str) else json.dumps(body, ensure_ascii=False, indent=2)


def render_markdown(data: dict) -> str:
    lines = ["# 研究过程审查本 · R51 八批", "", BOUNDARY, "", TIMING, ""]
    lines += ["## 本次发现", "", *[f"- {s}" for s in data["summary"]["conclusions"]], ""]
    for batch in data["batches"]:
        key = f"{batch['arm']}{batch['batch']}"
        lines += [f"## {key} · {batch['title']}", "", batch["overview"], ""]
        for q in batch["questions"]:
            lines += [
                f"### {q['title']} · {q['status']}",
                "",
                q["analysis"],
                "",
                f"可引用时间上限：{q['cutoff']}（批次、调用、0=request / 1=result）；"
                "分析者事后整理。",
                "",
            ]
            for ref in q["sources"]:
                lines += [f"- [{ref}](#{ref})"]
            lines += [""]
    lines += [
        "## 完整操作序列比较（批末回顾）",
        "",
        "仅比较已提交操作参数。相同操作不表示同噪声、同实际釜温或有充分独立重复。",
        "",
    ]
    for c in data["comparisons"]:
        lines += [f"### {c['left']} / {c['right']} · {c['left_steps']} / {c['right_steps']} 步", ""]
        lines += [f"- 第 {d['step']} 步：{', '.join(d['fields'])}" for d in c["differences"]]
        lines += [""]
    lines += [
        "## N 组笔记增量（单独来源）",
        "",
        "只比较已标注的决策与科学内容，不声称逐句穷尽。后来的重复不能抹去更早的公开承诺；"
        "共同日志也可能受写笔记影响，此处不是移除笔记的因果实验。",
        "",
    ]
    for d in data["notebook_delta"]:
        n = d["note"]
        lines += [
            f"### v{n['revision']} · N{n['batch']} / call {n['call']}",
            "",
            "分类：" + "、".join(d["categories"]),
            "",
            d["analysis"],
            "",
            "同期共同来源："
            + (", ".join(f"[{r}](#{r})" for r in d["contemporaneous"]) or "无对应同期陈述"),
            "",
            "后来共同来源："
            + (", ".join(f"[{r}](#{r})" for r in d["later"]) or "未指定后续对应陈述"),
            "",
            f"笔记原件：../{n['path']}。",
            "",
            "<details><summary>原始笔记（模型原话）</summary>",
            "",
            "```text",
            n["body"],
            "```",
            "",
            "</details>",
            "",
        ]
    lines += [
        "## 保留的工具错误",
        "",
        *[f"- [{e}](#{e})" for e in data["errors"]],
        "",
        "H4 四次请求在很短时间内成组提交，不能认定为四次读过反馈后仍忽略。",
        "",
        "## 共同来源原文索引",
        "",
    ]
    for ref, s in data["sources"].items():
        lines += [
            f'<a id="{ref}"></a>',
            f"### {ref}",
            "",
            f"来源：../{s['path']}，第 {s['line']} 行；{s['kind']}。",
            "",
            "```text",
            body_text(s),
            "```",
            "",
        ]
    return "\n".join(lines)


def render_html(data: dict) -> str:
    esc = html.escape

    def refs(keys: list[str]) -> str:
        return " ".join(f'<a class="ref" href="#{esc(k)}">{esc(k)}</a>' for k in keys) or "未记录"

    def source_html(s: dict) -> str:
        return (
            f'<details id="{esc(s["id"])}"><summary>{esc(s["id"])} · {esc(s["kind"])}</summary>'
            f'<p class="meta">{esc(s["path"])} · line {s["line"]} · '
            f"调用 {s['call']} · {'结果前' if s['order'][2] == 0 else '返回／提交后'}</p>"
            f"<pre>{esc(body_text(s))}</pre></details>"
        )

    nav = "".join(
        f'<a href="#{b["arm"]}{b["batch"]}">{b["arm"]}{b["batch"]}</a>' for b in data["batches"]
    )
    out = [
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>ChemWorld · 研究过程审查</title>",
        """<style>
body{margin:0;background:#f6f5f1;color:#252b2b;
font:16px/1.75 system-ui,"Microsoft YaHei",sans-serif}
main{max-width:1120px;margin:auto;padding:36px 24px}
h1{font-size:30px}h2{font-size:24px;margin-top:0}h3{font-size:18px}
nav{position:sticky;top:0;background:#fff;padding:12px 24px;
border-bottom:1px solid #ddd;z-index:1}
nav a{margin-right:20px}a{color:#205f59}
section{background:white;border:1px solid #ddd;border-radius:8px;padding:28px;margin:24px 0}
.grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
.card{border-top:2px solid #c4d6d2;padding:12px 4px}
.card:last-child{grid-column:1/-1}.meta{font-size:13px;color:#576264}
.ref{display:inline-block;font-size:13px;margin:3px 8px 3px 0}
details{border-top:1px solid #e5e5e5;padding:12px 0;scroll-margin-top:70px}
summary{cursor:pointer;font-weight:600}
pre{white-space:pre-wrap;overflow-wrap:anywhere;
font:14px/1.7 ui-monospace,Consolas,monospace;background:#f6f7f7;padding:16px}
.badge{font-size:13px;color:#58665e;margin-left:10px}
table{border-collapse:collapse;width:100%}
td,th{padding:10px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}
section[id]{scroll-margin-top:70px}
@media(max-width:750px){.grid{display:block}main{padding:18px 12px}
section{padding:18px}nav a{margin-right:12px}
details,section[id]{scroll-margin-top:110px}}
@media print{nav{position:static}.grid{display:block}section{break-inside:auto}}
</style>""",
        f'<nav>{nav}<a href="#delta">笔记增量</a><a href="#sources">原文索引</a></nav><main>',
        f'<h1>研究过程审查本</h1><p>{esc(BOUNDARY)}</p><p class="meta">{esc(TIMING)}</p>',
        "<section><h2>这轮记录告诉我们什么</h2><ul>",
        *[f"<li>{esc(s)}</li>" for s in data["summary"]["conclusions"]],
        f'</ul><p class="meta">{data["summary"]["batches"]} 批 · '
        f"{data['summary']['questions']} 个审查问题 · "
        f"{data['summary']['notebook_revisions_reviewed']} 个笔记版本；"
        "有来源不等于问题已被完整回答；来源检查不等于语义正确性验证。</p></section>",
    ]
    for b in data["batches"]:
        key = f"{b['arm']}{b['batch']}"
        out += [
            f'<section id="{key}"><h2>{key} · {esc(b["title"])}</h2>'
            f'<p>{esc(b["overview"])}</p><div class="grid">'
        ]
        for q in b["questions"]:
            out += [
                f'<article class="card"><h3>{esc(q["title"])}'
                f'<span class="badge">{esc(q["status"])}</span></h3>',
                f'<p>{esc(q["analysis"])}</p><p class="meta">'
                f"引用截止：批次 / 调用 / 阶段 {q['cutoff']}；中文为事后分析。</p>",
                refs(q["sources"]),
                "</article>",
            ]
        out += ["</div><details><summary>逐步查看全部操作与公开理由</summary>"]
        for a in b["actions"]:
            out += [
                f"<p><strong>call {a['call']} · {esc(a['action'].get('operation', ''))}"
                f"</strong> · {esc(str(a['status']))}</p>",
                source_html(data["sources"][a["reason"]]),
                source_html(data["sources"][a["result"]]),
            ]
        out += ["</details></section>"]
    out += [
        '<section><h2>实际操作对照 · 批末回顾</h2><p class="meta">'
        "仅比已提交参数；不等于同噪声、同实际釜温或充分独立重复。</p>",
        "<table><tr><th>比较</th><th>步数</th><th>不同位置与参数</th></tr>",
    ]
    for c in data["comparisons"]:
        changes = "；".join(
            f"第 {d['step']} 步：{', '.join(d['fields'])}" for d in c["differences"]
        )
        out += [
            f"<tr><td>{c['left']} / {c['right']}</td>"
            f"<td>{c['left_steps']} / {c['right_steps']}</td><td>{esc(changes)}</td></tr>"
        ]
    out += [
        '</table></section><section id="delta"><h2>笔记额外留下了什么</h2>',
        "<p>以下是独立来源。只比较已标注内容，不声称逐句穷尽；"
        "同一版本可同时包含重复和新增内容。后来的重复不抹去较早承诺，"
        "N 的共同日志也可能已受写笔记影响。</p>",
    ]
    for d in data["notebook_delta"]:
        n = d["note"]
        out += [
            f'<article class="card"><h3>N{n["batch"]} · v{n["revision"]} / call {n["call"]}</h3>',
            f'<p class="meta">{esc(" · ".join(d["categories"]))}</p><p>{esc(d["analysis"])}</p>',
            f"<p>同期共同来源：{refs(d['contemporaneous'])}</p><p>后来共同来源：{refs(d['later'])}</p>",
            source_html(n),
            "</article>",
        ]
    out += [
        "</section><section><h2>保留的错误与拒绝</h2>",
        "<p>H4 四次参数错误均保留。成组调用不能解释为四次忽略反馈。</p>",
        refs(data["errors"]),
        "</section>",
        '<section id="sources"><h2>共同来源原文索引</h2><p>动作理由和工具返回分开保存。'
        "笔记及 finish_batch 的 notebook_text 不进入此索引。"
        "检索元数据只说明调用发生，原始返回保留在来源行。</p>",
    ]
    # Action sources already have unique IDs in the per-batch timeline.
    action_ids = {a[k] for b in data["batches"] for a in b["actions"] for k in ("reason", "result")}
    out += [source_html(s) for k, s in data["sources"].items() if k not in action_ids]
    out += [
        """</section></main><script>
function showSource(id){
  const t=document.getElementById(id);if(!t)return;
  let p=t;while(p){if(p.tagName==="DETAILS")p.open=true;p=p.parentElement;}
  setTimeout(()=>t.scrollIntoView({block:"start"}),0);
}
document.addEventListener("click",e=>{
  const a=e.target.closest('a[href^="#"]');if(a)showSource(a.hash.slice(1));
});
showSource(location.hash.slice(1));
</script></html>"""
    ]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--annotations", type=Path, default=ANNOTATIONS)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    data = build(args.input, read_json(args.annotations))
    output = args.input / "observer-review"
    output.mkdir(exist_ok=True)
    (output / "review.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "review.md").write_text(render_markdown(data), encoding="utf-8")
    (output / "review.html").write_text(render_html(data), encoding="utf-8")
    if args.summary:
        args.summary.write_text(
            json.dumps(data["summary"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(data["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
