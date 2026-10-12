# n8n sandbox — OCR+Transform via SharePoint list

Status: Draft — not validated against a live system
Last reviewed: 2026-10-09

Written for: the engineer who sets up the SharePoint list and imports this workflow into n8n.

This is a **sandbox draft**. It has been checked for structural correctness (every node reachable, every node reference resolving), but it has never run against a real myGenAssist or SharePoint tenant. Two parts are placeholders that you must adjust before the first run — both are marked in section 6.

## What it does

Takes a document from a SharePoint list item, translates it with the prompt in
[`prompt.ocr+transform.0.9.md`](../../docs/05-design-spec/promtpts%20for%20text%20recogniztion/prompt.ocr+transform.0.9.md),
and writes the generated files back onto the same list item as attachments.

```
SharePoint list (Status = New)
        │
        ▼
  claim item  ──────────────►  Status = Processing
        │
        ▼
  download source attachment + prompt file
        │
        ▼
  ┌──► myGenAssist call  ──►  parse status + state block
  │           │
  │           ├─ INCOMPLETE ──► loop back (resume at next_stage)
  │           ├─ COMPLETE   ──► collect files ──► upload ──► Status = Done
  └───────────┴─ abort      ─────────────────────────────► Status = Manual review
```

The loop exists because the prompt reliably hits the myGenAssist step limit before a document is finished — see [resume-loop.md](../../docs/05-design-spec/resume-loop.md). An interruption is **not an error**; the workflow picks the run back up where it stopped.

## Folder layout

| Path | Contents |
| --- | --- |
| `workflows/` | Importable n8n workflow JSON |
| `config/` | `.env.example` — every setting the workflow reads |
| `docs/` | SharePoint list schema as a reference table |
| `scripts/` | Helper scripts (currently: workflow structure check) |

---

## 1. Set up the SharePoint list

Create a **custom list** (not a document library — the workflow uses list-item attachments).

### Columns

| Display name | Internal name | Type | Set by | Purpose |
| --- | --- | --- | --- | --- |
| Title | `Title` | Single line of text | human | Free label for the case |
| Status | `Status` | Choice | both | Drives the workflow. Values below. |
| CallCount | `CallCount` | Number | workflow | How many myGenAssist calls this document needed |
| BudgetConsumed | `BudgetConsumed` | Number (4 decimals) | workflow | Cost up to before the last call — see section 5 |
| BudgetUnit | `BudgetUnit` | Single line of text | workflow | Currency of the figure above |
| ProcessingStartedAt | `ProcessingStartedAt` | Date and Time | workflow | When the item was claimed |
| ProcessingFinishedAt | `ProcessingFinishedAt` | Date and Time | workflow | When it ended, either way |
| NotesForReviewer | `NotesForReviewer` | Multiple lines of text | workflow | Abort reason, or which files are missing |

**Status choice values — use these strings exactly:**

`New` · `Processing` · `Done` · `Done (partial)` · `Manual review`

The workflow only ever picks up `New`. Everything else it either sets itself or leaves alone.

> **Internal names matter, display names do not.** SharePoint derives the internal name from the display name at creation time and then freezes it. If you create a column called "Call Count" the internal name becomes `Call_x0020_Count`, and the workflow's `CallCount` write fails. Create each column with the exact display name above (no spaces), then rename it afterwards if you want nicer labels.

### Index the Status column

List settings → the `Status` column → **Index this column**.

Without the index, the `$filter=fields/Status eq 'New'` query needs the `Prefer: HonorNonIndexedQueriesWarningMayFailRandomly` header — which the workflow sends, but as the header name says, it may fail randomly once the list grows past 5000 items. Indexing makes it deterministic; you can then remove that header from the `SP: list New items` node.

### How a case is submitted

1. Create a list item, Status = `New`.
2. Attach **exactly one** source document (PDF, image, scan).
3. Leave the other columns empty.

The workflow refuses an item with zero or several source attachments rather than guessing which to translate. It ignores attachments whose names look like generated output (`_Translated by AI`, `_AI Translation Quality Report`, …), so re-running a half-processed item does not feed its own output back in.

---

## 2. Register an Entra application

The workflow talks to SharePoint through Microsoft Graph with an app identity (client credentials), so it runs unattended with no signed-in user.

1. Entra admin centre → **App registrations** → *New registration*. Name it for this use case.
2. **Certificates & secrets** → new client secret. Copy the value immediately; it is shown once.
3. **API permissions** → Microsoft Graph → *Application permissions*:

   | Permission | Why |
   | --- | --- |
   | `Sites.ReadWrite.All` | Read list items, read and write attachments, update fields |

   Then **Grant admin consent** — application permissions do not work without it.

4. Note the **tenant ID**, **client ID** and **client secret**.

> `Sites.ReadWrite.All` grants access to every site in the tenant. If your Bayer tenant policy requires least privilege, use `Sites.Selected` instead and have a SharePoint admin grant this app write access to that one site. That is the better posture; it needs one extra admin step per site.

### Find the site ID and list ID

With the app token, or in Graph Explorer:

```http
GET https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{site-path}
→ "id": "contoso.sharepoint.com,8f1e…,3b2d…"      ← SP_SITE_ID (the whole comma-joined string)

GET https://graph.microsoft.com/v1.0/sites/{SP_SITE_ID}/lists?$filter=displayName eq 'Your List'
→ "id": "a1b2c3d4-…"                               ← SP_LIST_ID
```

---

## 3. Configure n8n

### 3.1 Credentials

Create these **before** importing, so the import can bind to them.

| Credential | n8n type | Used by | Settings |
| --- | --- | --- | --- |
| `SharePoint Graph` | Microsoft Graph Security OAuth2 API | all `SP: …` nodes | Grant type **Client Credentials**, tenant ID, client ID, client secret, scope `https://graph.microsoft.com/.default` |
| `myGenAssist API` | Header Auth | `myGenAssist call` | Header name and value per the myGenAssist API contract (typically `Authorization` / `Bearer …`) |
| `Budget API` | Header Auth | `Read budget balance` | Only if you enable budget measurement (section 5) |

> The workflow references the Graph credential by type, not by name. After import, open each `SP: …` node once and select your credential from the dropdown — n8n does not bind it automatically.

**Never put a token in a node parameter, an environment variable that ends up in the message body, or the processing state.** The state block is passed back and forth between calls and would carry the secret permanently ([NFR-002](../../docs/02-requirements/non-functional-requirements.md)).

### 3.2 Environment variables

Copy [`config/.env.example`](config/.env.example) and fill it in. n8n reads these through `$env`, which requires:

```
N8N_BLOCK_ENV_ACCESS_IN_NODE=false
```

Without it, every `$env` lookup returns empty and the workflow fails at the first Graph call with a confusing 404.

### 3.3 Make the prompt file readable

The `Read prompt file` node reads the prompt from disk on every call. Mount the repo folder **read-only** into the n8n container:

```yaml
# docker-compose.yml
services:
  n8n:
    volumes:
      - /path/to/iqms-complaintmanagement-redesign/docs:/data/prompts:ro
    environment:
      - N8N_BLOCK_ENV_ACCESS_IN_NODE=false
      - NODE_FUNCTION_ALLOW_BUILTIN=buffer
```

Then set `PROMPT_FILE_PATH=/data/prompts/05-design-spec/promtpts for text recogniztion/prompt.ocr+transform.0.9.md`.

`NODE_FUNCTION_ALLOW_BUILTIN=buffer` is needed by the `Collect output files` node, which base64-encodes the reconstructed Markdown. Without it that node throws `Cannot find module 'buffer'`.

> **Pin the prompt version in the path.** A released prompt file is immutable precisely so a result can be traced to what produced it. Pointing at a "latest" symlink would silently change what your runs are based on.

### 3.4 Import

n8n → *Workflows* → **Import from file** → [`workflows/ocr-transform-sharepoint.json`](workflows/ocr-transform-sharepoint.json).

Then, in order:

1. Select the credential in each of the six `SP: …` nodes and in `myGenAssist call`.
2. Adjust the two placeholders in section 6.
3. Run once manually with a single test item before activating the schedule trigger.

---

## 4. The two delivery paths

It is **not settled** whether myGenAssist returns files through its API or only text — an open question in [resume-loop.md](../../docs/05-design-spec/resume-loop.md). The workflow detects which case it is at runtime:

| Case | What happens | Status set |
| --- | --- | --- |
| Response carries file attachments | All four files are uploaded unchanged | `Done` |
| Response is text only | The Markdown version is extracted and uploaded; DOCX, quality report and CSV cannot be produced | `Done (partial)` |

In the text-only case, `NotesForReviewer` names the missing files. The workflow deliberately does **not** fabricate a DOCX from the Markdown: it would lose the blue handwriting marking, the Word comments and the preamble page — the three things that make the output reviewable. Half a deliverable, clearly labelled, beats a convincing-looking one that has quietly dropped its review aids.

If it turns out myGenAssist only ever returns text, that is a design decision to take deliberately: either build the DOCX on the n8n side (a real piece of work — see the prompt's Phase 6 for what it has to reproduce) or drive myGenAssist through a different surface.

---

## 5. Budget measurement (optional, off by default)

From prompt 0.8 the quality report opens with the budget consumed. **The prompt measures nothing** — it is forbidden from calling anything, because a measurement step would eat the step budget it is meant to measure. n8n measures and hands the figure in.

Enable with `BUDGET_ENABLED=true` and set `BUDGET_ENDPOINT_URL`.

Before you trust the number, settle these four properties of the endpoint:

| Question | Why it matters | Where it lands |
| --- | --- | --- |
| Remaining balance or cumulative usage? | **Flips the sign.** Wrong way round puts a negative number in the report. | `BUDGET_MODE=remaining\|cumulative` |
| Update delay — immediate or batched? | With a delay, the reading before call *n* does not even include call *n−1*. The figure is then too low by an unknown amount. | no setting — if it is batched, the figure is not trustworthy |
| Scope — per user, project or API key? | Decides how much parallel processing on the same account distorts the difference. | note it in the audit log |
| Rate limit | The loop reads once per call. | — |

You must also adjust the response parsing in `Compute budget lines`:

```js
// TODO: adjust to the real response shape of the budget endpoint.
const current = Number(raw?.balance ?? raw?.value ?? raw?.amount);
```

### The figure is structurally incomplete, by design

n8n reads **before every call**. So the number written to SharePoint covers everything up to *before the last call* — the call that writes the quality report cannot include its own cost, because that cost is only known once the report is already written.

The quality report says so in its own text. For a dependable per-document cost, measure once more after the run ends and write that to your audit log ([NFR-004](../../docs/02-requirements/non-functional-requirements.md)).

If the reading fails, the call goes out anyway without the budget lines and the report states `not available`. A measurement must never break a run.

---

## 6. What you must still adjust

Two places are placeholders. They are marked in the node notes as well.

### 6.1 The myGenAssist request and response shape

`myGenAssist call` currently sends a multipart form with `files`, `model`, `temperature` and `message`, and `Parse status + state` reads the text from a handful of likely JSON paths:

```js
res.body?.content ?? res.body?.message ?? res.body?.choices?.[0]?.message?.content
```

**Both are guesses.** Replace them with the actual contract. Everything else in the workflow depends only on the delimiter blocks inside the response text, not on the envelope.

### 6.2 The budget endpoint

See section 5. Leave `BUDGET_ENABLED=false` until it is clarified; the run works without it.

---

## 7. How the resume loop behaves

Per call, the prompt emits a status block and a state block. The workflow takes the **last complete** pair — "complete" meaning both delimiter lines are present *and* the state JSON parses.

```text
===AI-TRANSLATION-STATUS===
run_state: INCOMPLETE
stages_completed: E1,E2,E3
next_stage: E4
===END-STATUS===
```

### Exit conditions

| Condition | Action |
| --- | --- |
| `run_state: COMPLETE` | Collect files, upload, `Done` |
| More than `MAX_CALLS_PER_DOCUMENT` calls (default 8) | `Manual review` |
| `stages_completed` unchanged across two consecutive calls | `Manual review` — the run is not progressing |
| No parsable status block twice in a row | `Manual review` |
| Prompt reported `blocked_step` | `Manual review` |

On abort the source stays on the list item and `NotesForReviewer` records the reason and the stage reached. Nothing is discarded silently.

### The known failure mode

The state block carries `translated_content` — the **entire translated document**, 10–15 KB for three pages. If the turn is cut off at the step limit while that JSON is being written, the block is truncated and unusable.

The workflow detects this (`stateBlockTruncated`) and says so in `NotesForReviewer` instead of reporting a generic failure. If you see it often, it is a finding against the prompt, not against this workflow — and the fix belongs in a prompt 0.10: either keep `translated_content` out of the in-response block, or cut the stages smaller. Which of the two is right depends on whether a myGenAssist call can continue an existing session, which is still open.

---

## 8. Retention

The state block holds the full translated document. The workflow keeps it in memory for the duration of the loop only and drops it at the end (`Drop state from memory`). Execution data saving is set to `none` for successful runs so the content is not written to the n8n database.

Error executions **are** saved (`saveDataErrorExecution: all`) so a failure can be diagnosed — which means a failed run may retain document content in the n8n database. Set your retention accordingly (`EXECUTIONS_DATA_MAX_AGE`), and treat that database as holding complaint data.

---

## Related

- [resume-loop.md](../../docs/05-design-spec/resume-loop.md) — the loop contract this implements
- [manual-test.md](../../docs/05-design-spec/manual-test.md) — running the same prompt by hand
- [prompt folder README](../../docs/05-design-spec/promtpts%20for%20text%20recogniztion/README.md) — prompt versioning rule
- [ADR-001](../../docs/06-decisions/adr-001-n8n-platform.md) — n8n is the automation platform

Per [`workflows/README.md`](../../workflows/README.md) at repo root, production workflow exports live there once the design spec is agreed. This folder is the sandbox until then.
