# Translation prompt

Status: In progress
Last reviewed: 2026-10-09

The prompt that drives OCR, translation and document generation for non-English complaint attachments ([FR-006](../../02-requirements/functional-requirements.md)).

## Files

| File | Role |
| --- | --- |
| `prompt.de.md` | **German master.** Edited in place. All changes start here. |
| `prompt.ocr+transform.0.9.md` | Current English version — the one to use. |
| `prompt.en.0.7.md`, `prompt.en.0.6.md`, `prompt.en.0.5.md`, `prompt.en.0.4.md` | Earlier English versions, under the former name `prompt.en.*.md`. Frozen. |

From 0.9 the English file is named `prompt.ocr+transform.<version>.md`. The earlier `prompt.en.*.md` files keep their names — a released version is never renamed, because a test record referring to `prompt.en.0.7.md` must stay resolvable.

## Versioning rule

**Every change to the English prompt creates a new file.** Never edit an existing released prompt file.

A released version is immutable because it may already be in use — referenced by an n8n workflow, attached to a test run under `test_input/`, or cited in a test record. Editing it in place would silently change what those runs were based on, and a result could no longer be traced to the prompt that produced it.

Workflow for a change:

1. Edit `prompt.de.md` (the master).
2. Copy the current English file to the next version number: `prompt.ocr+transform.0.9.md` → `prompt.ocr+transform.0.10.md`. A new business feature increments the digit after the first dot (0.9 → 0.10); a pure bug fix keeps the number and appends `_bugfix` to the file name.
3. Apply the same changes there.
4. Set `$prompt_file_version` in **both** files and add one changelog row in each.
5. Update the table above so the current version is unambiguous.

Keep the German master and the newest English file structurally identical — same headings, list items, code fences and table rows. Technical identifiers stay untouched in translation: `HANDWRITING`, `SIGNATURE`, `STAMP`, `#1F3FA8`, `[HW]`, `[UNCLEAR]`, `[ILLEGIBLE]`, the JSON keys, the file-name patterns, and the `===AI-TRANSLATION-STATUS===` / `===AI-TRANSLATION-STATE===` delimiters. Those delimiters are parsed by the automation — a single changed character breaks it silently.

## Related

- [resume-loop.md](../resume-loop.md) — what the n8n workflow must do when a run hits the step limit
- [manual-test.md](../manual-test.md) — how to run the prompt by hand in myGenAssist
