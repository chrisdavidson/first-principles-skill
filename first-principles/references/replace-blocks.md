<!-- GENERATED — DO NOT EDIT. Source: shared/spine/references/replace-blocks.md. Regenerate via: scripts/sync-content.py --write. -->

# Replacement blocks

> **Scope:** the correct-by-appending applier. Step 4 of *Deliver the analysis as a file*
> extracts the awk program below and runs it over `<path>.answer`, `<path>` and
> `<path>.process` concatenated, in that order. The agent never opens this file with Read;
> the contract below is the specification the program implements.

## Contract

The working files are append-only, so a block already appended is never rewritten in place.
A correction is appended as a replacement block, and step 4 swaps it in when it assembles.

- A replacement block's first line is `## Replace: <heading text>`, where the text is the
  existing heading exactly as written, without its leading `#` characters. The next line is
  the corrected heading line, followed by its full corrected content.
- The target is that heading through the next heading of the same or higher level. Only `##`
  and `###` headings can be targets, and the replacement opens a heading of the same level.
- The replacement's own text runs to the next `#` or `##` heading line, which in practice is
  the next appended block or the next marker. A `###` replacement may therefore carry further
  `###` blocks after its first heading, which is how a chain is added.
- Replacements apply in file order. A later one for the same heading wins, including one that
  targets a heading an earlier replacement introduced.
- Several blocks may share one heredoc, so the corrections one check finds go in one call.
- Lines inside a fenced code block are never headings or markers.
- A `## Withdraw: <text>` line cancels every earlier `## Replace: <text>` block with that
  text. It is the only recovery for a refused replacement, because the working files are
  append-only.
- A Withdraw naming no earlier replacement does not refuse. It prints
  `WARNING: withdraw matched nothing: <text>` on stderr and assembly continues, so a mistyped
  Withdraw is harmless and is fixed by appending a correct one.
- Both markers are consumed. The assembled file carries no `## Replace:` or `## Withdraw:`
  line.

## Refusals and recovery

Assembly that cannot proceed prints `NOT ASSEMBLED: ...` on stderr, writes nothing, and exits
non-zero; `<path>.answer` and `<path>.process` stay in place.

The four refusals a replacement block causes are: a target that matches no heading, a target
that matches more than one heading, a target heading of another level than the replacement,
and a marker not followed by a `##` or `###` heading line. Each is decided only after Withdraw
lines are processed, and each is cleared the same way: append `## Withdraw: <the text the
message quotes>`, copied from the message rather than retyped, then a corrected block if the
correction is still wanted, then re-issue step 4.

A refusal for a code fence that is never closed above a marker is not cleared by a Withdraw,
because every line under an unclosed fence, a Withdraw included, is fenced text. Append a line
of exactly three backticks to close it, then a Withdraw for the replacement block whose
content opened the fence if one did, then re-append any correction that sat inside the fence
(those marker lines are now literal fenced text and are not applied). The recovery is the same
whether the fence was opened inside a replacement block or inside an appended section.

## The program

```awk
# Apply every "## Replace: <heading>" block, and every "## Withdraw: <text>" line, in the text read.
# Reads stdin or files; writes the assembled text to stdout, or prints NOT ASSEMBLED: to stderr and writes nothing.
# A fence line is one that starts with three backticks; a heading is a "#" line outside a fence.
function lvl(s,   c) {
  c = 0
  while (substr(s, c + 1, 1) == "#") c++
  if (c < 1 || c > 6 || substr(s, c + 1, 1) != " ") return 0
  return c
}
function htext(s,   t) { t = substr(s, lvl(s) + 2); sub(/[ \t\r]+$/, "", t); return t }
function mark(   i, f) {
  f = 0; fstart = 0
  for (i = 1; i <= m; i++) {
    if (substr(C[i], 1, 3) == FENCE) { f = !f; H[i] = 0; if (f) fstart = i; continue }
    H[i] = f ? 0 : lvl(C[i])
  }
  return f
}
function die(msg) { print "NOT ASSEMBLED: " msg > "/dev/stderr"; exit 1 }
BEGIN { FENCE = "\140\140\140"; PFX = "Replace: "; WPFX = "Withdraw: " }
{ L[++n] = $0 }
END {
  for (i = 1; i <= n; i++) C[i] = L[i]
  m = n
  if (mark()) {
    for (i = fstart; i <= m; i++)
      if (substr(C[i], 1, 3) == "## " && (substr(C[i], 4, length(PFX)) == PFX || substr(C[i], 4, length(WPFX)) == WPFX)) die("a code fence opened at line " fstart " is never closed above the marker '" substr(C[i], 4) "' - append a line of three backticks, withdraw the block that opened it if one did, re-append what sat inside it, then re-issue")
  }
  nb = 0; nr = 0; i = 1
  while (i <= m) {
    if (H[i] == 2 && substr(htext(C[i]), 1, length(WPFX)) == WPFX) {
      W = substr(htext(C[i]), length(WPFX) + 1)
      wn = 0
      for (r = 1; r <= nr; r++) if (T[r] == W && !X[r]) { X[r] = 1; wn++ }
      if (wn == 0) print "WARNING: withdraw matched nothing: " W > "/dev/stderr"
      i += 1
    } else if (H[i] == 2 && substr(htext(C[i]), 1, length(PFX)) == PFX) {
      T[++nr] = substr(htext(C[i]), length(PFX) + 1)
      j = i + 1; h = (j <= m) ? H[j] : 0
      BAD[nr] = (h < 2 || h > 3 || substr(htext(C[j]), 1, length(PFX)) == PFX || substr(htext(C[j]), 1, length(WPFX)) == WPFX) ? "replacement for '" T[nr] "' does not start with a ## or ### heading line" : ""
      k = (j <= m && h != 1) ? j + 1 : j
      while (k <= m && !(H[k] >= 1 && H[k] <= 2)) k++
      RS_[nr] = rn + 1
      for (q = j; q < k; q++) R[++rn] = C[q]
      RE_[nr] = rn; RH[nr] = h
      i = k
    } else { B[++nb] = C[i]; i++ }
  }
  for (r = 1; r <= nr; r++) if (!X[r] && BAD[r] != "") die(BAD[r])
  for (i = 1; i <= nb; i++) C[i] = B[i]
  for (i = nb + 1; i <= m; i++) delete C[i]
  m = nb
  for (r = 1; r <= nr; r++) {
    if (X[r]) continue
    mark(); cnt = 0
    for (i = 1; i <= m; i++) if (H[i] > 0 && htext(C[i]) == T[r]) { cnt++; at = i }
    if (cnt == 0) die("no heading matches '" T[r] "'")
    if (cnt > 1) die(cnt " headings match '" T[r] "'")
    if (H[at] != RH[r]) die("the replacement for '" T[r] "' opens a level-" RH[r] " heading but the target is level " H[at])
    e = at + 1
    while (e <= m && !(H[e] >= 1 && H[e] <= H[at])) e++
    nn = 0
    for (i = 1; i < at; i++) N2[++nn] = C[i]
    for (q = RS_[r]; q <= RE_[r]; q++) N2[++nn] = R[q]
    for (i = e; i <= m; i++) N2[++nn] = C[i]
    for (i = 1; i <= nn; i++) C[i] = N2[i]
    for (i = nn + 1; i <= m; i++) delete C[i]
    m = nn
  }
  for (i = 1; i <= m; i++) print C[i]
}
```
