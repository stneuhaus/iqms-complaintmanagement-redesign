# Resume loop for the translation prompt

Status: Draft
Last reviewed: 2026-10-09

Written for: the engineer who builds the n8n workflow around the translation prompt.

To run the prompt by hand in myGenAssist instead — before the workflow exists — follow [manual-test.md](manual-test.md).

## Why this document exists

The translation prompt ([`promtpts for text recogniztion/prompt.en.0.8.md`](promtpts%20for%20text%20recogniztion/prompt.en.0.8.md), German master [`prompt.de.md`](promtpts%20for%20text%20recogniztion/prompt.de.md)) reliably hits the step limit of myGenAssist before a document is fully processed:

> The assistant stopped after reaching the maximum number of steps for this turn.

A prompt cannot restart itself. Once the turn ends, the model is no longer running and no text inside the prompt can trigger a new request. The resume has to come from the caller.

From version 0.6 onwards the prompt therefore makes the run **interruptible and resumable**: it works in five stages and, after each one, emits a machine-readable status block and a state block. This document specifies what n8n must do with them so that a document completes without a human typing "continue".

Version references in this document point at the behaviour, not at a file to use. The current English prompt is named in that folder's [README](promtpts%20for%20text%20recogniztion/README.md).

| Responsibility | Owner |
| --- | --- |
| Detect the interruption and call again | **n8n** |
| Carry the state between calls | **n8n** |
| Signal whether the run is finished and where it stopped | prompt (0.6+) |
| Resume without repeating or skipping work | prompt (0.6+) |

## What the prompt emits

After every completed stage, the model outputs two blocks. The delimiters are literal and must be matched exactly — a single changed character breaks the loop silently.

```text
===AI-TRANSLATION-STATUS===
run_state: INCOMPLETE
stages_completed: E1,E2,E3
next_stage: E4
pages_total: 3
pages_processed: 3
handwritten_segments: 19
files_written: 001_Translated by AI.docx
===END-STATUS===
===AI-TRANSLATION-STATE===
{ ...JSON... }
===END-STATE===
```

The five stages are E1 recognition, E2 translation, E3 DOCX, E4 Markdown, E5 reports. `run_state` is `COMPLETE` only when all five are done and all four output files exist.

## Loop logic

1. **First call** — send the prompt file and the PDF as attachments, with the message body:

   ```text
   Process the attached PDF according to the attached prompt file.
   ```

2. **Parse the response** for the **last complete** `===AI-TRANSLATION-STATUS===` block. "Complete" means both delimiter lines are present. Take the last one, not the first: the response contains one block pair per completed stage.

   A truncated block is discarded — the preceding complete one is the authoritative state. If **no** complete block pair is present at all, treat the next call as a first call (step 1) and count it against the call limit.

3. **`run_state: COMPLETE`** → collect the output files, exit the loop.

4. **`run_state: INCOMPLETE`** → build a follow-up call from four parts:

   - the **same** prompt file as an attachment,
   - the **same** PDF as an attachment,
   - the `===AI-TRANSLATION-STATE===` block from the same response, verbatim and including both delimiter lines,
   - this message body, with the state block appended:

     ```text
     Continue the processing run described by the processing state below.
     Resume at the stage given in next_stage. Do not repeat completed stages.

     ===AI-TRANSLATION-STATE===
     { ...the extracted state... }
     ===END-STATE===
     ```

   Send prompt and PDF again on every call. A follow-up call may land in a fresh session where neither is present.

5. Repeat from step 2 until `COMPLETE` or an exit condition below trips.

Why parse the last block and not the end of the response: the turn can be cut off mid-output, so a block near the end may be truncated.

The message body above is identical to the one in [manual-test.md](manual-test.md), so a manual test and the automated loop exercise the same path.

## Exit conditions

These prevent the most expensive failure mode — a loop that retries the same stage forever.

| Condition | Action |
| --- | --- |
| `run_state: COMPLETE` | Success. Collect files, exit. |
| More than **8** calls for one document | Abort, route to manual review. Five stages plus reserve. |
| `stages_completed` unchanged across two consecutive calls | Abort, route to manual review. The run is not progressing. |
| No parsable status block in the response | Retry once, then abort and route to manual review. |

On abort, retain the source document, the last known state and the call count so the case can be followed up. Never discard silently.

## State handling

Send the state back **verbatim**. Do not reformat, re-indent or re-serialise the JSON — the prompt reads it back and relies on its own field names.

The state carries `translated_content`, the full translated text. This is what makes a resume cheap: without it, a follow-up call would have to redo the translation, which is the most expensive stage. Expect the state to grow to a substantial size for longer documents and size the request limits accordingly.

The prompt also writes a `%Original Name%_AI Translation State.json` file. Do not rely on it across calls — if the follow-up call starts a fresh session, the sandbox is empty and that file is gone. The in-response state block is the authoritative transport.

From 0.8 the state also carries a `budget` object. It is pass-through data: n8n puts the figures in, the prompt stores them and prints them in the quality report. See the next section.

## Budget measurement

From 0.8 the quality report opens with the budget consumed for the document. **The prompt measures nothing** — it is explicitly forbidden from calling a tool, running code or making a network request for this, because a measurement step would quietly eat the step budget it is meant to measure.

n8n reads the credit balance **before every call** and passes the consumption accrued since the first call in the message body:

```text
budget_consumed: 0.42
budget_unit: EUR
budget_calls: 2
```

- Keep the balance from the first call as the baseline for the document.
- On the first call, `budget_consumed: 0` — nothing has been consumed yet.
- The figure in the report therefore covers everything up to **before** the last call. The last call, the one that writes the report, is necessarily missing from it: its cost is only known once the report has already been written.
- For the full cost per document, measure once more after `COMPLETE` and write the value to the audit log ([NFR-004](../02-requirements/non-functional-requirements.md)). That is the dependable number for a cost projection; the number in the report is the documented partial figure, and it says so.
- Credentials for the budget endpoint belong in the n8n credential store — never in the message body and never in the state block ([NFR-002](../02-requirements/non-functional-requirements.md)). The state is passed back and forth between calls and would otherwise carry the secret permanently.
- If the measurement fails, send the call anyway and omit the budget lines. The run must not fail over a measurement; the report then states `not available`.

### To settle before building this

The budget endpoint is not specified here yet. Four properties change the implementation and need to be confirmed against its documentation:

| Question | Why it matters |
| --- | --- |
| Remaining balance or cumulative usage? | Flips the sign. The wrong way round puts a negative number in the report. |
| Update delay — immediate or batched? | With a delay, the reading taken before call *n* does not even include call *n−1* in full, and the reported figure is too low by an unknown amount. |
| Scope — per user, project or API key? | Determines how much parallel processing on the same account distorts the difference. |
| Rate limit | The loop reads once per call; confirm that fits. |

## Data retention — owned by the workflow, not the prompt

Prompt versions up to 0.6 asked the model to delete uploaded files, clear tool caches and drop result files after 15 minutes. A prompt cannot do any of that: once the turn ends the model is no longer running, and it has no access to platform caches or to copies you downloaded. In practice the model answered with a disclaimer explaining what it could not guarantee — noise in the response, and no data actually deleted.

From 0.7 the prompt only commits to what it controls (not restating document content in the response body, removing its own temporary working files) and is explicitly told not to comment on the rest. Retention is the workflow's job:

- Delete result files from the platform once n8n has collected them. Do not wait for a timer.
- Do not persist the state block. It carries the full translated text — keep it in memory for the duration of the loop only, and drop it when the run reaches `COMPLETE` or is routed out.
- When a run is routed to manual review, the retained document and state (see Exit conditions) fall under the same retention rule as any other complaint data. Define where they go and for how long.
- Implement the applicable retention period in the workflow, not in the prompt.

## Expected behaviour

For the 3-page reference document (`test_input/001.pdf`), expect 2–3 calls. The reference result to match is in `test_input/Claude Opus 4.8/try 02/`: four output files, 19 blue passages, 19 Word comments authored `AI Translation`, 19 `[HW]` markers in the Markdown version.

## Open questions to settle before building

- **Does myGenAssist return files through n8n, or only text?** If only text, the DOCX and CSV cannot be collected as artifacts and would have to be built on the n8n side from the Markdown version and the state. This changes how stages E3 and E5 are used and should be answered first.
- **Can a call continue an existing session?** If yes, the state file survives and the in-response block is a redundant safeguard. If no, the block is the only transport. The prompt works either way.
- **Request size ceiling** for prompt + PDF + state on larger documents.
- **The budget endpoint's four properties** — see the table under "Budget measurement". Settle these before the figure in the quality report is used for a cost projection.

## Related

- [ADR-001](../06-decisions/adr-001-n8n-platform.md) — n8n is the automation platform
- [ADR-002](../06-decisions/adr-002-mvp-slice.md) — translation is part of the first delivery slice
- [FR-006](../02-requirements/functional-requirements.md) — translate non-English complaint text and attachments

No workflow JSON is committed yet. Per [`workflows/README.md`](../../workflows/README.md), exported workflows follow once the design spec is agreed.
