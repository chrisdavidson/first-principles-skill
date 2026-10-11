#!/usr/bin/env python3
"""SubagentStop guard for the first-principles agent (backlog 999.196).

The agent sometimes stops without running its procedure: it answers inline
with no tool call, answers from web searches alone, or invokes a skill and
loses the procedure. Its deliverable is a file, so a run that wrote no file is
a skipped run whatever its final message says. This hook reads the agent's own
transcript, finds the analysis file it created, and refuses the stop -- telling
the agent what is missing -- until that file is assembled (its first `## `
heading is `## Answer` and no `## Replace:`/`## Withdraw:` marker survives outside a
code fence) and the Markdown reader report beside it exists.

It blocks at most MAX_BLOCKS times per agent run, then lets the stop through,
so a run that genuinely cannot deliver (Bash denied, say) is never trapped.
Any error inside the hook fails open: a broken guard must never break the
agent it guards.

Usage as a hook: reads the SubagentStop JSON on stdin.
Self-test: `python3 delivery-guard.py --self-test`.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

AGENT_TYPES = frozenset({"first-principles:first-principles", "first-principles"})
MAX_BLOCKS = 2
# Matched suffix-first, then the directory prefix is walked back by hand: a
# leading `[^\s]*/` group backtracks quadratically on long whitespace-free tool
# results (base64, minified JSON) and hung the hook on real transcripts.
_ANALYSIS_RE = re.compile(r"\.first-principles/analysis-\d{8}T\d{6}Z\.md")
_PATH_STOP = frozenset(" \t\r\n\"'`<>|;&()=")


def _strings(value):
    """Yield every string nested anywhere in a JSON value."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _strings(v)


def analysis_paths(transcript: Path) -> list[str]:
    """Analysis-file paths named in the agent's tool calls and tool results.

    Only tool_use inputs and tool_result contents are read, never prompt or
    prose text, so a path merely mentioned in the task does not count.
    """
    found: list[str] = []
    with transcript.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            content = (entry.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    payload = block.get("input")
                elif block.get("type") == "tool_result":
                    payload = block.get("content")
                else:
                    continue
                for text in _strings(payload):
                    for m in _ANALYSIS_RE.finditer(text):
                        start = m.start()
                        while start > 0 and text[start - 1] not in _PATH_STOP:
                            start -= 1
                        path = text[start : m.end()]
                        if not path.startswith(("/", ".first-principles/")):
                            path = path[path.find(".first-principles/") :]
                        if path not in found:
                            found.append(path)
    return found


def surviving_marker(analysis: Path) -> str | None:
    """First `## Replace: ` or `## Withdraw: ` line outside a code fence, else None."""
    fenced = False
    with analysis.open(encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            if ln.startswith("```"):
                fenced = not fenced
            elif not fenced and ln.startswith(("## Replace: ", "## Withdraw: ")):
                return ln.rstrip("\n")
    return None


def delivery_problem(transcript: Path, cwd: Path) -> str | None:
    """None when the run delivered; otherwise what is missing, in one line."""
    paths = analysis_paths(transcript)
    if not paths:
        return (
            "you have not created the analysis file -- no "
            "`.first-principles/analysis-<UTC>.md` appears in any of your tool calls"
        )
    for raw in reversed(paths):
        analysis = Path(raw) if os.path.isabs(raw) else cwd / raw
        if not analysis.is_file():
            continue
        first_h2 = next(
            (
                ln.rstrip("\n")
                for ln in analysis.open(encoding="utf-8", errors="replace")
                if ln.startswith("## ")
            ),
            None,
        )
        if first_h2 != "## Answer":
            return (
                f"`{raw}` exists but is not assembled (its first `## ` heading is "
                f"{first_h2!r}, not '## Answer') -- finish steps 2-5 of *Deliver the "
                "analysis as a file*"
            )
        survivor = surviving_marker(analysis)
        if survivor is not None:
            return (
                f"`{raw}` is not assembled: the line {survivor!r} survives -- re-issue "
                "step 4 of *Deliver the analysis as a file*; it applies replacement blocks"
            )
        report = analysis.with_name(analysis.name.replace("analysis-", "report-", 1))
        if not report.is_file():
            return (
                f"`{raw}` is assembled but the reader report `{report.name}` beside it "
                "does not exist -- run step 6 of *Deliver the analysis as a file* and "
                "the steps after it"
            )
        return None
    return f"`{paths[-1]}` was named in your tool calls but does not exist on disk"


def agent_transcript(data: dict) -> Path | None:
    """The stopping agent's own transcript, never the parent session's.

    Uses `agent_transcript_path` when the event carries it; otherwise derives
    `<session dir>/subagents/agent-<agent_id>.jsonl` from the parent's
    `transcript_path`, which is where Claude Code keeps a subagent's turns.
    """
    raw = data.get("agent_transcript_path")
    if raw and Path(raw).is_file():
        return Path(raw)
    parent, agent_id = data.get("transcript_path"), data.get("agent_id")
    if parent and agent_id:
        p = Path(parent)
        derived = p.with_suffix("") / "subagents" / f"agent-{agent_id}.jsonl"
        if derived.is_file():
            return derived
    return None


def _block_count_file(data: dict) -> Path:
    key = re.sub(
        r"[^A-Za-z0-9_-]",
        "_",
        f"{data.get('session_id', '')}-{data.get('agent_id', '')}",
    )
    return Path(tempfile.gettempdir()) / f"fp-delivery-guard-{key}.count"


def decide(data: dict) -> dict | None:
    """The hook's JSON reply, or None to let the stop through."""
    if data.get("agent_type") not in AGENT_TYPES:
        return None
    transcript = agent_transcript(data)
    if transcript is None:
        return None
    cwd = Path(data.get("cwd") or os.getcwd())
    problem = delivery_problem(transcript, cwd)
    counter = _block_count_file(data)
    if problem is None:
        counter.unlink(missing_ok=True)
        return None
    blocks = int(counter.read_text()) if counter.is_file() else 0
    if blocks >= MAX_BLOCKS:
        counter.unlink(missing_ok=True)
        return None
    counter.write_text(str(blocks + 1))
    return {
        "decision": "block",
        "reason": (
            "Do not stop yet: " + problem + ". Your deliverable is the analysis FILE, "
            "not your final message -- an answer in chat, from web searches, or from a "
            "skill is not a delivery. Do not invoke any skill. Run the procedure in your "
            "own instructions now: Phases 1-5, written to the file one section per Bash "
            "call as *Deliver the analysis as a file* prescribes, then the reader report, "
            "then the short pointer message. "
            f"(first-principles delivery guard, block {blocks + 1} of {MAX_BLOCKS})"
        ),
    }


# --------------------------------------------------------------------- self-test


def _self_test() -> int:
    import shutil

    failures: list[str] = []

    def check(label: str, cond: bool) -> None:
        print(f"delivery-guard --self-test: {label} {'PASS' if cond else 'FAIL'}")
        if not cond:
            failures.append(label)

    def tool_line(kind: str, payload) -> str:
        if kind == "use":
            block = {"type": "tool_use", "name": "Bash", "input": {"command": payload}}
            role = "assistant"
        else:
            block = {"type": "tool_result", "content": payload}
            role = "user"
        return json.dumps({"type": role, "message": {"role": role, "content": [block]}})

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        stamp = "20261009T120000Z"
        rel = f".first-principles/analysis-{stamp}.md"
        prompt = json.dumps(
            {
                "type": "user",
                "message": {"role": "user", "content": f"Earlier run wrote {rel}."},
            }
        )

        def run(name: str, lines: list[str], files: dict[str, str]) -> dict | None:
            cwd = root / name
            (cwd / ".first-principles").mkdir(parents=True)
            for fname, body in files.items():
                (cwd / ".first-principles" / fname).write_text(body)
            transcript = cwd / "agent.jsonl"
            transcript.write_text("\n".join(lines) + "\n")
            data = {
                "hook_event_name": "SubagentStop",
                "agent_type": "first-principles:first-principles",
                "agent_transcript_path": str(transcript),
                "cwd": str(cwd),
                "session_id": f"selftest-{name}",
                "agent_id": "a1",
            }
            _block_count_file(data).unlink(missing_ok=True)
            reply = decide(data)
            _block_count_file(data).unlink(missing_ok=True)
            return reply

        created = [
            tool_line("use", "mkdir -p .first-principles && ..."),
            tool_line("result", rel),
        ]
        assembled = "## Answer\n\nx\n\n## 1. Essence\n"
        report = "# Title\n"

        # Positive control: an assembled file plus its report lets the stop through.
        check(
            "C01 delivered run passes",
            run(
                "c01",
                created,
                {f"analysis-{stamp}.md": assembled, f"report-{stamp}.md": report},
            )
            is None,
        )
        # Zero-tool skip (product-business): no tool call at all.
        r = run("c02", [prompt], {})
        check("C02 zero-tool run blocked", bool(r) and r["decision"] == "block")
        # The prompt naming a path is not a delivery: prose is never read.
        check(
            "C03 path in prompt prose not counted",
            bool(r) and "not created" in r["reason"],
        )
        # Web-only skip: tool calls, none creating the file.
        r = run(
            "c04",
            [tool_line("use", "curl example.org"), tool_line("result", "<html>")],
            {},
        )
        check("C04 web-only run blocked", bool(r) and "not created" in r["reason"])
        # Created but never assembled.
        r = run("c05", created, {f"analysis-{stamp}.md": "## 1. Essence\n"})
        check(
            "C05 unassembled file blocked", bool(r) and "not assembled" in r["reason"]
        )
        # Assembled but no reader report.
        r = run("c06", created, {f"analysis-{stamp}.md": assembled})
        check("C06 missing report blocked", bool(r) and "reader report" in r["reason"])
        # Named but absent on disk.
        r = run("c07", created, {})
        check(
            "C07 named-but-absent file blocked",
            bool(r) and "does not exist" in r["reason"],
        )

        # A replacement marker that survives assembly means step 4 did not apply it.
        r = run(
            "c14",
            created,
            {
                f"analysis-{stamp}.md": assembled + "## Replace: X\n## X\n",
                f"report-{stamp}.md": report,
            },
        )
        check(
            "C14 surviving Replace marker blocked",
            bool(r) and "survives" in r["reason"] and "not assembled" in r["reason"],
        )
        r = run(
            "c15",
            created,
            {
                f"analysis-{stamp}.md": assembled + "## Withdraw: X\n",
                f"report-{stamp}.md": report,
            },
        )
        check(
            "C15 surviving Withdraw marker blocked",
            bool(r) and "survives" in r["reason"],
        )
        check(
            "C16 fenced marker passes",
            run(
                "c16",
                created,
                {
                    f"analysis-{stamp}.md": assembled
                    + "```\n## Replace: X\n## Withdraw: X\n```\n",
                    f"report-{stamp}.md": report,
                },
            )
            is None,
        )

        # Another agent type is never blocked.
        cwd = root / "c08"
        cwd.mkdir()
        (cwd / "t.jsonl").write_text(prompt + "\n")
        check(
            "C08 other agent type ignored",
            decide(
                {
                    "agent_type": "general-purpose",
                    "agent_transcript_path": str(cwd / "t.jsonl"),
                    "cwd": str(cwd),
                }
            )
            is None,
        )

        # Bounded: the third stop of a non-delivering run goes through.
        data = {
            "agent_type": "first-principles",
            "agent_transcript_path": str(cwd / "t.jsonl"),
            "cwd": str(cwd),
            "session_id": "selftest-bound",
            "agent_id": "a1",
        }
        _block_count_file(data).unlink(missing_ok=True)
        seq = [decide(data) for _ in range(MAX_BLOCKS + 1)]
        check(
            "C09 at most MAX_BLOCKS blocks, then the stop goes through",
            all(s and s["decision"] == "block" for s in seq[:MAX_BLOCKS])
            and seq[-1] is None,
        )

        # An absolute path printed by the shell resolves as well.
        abs_dir = root / "c10"
        (abs_dir / ".first-principles").mkdir(parents=True)
        (abs_dir / ".first-principles" / f"analysis-{stamp}.md").write_text(assembled)
        (abs_dir / ".first-principles" / f"report-{stamp}.md").write_text(report)
        t = abs_dir / "t.jsonl"
        t.write_text(tool_line("result", str(abs_dir / rel)) + "\n")
        check(
            "C10 absolute path resolves",
            decide(
                {
                    "agent_type": "first-principles:first-principles",
                    "agent_transcript_path": str(t),
                    "cwd": "/nonexistent",
                }
            )
            is None,
        )

        # Linear time on a long whitespace-free tool result (the quadratic
        # regex this replaced hung on real transcripts).
        import time

        big = root / "c13.jsonl"
        big.write_text(tool_line("result", "A" * 2_000_000 + "/" + rel) + "\n")
        t0 = time.monotonic()
        hit = analysis_paths(big)
        check(
            "C13 2 MB whitespace-free result scanned in under 2 s",
            time.monotonic() - t0 < 2.0 and hit == [rel],
        )

        # The real captures, when run from the repository: one delivered run must
        # pass and every recorded skip mode must be blocked.
        repo_raw = Path(__file__).resolve().parents[2] / "tests" / "pointer-fix" / "raw"
        if repo_raw.is_dir():

            def capture(name: str) -> dict | None:
                agent_dir = repo_raw / f"{name}.a1.agent"
                transcript = next(agent_dir.glob("*.jsonl"))
                cwd = root / f"cap-{name}"
                files = repo_raw / f"{name}.a1.files"
                if files.is_dir():
                    shutil.copytree(files, cwd / ".first-principles")
                else:
                    cwd.mkdir()
                data = {
                    "agent_type": "first-principles:first-principles",
                    "agent_transcript_path": str(transcript),
                    "cwd": str(cwd),
                    "session_id": f"selftest-cap-{name}",
                    "agent_id": "a1",
                }
                _block_count_file(data).unlink(missing_ok=True)
                reply = decide(data)
                _block_count_file(data).unlink(missing_ok=True)
                return reply

            check(
                "C11 capture estimate-fermi (delivered) passes",
                capture("estimate-fermi") is None,
            )
            for name, mode in (
                ("product-business", "zero-tool"),
                ("decompose-irreducibility", "web-only"),
                ("science-engineering-2", "Skill-first"),
                ("self-application", "Skill-first"),
            ):
                r = capture(name)
                check(
                    f"C12 capture {name} ({mode} skip) blocked",
                    bool(r) and r["decision"] == "block",
                )
        else:
            print(
                "delivery-guard --self-test: captures not present (installed copy) -- C11/C12 skipped"
            )

    if failures:
        print(f"delivery-guard --self-test: FAIL ({len(failures)}): {failures}")
        return 1
    print("delivery-guard --self-test: PASS")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--self-test"]:
        return _self_test()
    try:
        data = json.load(sys.stdin)
        reply = decide(data)
        log = os.environ.get("FP_GUARD_LOG")
        if log:  # diagnostics only: what the event carried and what was decided
            with open(log, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"event": data, "reply": reply}) + "\n")
    except Exception as exc:  # noqa: BLE001 -- fail open: never break the agent this guards
        sys.stderr.write(f"first-principles delivery guard: skipped ({exc})\n")
        return 0
    if reply is not None:
        print(json.dumps(reply))
    return 0


if __name__ == "__main__":
    sys.exit(main())
