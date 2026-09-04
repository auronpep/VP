# Security Policy

## Reporting a vulnerability

Please **do not open a public issue** for a security problem.

Use GitHub's private reporting instead: go to the repository's **Security** tab and
choose **Report a vulnerability**. That opens a private advisory visible only to the
maintainers, and it lets a fix be prepared before any details become public.

If private reporting is not enabled on the repository, open a normal issue that says
only *"security report, please enable private advisories"* — with no details — and wait
for a maintainer to make contact.

When you report, the most useful things to include are:

- what an attacker can achieve, in one sentence
- the exact input that triggers it (a URL, a filename, a subtitle file, a model pack)
- the affected file and line if you have it
- your platform and Python version

## Scope

This project runs locally, drives external media tooling, and downloads models, so the
areas most worth scrutiny are:

- **Command construction.** Several code paths build `ffmpeg` / `demucs` command lines
  from user-supplied file paths. Paths can originate from a YouTube video title, which
  is controlled by whoever uploaded the video, so anything that reaches a shell counts
  as untrusted input.
- **Archive extraction.** Model packs are downloaded and unzipped. Entry names inside an
  archive are attacker-controlled and must not be able to escape the extraction
  directory.
- **Model loading.** `torch.load` and ONNX sessions execute data from model files.
  Downloaded checkpoints should come from a pinned source over verified TLS.
- **Web exposure.** Running with `--listen` or `--share` puts the Gradio UI on the
  network. `src/shared.py` warns about this, but it is worth restating: the UI can read
  and write files anywhere the process can, so it should not be exposed to an untrusted
  network without `--gradio-auth`.
- **Credentials.** Azure keys are read from `.env` via `app/abus_config.py`. Keys must
  not appear in logs, in Gradio output, or in a committed `.env` — only `.env.example`
  belongs in git.

## Out of scope

- Vulnerabilities in upstream dependencies that have no exploitable path in this
  project — report those to the upstream project.
- Findings that require the attacker to already have local code execution as the user
  running the app.
- The vendored third-party trees (`third_party/`, `cosyvoice/`, `rvc/`) where the issue
  also exists upstream. Please report those upstream, and mention them here only if this
  project's usage makes them reachable in a way upstream does not.

## Supported versions

Development happens on `main`, and fixes land there. If you are running an older
checkout, please re-test against current `main` before reporting.
