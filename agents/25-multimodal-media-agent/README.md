# Multimodal Media Generation Agent

Plans a campaign media asset, selects a live Atlas Cloud image or video model, validates the current model schema, and prepares a generation request. The default run is a dry run so you can review the chosen model, schema fields, request body, and cost metadata before submitting a paid generation job.

**Framework**: Python

**Media API**: Atlas Cloud

**Difficulty**: Intermediate

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Fill in `ATLASCLOUD_API_KEY` only if you plan to submit a generation job.

## Run a dry run

```bash
python agent.py \
  --type Image \
  --keyword "text-to-image" \
  --brief "Launch banner for a productivity app that summarizes meetings" \
  --audience "startup operators" \
  --style "clean editorial illustration"
```

Expected output:

```text
Selected model: <live model from Atlas Cloud>
Schema fields: [...]
Request body: {...}
Dry run only. Re-run with --submit after reviewing the request and cost.
```

## Submit and poll

```bash
python agent.py \
  --type Image \
  --keyword "text-to-image" \
  --brief "Launch banner for a productivity app that summarizes meetings" \
  --audience "startup operators" \
  --style "clean editorial illustration" \
  --submit \
  --poll
```

The agent fetches the live model catalog and schema at runtime, then sends only fields accepted by the selected model. It does not retry `POST` requests automatically, which avoids accidental duplicate paid jobs.
