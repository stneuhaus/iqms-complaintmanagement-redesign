# SharePoint list — reference

Status: Draft
Last reviewed: 2026-10-09

Written for: whoever creates or audits the list. Setup instructions are in the [sandbox README](../README.md) section 1; this page is the schema on its own, for checking an existing list against.

## List type

**Custom list**, not a document library. The workflow uses *list-item attachments*, which a document library does not have.

## Columns

| Internal name | Type | Written by | Notes |
| --- | --- | --- | --- |
| `Title` | Single line of text | human | Free label |
| `Status` | Choice | both | See values below |
| `CallCount` | Number | workflow | myGenAssist calls needed for this document |
| `BudgetConsumed` | Number, 4 decimals | workflow | Null unless budget measurement is on |
| `BudgetUnit` | Single line of text | workflow | Currency of the above |
| `ProcessingStartedAt` | Date and Time | workflow | Set when the item is claimed |
| `ProcessingFinishedAt` | Date and Time | workflow | Set on success and on abort |
| `NotesForReviewer` | Multiple lines of text, plain | workflow | Abort reason or missing-file list |

The internal name is what Graph writes to, and SharePoint freezes it at creation from the display name. Create the columns with these exact display names (no spaces), rename afterwards if you want friendlier labels. A column created as "Call Count" gets the internal name `Call_x0020_Count` and the write fails.

## Status values

| Value | Meaning | Set by |
| --- | --- | --- |
| `New` | Ready to be picked up. **The only value the workflow acts on.** | human |
| `Processing` | Claimed by a run | workflow |
| `Done` | All four output files attached | workflow |
| `Done (partial)` | Only the Markdown version — myGenAssist returned text, not files. See `NotesForReviewer`. | workflow |
| `Manual review` | Aborted. Reason in `NotesForReviewer`, source still attached. | workflow |

## Indexing

Index `Status`. The workflow filters on it; beyond 5000 items an unindexed filter fails intermittently, and the header that works around it is named `HonorNonIndexedQueriesWarningMayFailRandomly` for good reason.

## Attachments

**Input:** exactly one source document per item. Zero or several and the run fails deliberately rather than guessing.

**Output:** written back onto the same item.

| File | Stage | Present when |
| --- | --- | --- |
| `<name>_Translated by AI.docx` | E3 | myGenAssist returns files |
| `<name>_Translated by AI.md` | E4 | always |
| `<name>_AI Translation Quality Report.docx` | E5 | myGenAssist returns files |
| `<name>_AI Translation Used Terminology.csv` | E5 | myGenAssist returns files |

Files matching the generated-output patterns are skipped when the source is picked, so re-running a half-processed item does not translate its own output.

## Permissions

The Entra app needs `Sites.ReadWrite.All` (application) with admin consent, or `Sites.Selected` plus a per-site grant — the better posture, one extra admin step.

Anyone who can read the list can read the attachments, which are complaint documents. Scope list permissions to the people who should see them ([NFR-001](../../../docs/02-requirements/non-functional-requirements.md)).
