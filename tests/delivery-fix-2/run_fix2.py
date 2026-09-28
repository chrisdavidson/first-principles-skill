#!/usr/bin/env python3
"""delivery-fix-2 -- the re-run pre-registered in docs/delivery-fix-2-preregistration.md.

    python3 tests/delivery-fix-2/run_fix2.py run --body <wt>/first-principles --cwd <empty dir>
    python3 tests/delivery-fix-2/run_fix2.py read
    python3 tests/delivery-fix-2/run_fix2.py --self-test

Same transport, capture, prompts and passes as delivery-fix (reused, not copied); the judge is
replaced by a PER-SECTION fidelity check, because v2's resumed message is itself a full copy and
a whole-document ratio against the first rendering would count the document twice.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

spec = importlib.util.spec_from_file_location("_fx1", REPO_ROOT / "tests/delivery-fix/run_fix.py")
fx = importlib.util.module_from_spec(spec)
sys.modules["_fx1"] = fx
spec.loader.exec_module(fx)

FIDELITY = 0.90
_HEADING = re.compile(r"^(#{1,4})\s+(.*\S)\s*$")


def _norm(title: str) -> str:
    """Heading identity: drop numbering and markup, so '# 2. Assumptions Table' and
    '## 2. Assumptions Table' and '## Assumptions Table' are one section."""
    t = re.sub(r"[*_`]", "", title).strip()
    t = re.sub(r"^\d+[.)]\s*", "", t)
    return t.lower()[:60]


def sections(doc: str) -> dict[str, int]:
    """{normalised heading: words under it, up to the next heading of ANY level (1-4)}.

    Level-agnostic on purpose: a re-send that demotes `## 2. Assumptions Table` to `###` must
    still be matched section for section, not scored as missing."""
    out: dict[str, int] = {}
    cur, buf = None, []
    def flush():
        if cur is not None:
            out[cur] = out.get(cur, 0) + len(" ".join(buf).split())
    for ln in doc.splitlines():
        m = _HEADING.match(ln)
        if m:
            flush()
            cur, buf = _norm(m.group(2)), []
        else:
            buf.append(ln)
    flush()
    return out


def judge(received: str, turns: list[dict]) -> dict:
    """Pre-registration section 3: every level-1/2 section the agent wrote in its first
    rendering must reach the caller with >= 90% of the most words it was ever written with."""
    cut, first = fx.first_rendering(turns)
    ref: dict[str, int] = {}
    # the first rendering may hold the document twice (a cut copy and a full re-send): per
    # heading, the reference is the MOST words that heading was ever written with.
    for part in [t["text"] for t in turns if t["role"] == "agent" and t["text"]] if cut else []:
        if part and part in first:
            for k, v in sections(part).items():
                ref[k] = max(ref.get(k, 0), v)
    got = sections(received)
    short = {k: (got.get(k, 0), v) for k, v in ref.items()
             if v >= 20 and got.get(k, 0) < FIDELITY * v}
    total_ref, total_got = sum(ref.values()), sum(min(got.get(k, 0), v) for k, v in ref.items())
    return {
        "cut_off": cut,
        "first_words": len(first.split()), "received_words": len(received.split()),
        "fidelity": round(total_got / total_ref, 3) if total_ref else None,
        "sections_first": len(ref), "sections_received": len([k for k in ref if k in got]),
        "short_sections": {k: f"{a}/{b}" for k, (a, b) in short.items()},
        "whole_with_fidelity": (not cut) or (bool(ref) and not short),
        "resend_cut_off": sum(1 for t in turns if t["role"] == "agent"
                              and t.get("stop") == "max_tokens") > 1,
    }


def self_test() -> int:
    body = lambda n: " w" * n
    doc = ("## Self-Audit Gate (process output)\n" + body(500) + "\n## 1. Problem Essence\n"
           + body(170) + "\n## 2. Assumptions Table\n" + body(870) + "\n## 6. Conclusion\n" + body(660))
    head, tail = doc[: len(doc) // 2], doc[len(doc) // 2:]
    cut = [{"role": "agent", "text": head, "tools": [], "stop": "max_tokens"},
           {"role": "user", "text": "Output token limit hit. Resume directly"}]
    v2_resend = cut + [{"role": "agent", "text": doc, "tools": [], "stop": "end_turn"}]
    v1_tail = cut + [{"role": "agent", "text": tail, "tools": [], "stop": "end_turn"}]
    no_process = doc.replace("## Self-Audit Gate (process output)\n" + body(500) + "\n", "")
    condensed = doc.replace(body(870), body(400))
    checks = {
        "v2: a verbatim full re-send in the resumed message is WHOLE":
            judge(doc, v2_resend)["whole_with_fidelity"],
        "v1-style: a tail continuation delivered alone is LOST":
            not judge(tail, v1_tail)["whole_with_fidelity"],
        "dropping process output is LOST (the v1 re-run failure)":
            not judge(no_process, v2_resend)["whole_with_fidelity"],
        "a condensed section (under 90%) is LOST even with every heading":
            not judge(condensed, v2_resend)["whole_with_fidelity"],
        "heading level and numbering do not change section identity":
            sections("# 2. Assumptions Table\nx y\n") == sections("### Assumptions Table\nx y\n"),
        "a verbatim re-send demoted one heading level is still WHOLE":
            judge(doc.replace("\n## ", "\n### ").replace("## Self", "### Self", 1), v2_resend)["whole_with_fidelity"],
        "a run with no cut-off is WHOLE by definition":
            judge(doc, [{"role": "agent", "text": doc, "tools": [], "stop": "end_turn"}])["whole_with_fidelity"],
    }
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    ok = all(checks.values())
    print(f"delivery-fix-2 --self-test: {'PASS' if ok else 'FAIL'} ({len(checks)} controls)")
    return 0 if ok else 1


# Point the reused runner at this directory and this judge.
fx.HERE, fx.RAW = HERE, HERE / "raw"
fx.judge = judge
fx.self_test = self_test

if __name__ == "__main__":
    sys.exit(fx.main())
