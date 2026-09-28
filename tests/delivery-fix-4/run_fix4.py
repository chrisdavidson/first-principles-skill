#!/usr/bin/env python3
"""delivery-fix-4 -- the re-run pre-registered in docs/delivery-fix-4-preregistration.md.

    python3 tests/delivery-fix-4/run_fix4.py run --body <wt>/first-principles --cwd <empty dir>
    python3 tests/delivery-fix-4/run_fix4.py read
    python3 tests/delivery-fix-4/run_fix4.py --self-test

Reuses delivery-fix-3's transport, capture, file collection and replay. Two things differ, both
fixed before any run: the replay also executes the agent's own Python edits (every heredoc body
is removed before the command words are checked), and a run is DELIVERED when the file was used,
carries all six sections, was read by the main session, and replays byte for byte -- in-place
revision is allowed, silent change is not.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

spec = importlib.util.spec_from_file_location("_fx3", REPO_ROOT / "tests/delivery-fix-3/run_fix3.py")
fx = importlib.util.module_from_spec(spec)
sys.modules["_fx3"] = fx
spec.loader.exec_module(fx)

_verbs_v3 = fx._verbs
_HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?\n.*?\n\s*\1\b", re.S)


def _verbs(command: str):
    """v3's quote-aware command words, after removing EVERY heredoc body (not only FP_EOF)."""
    return _verbs_v3(_HEREDOC.sub("", command))


fx._verbs = _verbs
_SAFE_V4 = fx._SAFE_VERBS | {"python3", "python"}                                  # as registered
_SAFE_V4B = _SAFE_V4 | {"readlink", "date", "file", "which", "env"}                 # Amendment 1
fx._SAFE_VERBS = _SAFE_V4
_row_v3 = fx.row


def row(key: str, cell: dict) -> dict:
    fx._SAFE_VERBS = _SAFE_V4B                     # 4b's replay, scored first ...
    prov_4b = _row_v3(key, cell)["provenance"]
    fx._SAFE_VERBS = _SAFE_V4                      # ... then v4 exactly as registered
    j = _row_v3(key, cell)
    j["provenance_4b"] = prov_4b
    j["verbatim_v3"] = j["verbatim"]
    j["delivered"] = bool(j["file"] and j["sections"] >= fx.CONTRACT and j["caller_read"]
                          and j["provenance"] is True)
    # delivery-fix-4b (Amendment 1): provenance also holds when the file equals its appends
    # exactly -- no other write can have left a trace -- and read-only utilities replay.
    j["delivered_4b"] = bool(j["file"] and j["sections"] >= fx.CONTRACT and j["caller_read"]
                             and (j["verbatim"] or prov_4b is True))
    return j


fx.row = row
fx.HERE, fx.RAW = HERE, HERE / "raw"
_self_test_v3 = fx.self_test


def self_test() -> int:
    rc = _self_test_v3()
    py = ("F=\"x.md\"\npython3 - <<'PYEOF'\nfor line in open('x.md'): pass\nwith open('x.md','w') as f: f.write('y')\nPYEOF")
    checks = {
        "a Python heredoc edit contributes only 'F' and 'python3' as command words":
            _verbs(py) == {"F", "python3"},
        "an unlisted command is still refused":
            not (_verbs("F=\"x\"\ncurl http://example.com") <= _SAFE_V4B | {""}),
        "v4 as registered does not admit readlink; 4b does":
            "readlink" not in _SAFE_V4 and "readlink" in _SAFE_V4B,
    }
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    ok = rc == 0 and all(checks.values())
    print(f"delivery-fix-4 --self-test: {'PASS' if ok else 'FAIL'} ({len(checks)} added controls)")
    return 0 if ok else 1


fx.self_test = self_test
_read_v3 = fx.cmd_read
PRE_4B = {"TB-02.r1", "TB-02.r2", "TB-02.r3"}   # observed before Amendment 1's commit
MIN_4B = 9


def cmd_read() -> int:
    rc = _read_v3()
    import json
    cells = json.loads((HERE / "cells.json").read_text())
    rows = {k: row(k, v) for k, v in cells.items() if v["outcome"] == "scored" and k not in PRE_4B}
    ok = [k for k, r in rows.items() if r["delivered_4b"]]
    verdict = ("OPERATIONAL" if len(rows) >= MIN_4B and len(ok) == len(rows) else "NOT OPERATIONAL")
    print(f"4b (prospective, Amendment 1)  delivered {len(ok)}/{len(rows)}  VERDICT-4B  {verdict}")
    return rc


fx.cmd_read = cmd_read

if __name__ == "__main__":
    sys.exit(fx.main())
