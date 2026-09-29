#!/usr/bin/env python3
"""regression-rerun-2 -- re-run software-systems-2 on rerun-fixes-2 (docs/regression-rerun-protocol.md §2).

    python3 tests/regression-rerun-2/run.py run --body <wt>/first-principles --cwd <empty dir>
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location("_er2", ROOT / "tests/example-rerun/run_examples.py")
er = importlib.util.module_from_spec(spec)
sys.modules["_er2"] = er
spec.loader.exec_module(er)

er.PROMPTS = {f"software-systems-2.r{r}": er.PROMPTS["software-systems-2"] for r in (1, 2)}
er.HERE, er.RAW, er.DOCS = HERE, HERE / "raw", HERE / "documents"

if __name__ == "__main__":
    sys.exit(er.main())
