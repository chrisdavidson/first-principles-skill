#!/usr/bin/env python3
"""abandonment Phase 0 -- the offline reading pre-registered in
docs/abandonment-preregistration.md section 3. Zero spend: it reads frozen transcripts only.

    python3 tests/abandonment/phase0_reading.py            # table + H1 + dispatch + rate
    python3 tests/abandonment/phase0_reading.py --json     # also writes phase0.json

Definitions are the pre-registration's section 2, and extraction is w4-paired's `extract`
(Stage A extractor plus persisted hand-back recovery) -- reused, never re-implemented, so a
fix to one grammar cannot silently diverge from the other.

A recorded reading, never a gate.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

spec = importlib.util.spec_from_file_location("_w4", REPO_ROOT / "tests/w4-paired/run_paired.py")
w4 = importlib.util.module_from_spec(spec)
sys.modules["_w4"] = w4
spec.loader.exec_module(w4)
stage_a = w4.stage_a

# (glob, body label). The label names the body the transcript was produced on.
CORPORA = (
    ("tests/w4-paired/raw/*.old.*.jsonl", "v9.0.0"),
    ("tests/w4-paired/raw/*.new.*.jsonl", "v9.12.0"),
    ("tests/emission-stage-a-v9.14/raw/*.jsonl", "v9.12.0"),
    ("tests/emission-stage-a-v9.14/raw-attempt1/*.jsonl", "v9.12.0"),
    ("tests/live-conformance-v9.0/*.jsonl", "v9.0-era"),
    ("tests/quality-provenance-v8.24/*.jsonl", "v8.24"),
)

DISPATCH_PATTERN = re.compile(
    r"concise|brief|short|quick|summar|high[- ]level|don'?t (use|run)"
    r"|no (tools|research|web)|without (research|tools)",
    re.I,
)
MIN_SECTIONS = stage_a.MIN_SECTIONS


def _events(jsonl: str):
    for line in jsonl.splitlines():
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def legacy_handback(jsonl: str) -> str:
    """The Agent tool's result, for captures that predate the `[Subagent hand-back]` frame.

    Amendment 1 (docs/abandonment-preregistration.md section 8). Before the harness framed a
    hand-back, the subagent's document arrived as the plain `tool_result` of the main
    session's `Agent` call, which `extract_subagent_text` does not recognise: on
    `tests/live-conformance-v9.0/` and `tests/quality-provenance-v8.24/` it returns 0 words,
    while each committed `<id>.md` -- that corpus's own verbatim extraction -- is this
    tool result less a ~20-word trailer. Used only when the framed extraction is empty.
    """
    agent_ids, out = set(), ""
    for obj in _events(jsonl):
        content = obj.get("message", {}).get("content", []) or []
        if obj.get("parent_tool_use_id") or not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict):
                continue
            if obj.get("type") == "assistant" and b.get("type") == "tool_use" \
                    and b.get("name") == "Agent":
                agent_ids.add(b.get("id"))
            if obj.get("type") == "user" and b.get("type") == "tool_result" \
                    and b.get("tool_use_id") in agent_ids:
                c = b.get("content")
                text = c if isinstance(c, str) else "".join(
                    x.get("text", "") for x in c or [] if isinstance(x, dict))
                if stage_a._HANDBACK_MARK not in text:
                    out = text
    return out


def read_attempt(path: Path, body: str) -> dict:
    jsonl = path.read_text(encoding="utf-8")
    dispatch_prompts, sub_events, tools, reads = [], 0, [], []
    for obj in _events(jsonl):
        if obj.get("parent_tool_use_id"):
            sub_events += 1
        if obj.get("type") != "assistant":
            continue
        for b in obj.get("message", {}).get("content", []) or []:
            if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                continue
            if obj.get("parent_tool_use_id"):
                tools.append(b.get("name"))
                if b.get("name") == "Read":
                    reads.append(str(b.get("input", {}).get("file_path", "")))
            elif b.get("name") == "Agent":
                dispatch_prompts.append(str(b.get("input", {}).get("prompt", "")))
    dispatched = bool(dispatch_prompts)
    doc, _orch, status = w4.extract(jsonl) if dispatched else ("", "", "ok")
    legacy = False
    if dispatched and status != "transport" and not doc.strip():
        doc = legacy_handback(jsonl)
        legacy = bool(doc.strip())
    observable = dispatched and sub_events > 0
    prompt = dispatch_prompts[0] if dispatch_prompts else ""
    return {
        "attempt": path.relative_to(REPO_ROOT).as_posix(),
        "body": body,
        "dispatched": dispatched,
        "transport": status == "transport",
        "legacy_handback": legacy,
        "observable": observable,
        "tool_calls": len(tools) if observable else None,
        "template_read": any(r.endswith("output-template.md") for r in reads),
        "one_shot": observable and not tools,
        "abandoned": dispatched and status != "transport"
        and len(stage_a.sections_present(doc)) < MIN_SECTIONS,
        "dispatch_words": len(prompt.split()),
        "dispatch_marker": bool(DISPATCH_PATTERN.search(prompt)),
        "dispatch_match": (m.group(0) if (m := DISPATCH_PATTERN.search(prompt)) else ""),
    }


def collect() -> list[dict]:
    rows = []
    for pattern, body in CORPORA:
        for path in sorted(REPO_ROOT.glob(pattern)):
            rows.append(read_attempt(path, body))
    return rows


def h1(rows: list[dict]) -> dict:
    pool = [r for r in rows if r["observable"] and not r["transport"]]
    a = [r["attempt"] for r in pool if r["abandoned"] and not r["one_shot"]]
    b = [r["attempt"] for r in pool if r["abandoned"] and r["template_read"]]
    return {"pool": len(pool), "abandoned": sum(r["abandoned"] for r in pool),
            "a_violations": a, "b_violations": b, "holds": not a and not b}


def dispatch_side(rows: list[dict]) -> dict:
    pool = [r for r in rows if r["observable"] and not r["transport"]]
    one = [r for r in pool if r["one_shot"]]
    rest = [r for r in pool if not r["one_shot"]]
    rate = lambda g: (sum(r["dispatch_marker"] for r in g), len(g))
    k1, n1 = rate(one)
    k2, n2 = rate(rest)
    implicated = n1 > 0 and k1 * 2 >= n1 and k2 * 4 <= n2
    med = lambda g: sorted(r["dispatch_words"] for r in g)[len(g) // 2] if g else 0
    return {"one_shot_marker": [k1, n1], "other_marker": [k2, n2],
            "one_shot_median_words": med(one), "other_median_words": med(rest),
            "implicated": implicated}


def emission(rows: list[dict]) -> dict:
    out = {}
    for body in dict.fromkeys(b for _, b in CORPORA):
        g = [r for r in rows if r["body"] == body and r["dispatched"] and not r["transport"]]
        out[body] = [sum(not r["abandoned"] for r in g), len(g)]
    return out


def main() -> int:
    rows = collect()
    print("abandonment Phase 0 -- offline reading (a recorded reading, never a gate)\n")
    print(f"{'attempt':<58}{'body':<10}{'disp':>5}{'obs':>5}{'tools':>6}{'tmpl':>5}"
          f"{'1shot':>6}{'aband':>6}{'dwords':>7}  marker")
    for r in rows:
        t = "-" if r["tool_calls"] is None else r["tool_calls"]
        print(f"{r['attempt'][-57:]:<58}{r['body']:<10}{r['dispatched']:>5}{r['observable']:>5}"
              f"{t:>6}{r['template_read']:>5}{r['one_shot']:>6}{r['abandoned']:>6}"
              f"{r['dispatch_words']:>7}  {r['dispatch_match']}")
    print()
    for body in dict.fromkeys(b for _, b in CORPORA):
        g = [r for r in rows if r["body"] == body and r["observable"] and not r["transport"]]
        print(f"{body:<10} observable {len(g):>3}  one-shot {sum(r['one_shot'] for r in g):>2}  "
              f"abandoned {sum(r['abandoned'] for r in g):>2}  "
              f"abandoned|one-shot {sum(r['abandoned'] and r['one_shot'] for r in g)}/"
              f"{sum(r['one_shot'] for r in g)}  "
              f"template-read {sum(r['template_read'] for r in g)}")
    res = {"h1": h1(rows), "dispatch": dispatch_side(rows), "emission": emission(rows)}
    hh = res["h1"]
    print(f"\nH1 over {hh['pool']} observable dispatched attempts, {hh['abandoned']} abandoned:")
    print(f"  (a) every abandoned attempt is one-shot       -> "
          f"{'HOLDS' if not hh['a_violations'] else 'FAILS ' + str(hh['a_violations'])}")
    print(f"  (b) no template-reading attempt is abandoned  -> "
          f"{'HOLDS' if not hh['b_violations'] else 'FAILS ' + str(hh['b_violations'])}")
    print(f"  H1: {'HOLDS' if hh['holds'] else 'FAILS'}")
    d = res["dispatch"]
    print(f"\ndispatch prompt marker: one-shot {d['one_shot_marker'][0]}/{d['one_shot_marker'][1]}"
          f"  others {d['other_marker'][0]}/{d['other_marker'][1]}"
          f"  | median words one-shot {d['one_shot_median_words']}, others "
          f"{d['other_median_words']}  -> dispatch side "
          f"{'IMPLICATED' if d['implicated'] else 'not implicated'}")
    print("\ncontract-emission reliability (kept / dispatched, non-transport):")
    for body, (k, n) in res["emission"].items():
        print(f"  {body:<10} {k}/{n}")
    if "--json" in sys.argv:
        (HERE / "phase0.json").write_text(
            json.dumps({"rows": rows, **res}, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
