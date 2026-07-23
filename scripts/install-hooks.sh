#!/usr/bin/env bash
# Idempotent installer that symlinks scripts/git-hooks/pre-commit into
# .git/hooks/pre-commit. Preserves any prior hook as .git/hooks/pre-commit.bak
# on first run; refuses to overwrite if a .bak already exists.
#
# HOOK-04 + D-05. Cwd-agnostic: re-runs from anywhere inside the working tree.

set -euo pipefail

# Move to repo root.
if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    echo "install-hooks: not inside a git working tree" >&2
    exit 1
fi
cd "$REPO_ROOT"

HOOK_SRC_REL="../../scripts/git-hooks/pre-commit"
HOOK_DST=".git/hooks/pre-commit"
HOOK_BAK=".git/hooks/pre-commit.bak"

# Sanity-check the source hook is present in the worktree.
if [[ ! -f scripts/git-hooks/pre-commit ]]; then
    echo "install-hooks: source hook scripts/git-hooks/pre-commit not found" >&2
    exit 1
fi

# Defensive: ensure the source hook is executable. Task 1 already chmods it,
# but a fresh clone or an editor strip could clear the bit.
chmod +x scripts/git-hooks/pre-commit

# Already installed (correct symlink)? Idempotent no-op.
if [[ -L "$HOOK_DST" && "$(readlink "$HOOK_DST")" == "$HOOK_SRC_REL" ]]; then
    echo "install-hooks: already installed"
    exit 0
fi

# Existing non-our hook (regular file, wrong symlink, or broken symlink).
if [[ -e "$HOOK_DST" || -L "$HOOK_DST" ]]; then
    if [[ -e "$HOOK_BAK" || -L "$HOOK_BAK" ]]; then
        echo "install-hooks: refusing to overwrite $HOOK_DST -- $HOOK_BAK already exists; resolve manually" >&2
        exit 1
    fi
    mv "$HOOK_DST" "$HOOK_BAK"
    echo "install-hooks: preserved prior hook as $HOOK_BAK"
fi

# Create the relative symlink.
ln -s "$HOOK_SRC_REL" "$HOOK_DST"
echo "install-hooks: symlinked $HOOK_DST -> $HOOK_SRC_REL"

# Warn if core.hooksPath is set -- Git will ignore .git/hooks/ in that case.
if HOOKS_PATH="$(git config --get core.hooksPath 2>/dev/null)"; then
    {
        echo "install-hooks: WARNING -- 'core.hooksPath' is set to '${HOOKS_PATH}'."
        echo "  Git will use that path and IGNORE $HOOK_DST."
        echo "  To activate this installer's hook, run: git config --unset core.hooksPath"
        echo "  (Or skip this installer and manually add the sync-drift check into your custom hooks path.)"
    } >&2
fi

exit 0
