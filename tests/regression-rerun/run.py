#!/usr/bin/env python3
"""regression-rerun -- re-run the examples whose re-runs regressed, on the rerun-fixes body.

    python3 tests/regression-rerun/run.py run --body <wt>/first-principles --cwd <empty dir>

Protocol: docs/regression-rerun-protocol.md. Reuses tests/example-rerun/run_examples.py's
transport, capture and prompts (unchanged), two runs per affected example.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location("_er", ROOT / "tests/example-rerun/run_examples.py")
er = importlib.util.module_from_spec(spec)
sys.modules["_er"] = er
spec.loader.exec_module(er)

AFFECTED = ("science-engineering", "software-systems-2", "theoretical-limit-carnot",
            "personal-general-2")
REPEATS = (1, 2)
er.PROMPTS = {f"{n}.r{r}": er.PROMPTS[n] for n in AFFECTED for r in REPEATS}
er.HERE, er.RAW, er.DOCS = HERE, HERE / "raw", HERE / "documents"

if __name__ == "__main__":
    sys.exit(er.main())
