# Contributing to 500-AI-Agents-Projects

Welcome — this repository collects 500 AI agent projects, templates, demos, and integrations. Thank you for helping grow a practical, reproducible, and responsible catalog of agent work. This document is tuned to the AI-agent focus of the project: reproducibility, model/data hygiene, evaluation, and safety.

Quick summary
- Add small, runnable, well-documented agent examples and templates.
- Prefer reproducible demos and small checkpoints or external download scripts.
- Follow the folder schema and metadata so projects are discoverable and automatable.
- Pay attention to license, data provenance, and ethical/safety notes.

---

## What to contribute
- New agent projects (single- or multi-agent; code, notebooks, or demos).
- Templates/boilerplates for agent types (reactive, planning-based, learning agents, RL, LLM-based, etc.).
- Integrations (environments, simulators, observability / logging tools).
- Shared tooling (evaluation harnesses, metrics, benchmark suites, dataset loaders).
- Docs, reproducible experiments, visualization utilities, or lightweight datasets (or links to them).

If your contribution is large (new category, many projects, major refactor) please open an issue first to coordinate placement and naming.

---

## Project folder requirements (must-have)
Each agent project added must include the following at the top level of its folder:

Agents live in `agents/NN-agent-name/` where `NN` is the next free number. Copy the
layout of an existing agent — `agents/01-web-research-agent/` is the reference. Exactly
five files, nothing more:

- `README.md` — what it does, quick start with exact commands, sample output, and rough runtime.
- `agent.py` — the runnable entrypoint. Must run end-to-end in under 10 minutes.
  A notebook is fine instead if the demo is genuinely better that way.
- `requirements.txt` — pin your versions. `pyproject.toml` or `environment.yml` also fine.
- `.env.example` — every env var the agent needs, with placeholder values. Never a real key.
- `metadata.yaml` — see the schema below.

Everything here is MIT under the repository root `LICENSE`. If your agent pulls in code,
models, or data under a different licence, say so in your README and link the source.

Large models and datasets don't belong in the repo. Host them externally (Hugging Face,
S3, Zenodo) and add a download script.

metadata.yaml schema
```yaml
title: web-research-agent
description: Searches the web for a topic and synthesizes a structured research report
author: your-github-username
language: python
framework: langgraph        # langgraph | crewai | autogen | agno | llamaindex | other
tags: [research, web-search, rag, langgraph]
industry: general
difficulty: intermediate    # beginner | intermediate | advanced
llm: gpt-4o-mini
entrypoint: agent.py
requirements: requirements.txt
```

---

## Naming & layout conventions
- Folder names: lowercase, hyphen-separated (e.g., multi-agent-pursuit).
- Place one logical project per folder.
- Keep demos and notebooks near the code: demo.ipynb and run_demo.py in the project root.
- Avoid committing large binaries. Use .gitattributes or .gitignore to keep repository clean.

---

## Reproducibility & experiments
- Include seed values, environment variables, and exact dependency versions.
- Provide a minimal run command and expected output sample.
- For stochastic experiments, include evaluation scripts and deterministic seeds or checkpoints.
- If results require large compute or private data, include a small reproducible “toy” example that demonstrates the same pipeline on tiny inputs.

---

## Models, datasets & large files policy
- Don’t add large datasets or model checkpoints directly. Instead:
  - Provide a download script (download.sh / download.py) that fetches artifacts from a stable host (Hugging Face, S3, Zenodo).
  - Document the expected location/path after download.
- Clearly state dataset licenses, attribution, and any usage restrictions.
- When linking to external model weights provide their license and any fine-tuning provenance.

---

## Code style, documentation & tests
- Python: follow PEP 8, add a linter config (.flake8, pyproject.toml with [tool.black] or similar).
- JS/TS: provide ESLint/Prettier configs where relevant.
- Document complex algorithms with short docstrings and references.
- Add unit or integration tests when possible. Include a lightweight smoke test that CI can run quickly.

---

## Evaluation & metrics
- Include an evaluation script that produces metrics (accuracy, reward, latency).
- State measurement conditions (hardware, seeds).
- Where applicable, include latency and memory cost alongside performance metrics.

---

## CI / GitHub Actions recommendations
- If adding workflows, put them under .github/workflows and ensure expensive jobs are optional or use small inputs.
- Recommended checks: lint, unit tests, smoke demos. Heavy training jobs should be omitted or gated/opt-in.

---

## PR process and checklist
Before opening a PR:
- [ ] Fork and create a branch: feat/<short-desc> or fix/<short-desc>
- [ ] Sign off every commit with `git commit -s` (see below)
- [ ] Update README and metadata
- [ ] Paste real sample output from a run into your agent's README
- [ ] Ensure no secrets or private data are included
- [ ] Rebase onto current `main` — README moves fast and stale branches conflict
- [ ] Confirm license compatibility for added assets

### Sign your commits (DCO)

Every commit needs a `Signed-off-by` line. Use `-s` and git adds it for you:

```bash
git commit -s -m "add my agent"
```

Which appends:

```
Signed-off-by: Your Name <you@example.com>
```

Forgot on commits you already pushed? Fix them all at once:

```bash
git rebase --signoff origin/main
git push --force-with-lease
```

Set `git config user.name` and `git config user.email` first, since the sign-off must
match the commit author. A CI check enforces this on every PR.

This is the [Developer Certificate of Origin](https://developercertificate.org/) — by
signing off you're stating that you wrote the contribution, or otherwise have the right
to submit it under this repository's MIT licence. There's no separate form to fill in
and nothing is stored beyond the commit itself.

PR description should include:
- What changed and why
- How to run the example(s) and tests
- Links to related issues or external artifacts (datasets, model hosts)

Suggested minimal PR template (add to .github/PULL_REQUEST_TEMPLATE.md if helpful):
```markdown
## Summary
Short description of change

## How to run
1. pip install -r requirements.txt
2. python run_demo.py

## Checklist
- [ ] README updated
- [ ] metadata.yaml added/updated
- [ ] smoke test included
```

---

## Security, secrets & responsible disclosure
- Never commit secrets, private keys, or API tokens.
- If you discover a security vulnerability, do not open a public issue. Contact maintainers privately (see repository contact info) or use GitHub's private security advisory.

---

## Ethics, fairness & safety
AI agents can amplify harms. When contributing:
- Include an explicit "Ethical considerations" or "Safety notes" section in the README if the agent interacts with people, makes decisions, or processes personal data.
- State potential biases, failure modes, and appropriate usage guidance.
- Avoid shipping models trained on clearly disallowed data (private or scraped personal content without consent).
- Prefer human-in-the-loop defaults for high-risk demos and clearly mark such demos as not production-ready.

---

## Licensing and attribution
- Respect upstream licenses for models, code, and datasets. Include attribution and license text where required.
- If the project uses third-party models/datasets, list their license and link to the source.

---

## Communication & review
- Maintainers will review PRs and may request changes. Please reply to review comments and push updates.
- For large or disruptive changes, maintainers may ask for staged PRs to ease review.

---

## Contributor support & contact
If you need early feedback:
- Open an issue describing your planned contribution with the following: summary, folder name, and minimal example of what you plan to add.
- For urgent or private matters, use the contact method listed in the repository (owner profile / repo settings).

---

## Code of Conduct
By contributing, you agree to the project's Code of Conduct. Be respectful, constructive, and collaborative.

---

Thank you for contributing to 500-AI-Agents-Projects — your examples, templates, and tools make the agent community stronger and more reproducible.
