# Contributing to Voice-Pro

Thanks for taking the time. This file covers the things that are specific to this
project — the general "fork, branch, PR" mechanics work the way you expect.

## Before you start

**Open an issue first for anything non-trivial.** A bug fix with a clear reproduction
can go straight to a PR. A new tab, a new backend, or a change to how models are
downloaded is worth a short discussion first, so nobody spends a weekend on something
that does not fit.

## Setting up

Use the launcher for your platform rather than installing dependencies by hand — it
creates the conda environment the app expects:

```
Windows      start.bat
Linux/macOS  ./start.sh
```

`configure.bat` (Windows) installs the system-level prerequisites — Chocolatey, ffmpeg,
CUDA, Visual Studio build tools.

Two things that catch people out:

- **`.sh` files must keep LF line endings** and `.bat` files CRLF. `.gitattributes`
  enforces this; if you edit a shell script on Windows, check your editor has not
  converted it.
- **Never commit `.env`.** Azure keys live there. `.env.example` is the template that
  belongs in git.

## Making a change

**One concern per pull request.** A 20-line fix with a clear reproduction gets reviewed;
a 400-line change that fixes a bug *and* renames things *and* reformats a file waits.
If you find three problems, that is three PRs.

**Do not reformat code you are not changing.** Whitespace churn hides the real diff.

**Match the surrounding style.** This codebase has conventions worth preserving:

- log through `structlog` (`logger = structlog.get_logger()`), with the
  `[filename.py] function_name - message` prefix used throughout
- return `True`/`False` from helpers and let callers branch on truthiness
- keep Korean comments where they exist; add English ones alongside if it helps

**Watch out for star imports.** Many modules do `from app.abus_path import *`, so an
import that looks unused in one file may be re-exported to another. Do not delete
imports on a linter's say-so without checking who star-imports the module.

## Before you push

The CI workflow runs these; running them locally first saves a round trip:

```
python -m compileall -q app src one_click.py start-abus.py start-voice.py
ruff check app src one_click.py start-abus.py start-voice.py --select E9,F63,F7,F82
bash -n start.sh update.sh configure.sh uninstall.sh
```

The `ruff` selection is deliberately narrow — syntax errors, invalid comparisons, and
undefined names. There is no style gate, so you will not be blocked over formatting.

## Writing the pull request

The PR template asks for four things; the one that matters most is **how you verified
it**. Say what you actually ran. This project spans Windows and POSIX, CPU and CUDA, and
several optional backends (Azure, DeepL, RVC, CosyVoice) that most contributors will not
all have keys or hardware for.

**"I could not test the GPU path" is a useful sentence.** Silence is not — it leaves a
reviewer unable to tell whether something was checked or merely assumed.

If you are fixing a bug, include the input that triggers it and the wrong output or
traceback. A reviewer who can reproduce it in ten seconds can merge in a minute.

## Vendored code

`third_party/`, `cosyvoice/` and `rvc/` are vendored upstream projects. Fixes that
belong upstream should go upstream — patching them here means carrying the patch
forever. If a change here really is necessary, say why in the PR.

## Security

Please do not open a public issue for a security problem. See
[SECURITY.md](SECURITY.md).
