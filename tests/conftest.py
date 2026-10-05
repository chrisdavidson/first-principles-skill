"""Run every test against source, never a cached .pyc.

CPython trusts a __pycache__ entry whose recorded source mtime (whole seconds)
and size match the file. A same-size edit made within the second -- the
mutate-run-restore probes these tests are checked with -- can then be served
stale bytecode in either direction: the mutation unseen, or the restored file
read as still mutated. Disabling writes alone still READS a stale entry, so the
cache is also redirected to an empty per-session directory. The environment
variables carry both settings to the scripts these tests run as subprocesses.

scripts/check-firewall-battery.sh and both pre-commit hooks apply the same
isolation to everything they run.
"""

from __future__ import annotations

import atexit
import os
import shutil
import sys
import tempfile

_PYCACHE_DIR = tempfile.mkdtemp(prefix="fp-pytest-pycache-")
atexit.register(shutil.rmtree, _PYCACHE_DIR, ignore_errors=True)

sys.dont_write_bytecode = True
sys.pycache_prefix = _PYCACHE_DIR
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = _PYCACHE_DIR
