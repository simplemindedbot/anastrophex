# Failure Pattern: Virtual Environment Using Wrong Python

**Observed:** Oct 23, 2025 - anastrophex development setup

## Behavior

1. Create venv with `python -m venv .venv`
2. Install package with `pip install -e ".[dev]"`
3. Package installs successfully, shows in `pip list`
4. Import fails: `ModuleNotFoundError: No module named 'package'`
5. .pth file exists in site-packages but path not added to sys.path
6. Running same command multiple times produces same error
7. Manually adding path with `site.addsitedir()` works

## Root Cause

The venv was created using uv's Python distribution instead of mise's Python:
- `which python` showed pyenv shim
- But venv symlink pointed to `/Users/sc/.local/share/uv/python/cpython-3.12.11-macos-aarch64-none/bin/python3.12`
- uv's Python has known .pth file processing issues (GitHub issues #10900, #11671, #12047)
- mise's Python is at `/Users/sc/.local/share/mise/installs/python/3.12.11/bin/python3`

## Trigger Conditions

```
IF editable install completes without error
   AND package appears in `pip list`
   AND import fails with ModuleNotFoundError
   AND .pth file exists in site-packages
   AND path in .pth file is valid (os.path.exists returns True)
   AND manually adding path works (site.addsitedir)
THEN: Likely using wrong Python distribution
```

## Effective Intervention

**Timing:** After seeing "package installed but can't import"

**Diagnostic steps:**
```bash
# Check which Python the venv is using
readlink .venv/bin/python
ls -la .venv/bin/python

# Check where mise's Python is
mise where python

# Compare the two paths
```

**Reminder:**
```
⚠️ Package installs but won't import - check Python distribution

When using mise:
1. Don't rely on `python` in PATH (might be pyenv/uv)
2. Use mise's Python explicitly: $(mise where python)/bin/python3 -m venv .venv
3. Or: Use mise's venv command if available

Check: readlink .venv/bin/python
Should point to: /Users/sc/.local/share/mise/installs/python/VERSION/...
NOT to: /Users/sc/.local/share/uv/python/...
```

## Solution Applied

```bash
# Remove old venv
rm -rf .venv

# Create venv with mise's Python directly
/Users/sc/.local/share/mise/installs/python/3.12.11/bin/python3 -m venv .venv

# Or use mise command:
# $(mise where python)/bin/python3 -m venv .venv

# Install package
.venv/bin/pip install -e ".[dev]"

# Verify it works
.venv/bin/python -c "import package; print('✅ Success')"
```

**Result:** Import works, tests pass

## Detection Pattern for Anastrophex

```python
pattern_signature = "venv-wrong-python"

def detect(tool_history):
    # Look for sequence:
    # 1. pip install -e succeeded
    # 2. Import failed with ModuleNotFoundError
    # 3. Same import tried 2+ times with same error
    # 4. No fix attempted (no venv recreation, no path changes)

    if has_sequence(tool_history, [
        "pip install -e . succeeded",
        "python -c import X failed",
        "python -c import X failed again",
    ]):
        # Check if .pth file exists
        if pth_file_exists_for_package():
            return True
    return False
```

## Why This Happens

**Multiple Python version managers:**
- pyenv (older, user may have used before)
- mise (current, recommended)
- uv (fast, often installed alongside)

**PATH precedence:**
- Shell might have pyenv shims first
- `python` command may not resolve to mise's Python
- `python -m venv` uses whatever `python` resolves to

**uv-specific issues:**
- uv bundles Python distributions for speed
- Known .pth file processing bugs (as of Jan-Mar 2025)
- Silent failures - no error messages, just doesn't work

## Prevention

**Always be explicit with Python path when using mise:**

```bash
# DON'T (ambiguous)
python -m venv .venv

# DO (explicit)
$(mise where python)/bin/python3 -m venv .venv
```

**Or configure mise to handle venv:**

```toml
# .mise.toml
[tools]
python = "3.12.11"

[env]
_.python.venv = { path = ".venv", create = true }
```

## Related Issues

- uv GitHub issue #10900: "uv ignored .pth files in package" (Jan 2025)
- uv GitHub issue #11671: "Corrupt .pth in site-packages" (Feb 2025)
- uv GitHub issue #12047: "uv uses stale project pth file" (Mar 2025)

## Learning

**For anastrophex:**
- This is a meta-pattern: "wrong tool/version being used"
- Similar to "wrong Python version" or "wrong venv activated"
- Diagnostic: "Tool reports success but operation fails"
- Key signal: Same error repeats despite "successful" fix attempts

**Broader pattern:**
- When standard operations fail silently
- Check which version/installation of the tool is actually being used
- PATH and shell configuration matter
- Explicit paths > relying on shell resolution
