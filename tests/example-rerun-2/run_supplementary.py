#!/usr/bin/env python3
"""example-rerun-2 supplementary -- one more run for each example whose first run skipped the
agent's procedure (no template read, no file). Same transport and body as run_examples.py; the
result is recorded under '<name>.supp' beside the first run, which stays the registered reading.

    python3 tests/example-rerun-2/run_supplementary.py --body <dir>/first-principles --cwd <empty dir>
"""
import argparse, importlib.util, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("_er2", HERE / "run_examples.py")
er = importlib.util.module_from_spec(spec)
sys.modules["_er2"] = er
spec.loader.exec_module(er)

SKIPPED = ("decompose-irreducibility", "personal-general-2", "product-business")

ap = argparse.ArgumentParser()
ap.add_argument("--body", type=Path, required=True)
ap.add_argument("--cwd", type=Path, required=True)
a = ap.parse_args()
er.PROMPTS = {f"{n}.supp": er.PROMPTS[n] for n in SKIPPED}
sys.exit(er.run(a.body.resolve(), a.cwd.resolve()))
