<!--
Thanks for contributing to Voice-Pro. Keep the change as small as it can
usefully be - one problem per pull request reviews far faster than five.
-->

## What this changes

<!-- One or two sentences. What is different after this PR? -->

## Why

<!--
The concrete problem, not the abstract one.

If it is a bug fix: what input or condition produces the wrong behaviour, and
what does the user actually see? Paste the traceback or the wrong output.

If it is an enhancement: what could you not do before?
-->

## How it was verified

<!--
Say what you ran, not just that it works. For example:

  - python -m compileall -q app src
  - ruff check app src --select E9,F63,F7,F82
  - transcribed a 3-minute mp4 with faster-whisper, .srt timings checked
  - before/after output for the affected function

If you could not test something (no NVIDIA GPU, no Azure key, no macOS),
say so here rather than leaving it implied.
-->

## Scope

- [ ] Touches only the files needed for this one change
- [ ] No unrelated reformatting, renaming, or import reordering
- [ ] Existing behaviour is unchanged for inputs that already worked, or the
      change in behaviour is described above

## Platforms

<!-- Tick what you actually ran it on. -->

- [ ] Windows
- [ ] Linux
- [ ] macOS
- [ ] NVIDIA GPU path
- [ ] CPU-only path

## Related issues

<!-- e.g. Fixes #123 -->
