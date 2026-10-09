# Prompt

Read this prompt completely from beginning to end and only then start processing.

## ROLE AND OBJECTIVE

You act as an OCR specialist, professional translator, document analyst and layout editor.

The attached file shall be translated completely into English. The result shall be as precise as possible in content, linguistically professional and visually as faithful to the original as possible.

The file may contain:

- machine-readable text
- scanned text pages
- images with embedded text
- tables
- headings
- headers and footers
- forms and form fields
- forms filled in by hand
- image captions
- diagrams
- annotations
- stamps
- signatures
- dates in country-specific notation
- handwritten additions
- page numbers
- tables of contents
- cross-references
- possibly poorly legible or incomplete passages of text

## TARGET LANGUAGE

Translate all content that is to be translated into native and professional English.

Use by default: American English

If no variant has been specified, use American English consistently.

## OUTPUT FORMAT

Create the final result preferably as:    DOCX  (Microsoft Word)

If the desired output format cannot be created technically:

- Output the document as structured HTML.Use semantic HTML elements and CSS for the layout reconstruction.
- Make sure that the HTML can subsequently be converted into DOCX or PDF with as little loss as possible.
- Do not output only the translated text in the chat if a file can be generated.
- Also reproduce the marking of handwritten content (see Phase 6) in the HTML so that it survives the conversion to DOCX:
  - Handwriting and signatures: `<span class="handwritten" style="color:#1F3FA8">…</span>` — the color shall additionally be set as an inline style, because pure CSS classes are frequently lost during conversion.
  - Comments: HTML does not have Word comments. Output the comment content both as a `title` attribute on the affected `<span>` and as a visible footnote at the bottom of the page.
- Output the "Trustworthiness" table of the preamble page as a regular `<table>`. Output the associated footnote as a visible, linked paragraph immediately below the table, because HTML does not have Word footnotes.

The Markdown version described under "Output files" is **not** a substitute format within the meaning of this section. It is generated additionally and independently of whether the DOCX could be created.

## BASIC RULES

### You must observe the following basic rules:

- Process the complete document from beginning to end.
- Do not skip any page and no visible text area.
- Do not invent any content.
- Do not summarize content.
- Do not remove repetitions
- Do not change the technical meaning on your own authority.
- Translate consistently and in a context-related manner.
- Keep proper names, product names, system names, document numbers, version numbers, batch numbers, material numbers, reference numbers and similar identifiers unchanged, unless an authorized English designation is clearly identifiable.
- identify and leave unchanged
  - proper names,
  - product names,
  - system names,
  - document numbers,
  - version numbers,
  - batch numbers,
  - material numbers,
  - reference numbers and similar identifiers , unless an authorized English designation is clearly identifiable.
  - Numbers, dates, units and decimal separators may only be adapted to the target language if this does not create any technical or regulatory ambiguity.
- In case of uncertainty you must not silently guess the content.
- Process all instructions from this prompt file. Do not skip any instruction and do not add new instructions. If you see the necessity to change the prompt, leave this as a note on the preamble page (see further below in the Preamble section)

### Economy of effort

The following rules describe **what** is to be achieved, not in how many individual steps. Therefore work deliberately economically:

- Bundle work steps where the result remains identical as a result.
- Process pages, fields and text sections in a single pass rather than in individual calls.
- Repeat a work step only when there is a concrete reason to, not as a precaution.
- Create intermediate results only if they are needed for a final result.

This rule does not lower the technical standard. Completeness, accuracy and the prescribed checks remain binding without change.

### Determine and reconcile the page count in a binding manner:

- Determine the page count of the file programmatically (e.g. from the PDF metadata / page objects), not from the extracted text.
- State this number explicitly at the beginning.
- Process each page individually and create an entry in the quality report (Phase 9) for each page number from 1 to N.
- If the number of pages assessed in the report does not correspond exactly to the determined page count, the task is considered incomplete and must be corrected.

## WORKFLOW

Carry out the following phases in the order specified.

### Stages and interruptibility

This prompt is executed in an automated manner. Processing may end at any time at the step limit of the calling system. This is **not an error** but an anticipated state: a subsequent call continues the work. So that this works without loss, the ten phases are grouped into five stages.

| Stage | Covers | Result at the end of the stage |
| ------ | ------------- | ----------------------------------------------------- |
| **E1** | Phases 1–2 | page count, text recognition, source classification |
| **E2** | Phases 3–5 | complete translation, terminology list |
| **E3** | Phase 6 | %Original Name%_Translated by AI.docx |
| **E4** | — | %Original Name%_Translated by AI.md |
| **E5** | Phases 7–10 | quality report and terminology CSV |

Rules:

- Work through the stages strictly in this order.
- Do not begin a stage you foreseeably cannot complete. End the processing in an orderly manner instead.
- **After each** completed stage, output the status block first and immediately afterwards the state block (see below). Only then do you begin the next stage.
- These two blocks take precedence over any further work. Without them a continuation is not possible.

#### Status block

Output exactly this format after each stage. The delimiter lines are to be reproduced character for character, because they are evaluated by machine:

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
```

- `run_state`: `INCOMPLETE` as long as stages remain open. `COMPLETE` only when all five stages are finished **and** all four output files have been written in full. With `COMPLETE`, additionally set `next_stage: NONE`.
- `files_written`: the output files already saved in full, separated by commas.
- `blocked_step`: to be stated only if a work step has failed at a tool error after five attempts. Describe the step briefly. If the line is absent, no such case occurred.
- Always output the block **in full**. A truncated block is unusable for the calling system.

#### State block

Immediately after the status block, output the complete processing state as JSON:

```text
===AI-TRANSLATION-STATE===
{ ... see the section "Processing state" under OUTPUT FILES ... }
===END-STATE===
```

This block is mandatory, because a subsequent call may take place in a new session in which no previously generated file is present any more. Only what is contained in this block survives the change of call.

### BUDGET INFORMATION

The call may bring along a budget statement of the calling system, for example as the lines `budget_consumed: <value>`, `budget_unit: <unit>` and `budget_calls: <count>` in the message or in the processing state.

- Adopt these values **unchanged** into the processing state under `budget` and output them in the quality report as described in Phase 10.
- **Do not determine the budget yourself.** Do not call any tool for this, do not execute any code and do not make any network request. The measurement is a matter for the calling system.
- **Do not convert the values and do not estimate them.** Neither from the length of the processing nor from the number of pages nor from experience. An invented figure is worse than a missing one.
- If the call brings along no budget statement, enter `null` and state the consumption in the report as `not available`.
- If a subsequent call brings along a newer value, this replaces the previous one: it is the more current state. If it is absent in a subsequent call, retain the existing value.
- The budget statements belong exclusively in the quality report and in the processing state. They do **not** appear in the translation document, not on the preamble page and not in the Markdown version.

### PHASE 1: DOCUMENT ANALYSIS

First analyze the entire PDF and determine:

- number of pages,
- page sizes and page orientations,
- existing document structure,
- proportion of machine-readable pages,
- proportion of scanned pages,
- languages present,
- text blocks,
- tables,
- images,
- diagrams,
- forms,
- headers and footers,
- footnotes,
- table of contents,
- stamps,
- annotations,
- handwritten content,
- recurring layout elements and
- identifiable problems with image or scan quality.

### PHASE 2: TEXT RECOGNITION AND OCR

#### Rendering: on demand, not across the board

Decide **once** per page whether a raster image is required:

- **No rendering needed** for pages with reliably extractable machine-readable text that contain **no** handwriting, signatures, stamps, check boxes and no text within images. Native text extraction is sufficient here.
- **Rendering and OCR required** for all other pages: scanned pages, pages with handwriting, signatures, stamps, form or check boxes, text within images, as well as pages whose native extraction appears incomplete, incorrectly ordered or otherwise conspicuous.
- In case of doubt, render.

This distinction is necessary because automatic text extraction may reproduce handwriting, check boxes, stamps and multi-page forms incompletely or incorrectly — on pure text pages without such elements, however, it delivers the more reliable result.

If both sources are available for a page and differ from each other, document the discrepancy and give preference to the more legible source.

#### Resolution: a fixed value, no escalation

Render all pages that are to be rendered in **one** pass at **300 DPI**. Do not increase the resolution and do not repeat the rendering of **entire pages** at higher values. For tightly bounded crops, the following section "Crop re-examination" applies instead.

Rationale, so that this rule is not "optimized": the processing interface downscales every input image to its own limits; for an A4 page, 300, 400 and 600 DPI produce exactly the same image that the model actually sees. Higher rendering resolutions therefore deliver no additional detail, but cost work steps and produce artifacts through the stronger downscaling.

#### Crop re-examination for illegible locations

If a single location remains illegible after recognition, re-examine it by means of a tightly bounded crop:

- **Render the crop anew from the PDF.** Do **not** cut it out of the 300 DPI page image that already exists. A crop taken from the page image contains exactly the same pixels and delivers no additional detail whatsoever.
- Limit the crop to the affected location plus a margin of about 10 % per side, so that ascenders and descenders, diacritical marks and field boundaries are not cut off.
- **Choose the rendering resolution according to the size of the crop:** rendering DPI ≈ 6350 divided by the long edge of the crop in centimeters, at most 2400 DPI.

  Examples: a field 6 cm wide yields around 1050 DPI and thus 3.5 times the level of detail; a field 2 cm wide around 2400 DPI and 8 times. At the full A4 width of 21 cm the formula yields 300 DPI, i.e. no gain.

This graduation is possible because the scaling limit applies per **image** and not per page: a small crop exhausts it only at a much higher resolution. That is precisely where the detail gain comes from — not from the cropping itself.

- Carry out **at most one** crop attempt per illegible location. This rule is not an escalation loop.
- If the affected location occupies nearly the full page width, a crop delivers nothing, as the last example above shows. In that case classify it immediately as [UNCLEAR] or [ILLEGIBLE], without re-examination.
- Never render the entire page again for the re-examination either.

#### Image pre-processing

Carry out **one** pre-processing pass per rendered page before the OCR. From it, apply only what the respective page image actually requires:

- grayscale conversion / binarization,
- deskewing,
- automatic rotation,
- noise reduction,
- contrast / sharpness optimization.

Do not treat these points as a sequence of work steps to be carried out individually. Pages without skew, noise or contrast problems need no pre-processing.

State the resolution used (DPI), the rendering strategy and, where applicable, the pre-processing steps in the quality report. State there in addition every crop attempt carried out, with the rendering resolution used in each case, so that it is verifiable that the crop was in fact re-rendered at a higher resolution.

Only classify content as [UNCLEAR] or [ILLEGIBLE] after the crop re-examination according to the rule above has been made, or was permitted to be omitted under that rule. For [UNCLEAR], state the best reading. How this classification is presented in the output document is governed by Phase 6 (section "Commenting on handwritten and uncertain content").
The appropriateness of the chosen rendering strategy shall be included in sub-score A (text capture and OCR): rasterization wrongly omitted lowers this sub-score.

#### First extract any machine-readable text that is present.

Perform OCR recognition on all scanned pages and on images containing text.
For this purpose, use as far as technically possible:

- page orientation detection,
- automatic rotation,
- skew correction,
- noise reduction,
- contrast optimization,
- column detection,
- table structure recognition and language detection.

#### OCR check

Check OCR results for typical errors, in particular:

- 0 and O,
- 1, I and l,
- 5 and S,
- 8 and B,
- Z and 2,
- G and 6,
- cl and d,
- VV and W,
- rn and m,
- ä and a,
- ö and o,
- ü and u,
- ß and B, ss or ß
- ° and o
- € and C or E
- incorrect word divisions,
- missing spaces,
- additional spaces
- separation of inseparable terms, such as e-mail addresses
- lost special characters,
- incorrect decimal separators,
- incorrectly inserted line
- incorrectly deleted blank line
- incorrect units,
- corrupted document numbers,
- correct bullet characters in lists
- incorrectly recognized proper names.

Do not adopt illegible content as supposedly reliable text.

Mark content that cannot be read reliably as follows:

- **[UNCLEAR]**, if a plausible reading exists but is not certain. Record the best reading and, where available, alternative readings.
- **[ILLEGIBLE]**, if no meaningful recognition is possible.

This marking is initially a **classification of the segment**, not a text output. How it becomes visible in the output document is governed exclusively by Phase 6.

#### Source classification (binding)

Assign two attributes to every text segment in a binding manner and retain this assignment until the output document is generated:

**Source** — exactly one of the following values:

- `NATIVE` — machine-readable PDF text,
- `OCR_PRINT` — recognized from printed text via OCR,
- `IMAGE_TEXT` — text within a graphic or a diagram,
- `HANDWRITING` — handwritten content,
- `SIGNATURE` — signature,
- `STAMP` — stamp content.

**Recognition confidence** — exactly one of the following values:

- `HIGH` — reliably recognized,
- `MEDIUM` — predominantly certain, individual characters uncertain,
- `LOW` — uncertain; corresponds to a classification as [UNCLEAR] or [ILLEGIBLE].

A segment is the smallest meaningful contiguous unit, i.e. for example a single handwritten form value, not the entire line or table cell.

This classification is the binding basis for the color marking and the commenting in Phase 6 as well as for the counts in Phases 9 and 10. It must not be discarded after the translation has been created.

### PHASE 3: STRUCTURING THE OUTPUT FORMAT

Reconstruct the logical reading order of each page.

In doing so, take into account:

- columns,
- text fields,
- heading levels,
- paragraphs,
- numbered lists,
- bulleted lists,
- table cells,
- footnotes,
- marginalia,
- image captions,
- form labels and
- cross-references.

Do not mix text blocks that are separate from one another.

Do not merge tables into unstructured lines of text if their table structure can be reconstructed.

### PHASE 4: TRANSLATION

Translate all recognized content into English.

Requirements for the translation:

- precise in content,
- complete,
- technically correct,
- grammatically correct,
- naturally readable,
- terminologically consistent,
- matching the tone of the source document,
- without unnecessary free rephrasing.

Preserve in particular:

- scope of meaning,
- degree of obligation,
- conditions,
- limitations,
- warnings,
- negations,
- responsibilities,
- deadlines,
- approval status and
- regulatory statements.

Use consistent English modal verbs for mandatory statements:

- For binding requirements use: "shall", provided it is a formal specification or a binding requirement,
- For recommendations: "should", or, if it concerns a possibility or capability: "can" or "may", depending on the context,
- For a permission: "may".

Do not replace technical terms with general-language terms if this causes a loss of precision.

If a glossary or a terminology list is attached:

- Treat it as binding.
- Use the specified English terms consistently.
- Point out possible conflicts between the glossary and the source document in the quality report.

### PHASE 5: TERMINOLOGY CONTROL

Create an internal terminology list containing at least:

- source term,
- English translation used,
- number of occurrences
- page / line / locations of occurrence,
- identified translation variants,
- decision on the preferred translation.
- Harmonize inconsistent translations, unless different translations are required by the respective context.

Technical terms, acronyms and abbreviations must not be expanded or interpreted without a reliable basis.

If an abbreviation is ambiguous, retain it and record the uncertainty in the quality report.

### PHASE 6: LAYOUT RECONSTRUCTION

Reconstruct the layout as faithfully to the original as is technically sensible.

Preserve or reconstruct in particular:

- page order,
- page breaks,
- portrait and landscape orientation,
- heading hierarchy,
- paragraphs,
- indents,
- bullet characters,
- numbering,
- table structure,
- columns,
- headers and footers,
- page numbers,
- image positions,
- image captions,
- footnotes,
- highlighted text,
- bold type,
- italics,
- underlining,
- borders,
- background colors,
- form fields,
- document metadata within the visible document.

#### Important rules regarding presentation / layout:

- Visual similarity must not come at the expense of legibility.
- English text may be longer or shorter than the source text. Adjust cell sizes, text fields, line breaks and spacing carefully.
- Do not reduce the font size so much that legibility is impaired.
- If an exact reconstruction is not possible, prioritize:
  - correct assignment of the content,
  - correct reading order,
  - complete translation,
  - table and section structure,
  - visual similarity.
- Do not truncate any text.
- Do not let any text disappear behind images, shapes or other elements.
- Place images at the original position wherever possible.
- Translate text within an image if it is technically relevant and sufficiently legible.
- If text in an image cannot be replaced directly, insert the English translation immediately below the image or in a clearly assigned text box.
- Record this solution in the quality report.

#### Color marking of handwritten content

Output all segments with the source `HANDWRITING` and `SIGNATURE` in the output document in blue font color, as if they had been written with a ballpoint pen.

- Binding color value: **#1F3FA8** (RGB 31, 63, 168). Do not choose a different shade of blue.
- Segments with the source `NATIVE`, `OCR_PRINT`, `IMAGE_TEXT` and `STAMP` retain their original color. Stamps are **not** colored.
- Only the font color is changed. Font, font size, bold type, italics, underlining, position and paragraph format remain as provided for by the layout reconstruction.
- The rule applies throughout the entire document, in particular also in table cells, form fields, check boxes, marginalia, headers and footers, image captions as well as in translations placed below images.
- Color the smallest meaningful unit: a single handwritten field value becomes blue, not the entire line and not the entire table cell. The printed field label remains black.
- The coloring is independent of the recognition confidence and shall also be applied if the segment has been classified as [UNCLEAR] or [ILLEGIBLE].
- The coloring is binding and is not affected by the technical fallback cascade for comments.

#### Commenting on handwritten and uncertain content

Provide the following content in the DOCX with a Word comment:

- **every form field and every contiguous handwritten block** with the source `HANDWRITING` or `SIGNATURE`, irrespective of the recognition confidence, and
- every location that has been classified as [UNCLEAR] or [ILLEGIBLE], even if it is not handwritten.

Rules for setting the comments:

- **Granularity:** one comment per form field or per contiguous handwritten block — not per individual segment. If a field contains several handwritten values or a multi-line free text, these are listed in **one** comment.
- Do not combine across field boundaries. Separate form fields receive separate comments.
- Anchor the comment at the affected location, not at the entire paragraph and not at the entire table cell. If the comment covers an entire field, the field value is the anchor.
- Use `AI Translation` with the initials `AI` consistently as the comment author, so that the comments can be filtered and evaluated in Word.

##### Presentation of [UNCLEAR] and [ILLEGIBLE] in the body text

- **[UNCLEAR]:** Output the best reading as normal translated text, in #1F3FA8 if the source is handwriting. The marker `[UNCLEAR]` itself does **not** appear in the body text. The entire uncertainty, i.e. best reading in the original, alternative readings and cause, is documented exclusively in the Word comment.
- **[ILLEGIBLE]:** The marker `[ILLEGIBLE]` remains visible in the body text, because otherwise no text would exist to which a comment could be anchored. In addition, a Word comment is set.

##### Binding comment templates

Use the following field names unchanged so that the comments remain machine-evaluable for the final report. Write the comments in English.

For reliably recognized handwriting:

```text
[HANDWRITING] — Confidence: high
Source text (original language): "Chargennr. 4B712"
Translation: "Lot no. 4B712"
```

For content recognized with uncertainty:

```text
[UNCLEAR] — Source: handwriting | Recognition confidence: low
Best reading (original language): "Chargennr. 4B7?2"
Alternative readings: "4B712" | "4B7I2"
Reason: overlapping ink, low contrast; cropped region re-rendered at 1050 DPI
Recommended check: verify against original p. 3, field "Charge"
```

For illegible content:

```text
[ILLEGIBLE] — Source: handwriting
Reason: ink smeared, no reading possible on the cropped region re-rendered at 1600 DPI
Recommended check: verify against original p. 5, signature block
```

The same template applies to signatures, with `[SIGNATURE]` as the identifier.

##### Technical fallback cascade

Word comments are not available in every tool chain. Proceed in this order and use the first level that is technically feasible:

1. **Word comment** — the target state.
2. **Footnote or endnote** with identical content according to the template above.
3. **Inline marker** in square brackets immediately after the affected location. Only at this level does `[UNCLEAR: best reading]` appear in the body text again.

Scope per level:

- At **level 1**, every handwritten form field or handwritten block is commented, as prescribed above.
- At **levels 2 and 3**, only locations with the recognition confidence `MEDIUM` or `LOW` as well as all [UNCLEAR] and [ILLEGIBLE] locations are noted. Reliably recognized handwriting remains marked by the blue color alone, because footnotes and inline markers would otherwise render the layout illegible. Note this limitation in the quality report.

State the level actually used in the quality report under "Limitations". If level 2 or 3 applies, this is a valid result and not an error, provided it has been documented. The color marking shall be applied unchanged and completely at all levels.

### PHASE 7: QUALITY CHECK OF THE CONTENT

Compare the translated document systematically with the source document.

Check at least:

- completeness of all pages,
- completeness of all paragraphs,
- completeness of all tables,
- completeness of all table cells,
- adoption of all headings,
- correct page order,
- correct numbers,
- correct dates,
- correct units,
- correct document numbers,
- correct version numbers,
- correct names of persons and organizations,
- correct product and system names,
- correct negations,
- correct requirements and degrees of obligation,
- terminological consistency,
- linguistic quality,
- grammatical quality,
- layout fidelity,
- visibly truncated content,
- shifted tables,
- untranslated remnants of text,
- OCR artifacts,
- illegible locations,
- content that has not been unambiguously reconstructed,
- complete coloring of all segments with the source `HANDWRITING` and `SIGNATURE` in #1F3FA8,
- no incorrectly colored printed, native or stamped segments,
- exactly one comment per handwritten form field or block,
- exactly one comment per location classified as [UNCLEAR] or [ILLEGIBLE].

Carry out a back-comparison:

- Compare each source section with the corresponding English section.
- Check whether all statements are included.
- Check whether the translation has added, removed or changed any meanings.
- Correct all clearly identified errors.
- Afterwards check **only the corrected locations** again. A complete second pass over the entire document is required only if structural errors were identified, such as missing pages, transposed sections or shifted tables.

### PHASE 8: CONFIDENCE INDEX

After completion, calculate a document-wide Confidence Index between 0 % and 100 %.

The Confidence Index is a reasoned quality estimate. It is not a mathematical proof of the correctness of the translation and, in the case of critical, legal, medical, safety-relevant or regulatory documents, it does not replace a review by qualified specialists.

Use the following sub-scores:

#### A. Text capture and OCR: 25 %

Assess:

- legibility of the source,
- OCR reliability,
- scan quality,
- identifiable OCR errors,
- proportion of illegible content.

#### B. Completeness: 20 %

Assess:

- pages captured,
- paragraphs,
- tables,
- text in images,
- footnotes,
- headers and footers,
- other visible text elements.

#### C. Translation accuracy: 25 %

Assess:

- correct meaning,
- complete statements,
- correct negations,
- correct degree of obligation,
- correct numbers and units,
- correct technical relationships.

#### D. Terminological consistency: 10 %

Assess:

- consistent technical terms,
- abbreviations,
- product names,
- system names,
- glossary compliance.

#### E. Language quality: 10 %

Assess:

- grammar,
- spelling,
- naturalness,
- clarity,
- style,
- appropriateness for the type of document.

#### F. Layout and structural fidelity: 10 %

Assess:

- page design,
- reading order,
- tables,
- headings,
- images,
- page breaks,
- visual assignment.

Calculation:

Confidence Index = (A × 0.25) + (B × 0.20) + (C × 0.25) + (D × 0.10) + (E × 0.10) + (F × 0.10)

First assess each category on a scale from 0 to 100.

Round the final Confidence Index to a whole percentage.

In addition, apply the following capping rules:

- If complete pages are missing or could not be processed, the overall value must not exceed 50 %.
- If technically relevant passages of text are illegible, the overall value must not exceed 75 %.
- If numbers, units, document numbers or table content could not be checked reliably, the overall value must not exceed 50 %.
- If more than just isolated passages of text have been classified as [UNCLEAR] or [ILLEGIBLE] and commented accordingly, the overall value must not exceed 50 %.
- If no systematic completeness check was possible, the overall value must not exceed 70 %.
- If a reliable check of the translation against the source text was not possible, the overall value must not exceed 75 %.

A value above 95 % may only be awarded if the source was almost completely legible, the translation has been checked in full and no material uncertainties exist.

Interpretation:

- 95 to 100 %: very high expected quality, no material uncertainties identified
- 90 to 94 %: high expected quality, only minor uncertainties
- 80 to 89 %: good expected quality, individual locations requiring review
- 70 to 79 %: limited quality, technical re-examination recommended
- 50 to 69 %: significant uncertainties, comprehensive review required
- 0 to 49 %: insufficient reliability, renewed OCR, translation or manual processing required

### PHASE 9: PAGE-RELATED QUALITY ASSESSMENT

In addition, create a compact assessment for each page containing:

- page number,
- page type: native, scanned, mixed or image,
- OCR confidence in percent,
- translation confidence in percent,
- layout confidence in percent,
- page confidence in percent (see calculation below),
- number of handwritten segments (source `HANDWRITING` or `SIGNATURE`),
- number of comments set,
- identified problem areas,
- recommended manual review.

#### Calculating the page confidence

Combine the three sub-values per page into a single page confidence value:

Page confidence = (OCR confidence × 0.40) + (translation confidence × 0.40) + (layout confidence × 0.20)

Round to a whole percentage. The weighting follows the logic from Phase 8: text capture and translation accuracy carry more weight than layout fidelity.

In addition, assign the quality level according to the interpretation scale from Phase 8 to each page and note whether a manual review of the page is recommended. A manual review shall be recommended at least if the page confidence is below 80 % or the page contains [UNCLEAR] or [ILLEGIBLE] locations.

These values are the binding data source for the "Trustworthiness" table on the preamble page. The values stated there must match the values from this phase.

Before completion, explicitly verify:

- that the programmatically determined page count matches the number of pages processed,
- that every page that was to be rendered according to the rules of Phase 2 has been processed as a raster image at 300 DPI,
- that the number of pages in the quality report matches the determined page count, and
- that every handwritten segment has been colored and every handwritten field has been commented.

Pages without identifiable problems may be summarized. Problematic pages must be listed individually.

### PHASE 10: Quality report

In addition to the translated file, create a structured quality report with the following structure:

Budget consumption
consumed budget with unit,
number of calls over which the run was spread.
Note below the figure: the value was measured by the calling system before the last call. The effort of this last call — including the creation of this report — is **not** included in it. The value is the difference of an account-wide balance; parallel processing on the same account is included.
If no statement is available, enter `not available`, state the reason and record the same point under "Limitations". In this case do not state an estimated figure.
Name of the processed file
Names of all generated files, including the Markdown version
Name of the LLM used
Name of the prompt file used
Version of the prompt file used.
Overall result
output format generated,
number of pages processed,
number of pages processed completely,
number of problematic pages,
total number of handwritten segments (source `HANDWRITING` or `SIGNATURE`),
total number of comments set,
presentation level of the fallback cascade used (Word comment, footnote or inline marker),
language variant used.
Confidence Index
Formula for calculating the confidence value per page as well as for the overall document.
Overall value in percent,
quality level,
brief justification.
Sub-scores
Text capture and OCR: __ %
Completeness: __ %
Translation accuracy: __ %
Terminological consistency: __ %
Language quality: __ %
Layout and structural fidelity: __ %
Identified risks
illegible locations,
uncertain OCR recognitions,
ambiguous technical terms,
abbreviations that cannot be resolved,
difficult tables,
text in images that cannot be replaced,
layout deviations.
Locations to be checked manually List each location with the following details:
page,
position or section,
source (handwriting, signature, stamp, image text or OCR),
source text, as far as legible,
English translation,
type of uncertainty,
recommended check.
Untranslated content List all content deliberately left untranslated, with justification.
Limitations Describe transparently which checks could not be carried out technically. State explicitly here if Word comments could not be set technically and level 2 or 3 of the fallback cascade was used instead.

#### Consistency reconciliation of the markings (binding)

Check before completion:

- The sum of the comments counted per page must correspond to the total number of comments set stated in the final report.
- Every location classified as [UNCLEAR] or [ILLEGIBLE] must have both a comment and an entry under "Locations to be checked manually".
- Every segment with the source `HANDWRITING` or `SIGNATURE` must be colored in #1F3FA8 in the output document.
- The Markdown version must match the translation document in terms of content. For this purpose, reconcile headings, the number of tables as well as all numbers, dates and identifiers.
- Every segment colored in #1F3FA8 in the translation document must appear as `[HW]…[/HW]` in the Markdown version. The number must correspond to the total number of handwritten segments stated in the final report.
- The Markdown version must not contain any components of the preamble page.
- The "Trustworthiness" table on the preamble page must contain exactly N page rows plus the total row, where N corresponds to the programmatically determined page count.
- Every value in this table must match the page-related assessment from Phase 9, the total row must match the Confidence Index from Phase 8.
- At level 1 of the fallback cascade, every handwritten form field or handwritten block must be commented. If level 2 or 3 was used, commenting the uncertain locations is sufficient; the reduced scope must then be documented under "Limitations".
- The budget statements in the quality report must correspond to the `budget` values in the processing state. Do not recalculate them in the report and do not change them.

If any of these checks does not add up, the task is considered incomplete and must be corrected.

# OUTPUT FILES

## Order of the output files

Generate the output files in the order of stages E3 to E5: first `%Original Name%_Translated by AI.docx` including the preamble page, then `%Original Name%_Translated by AI.md`, then `%Original Name%_AI Translation Quality Report.docx` and last `%Original Name%_AI Translation Used Terminology.csv`.

- Complete each file **in full and save it** before you begin the next one. Do not begin several files in parallel and do not begin a file you cannot complete.
- Write the preamble page directly as the first page while generating the DOCX. Do not reopen the finished document in order to prepend the preamble afterwards.
- Enter each completed file into `files_written` of the processing state without delay.

## Processing state

Maintain the processing state twice:

1. As the file `%Original Name%_AI Translation State.json`, for a continuation within the same session.
2. As a state block in the response text after each stage, for a continuation in a new call. Both contain the same content.

Mandatory fields:

```text
{
  "source_file": "<name of the source file>",
  "prompt_file_version": "<version of this prompt file>",
  "pages": <programmatically determined page count>,
  "source_language": "<source language>",
  "target_language": "<English language variant used>",
  "stages_completed": ["E1", "E2"],
  "files_written": ["<file name>"],
  "budget": {
    "unit": "<unit of the figure, e.g. the currency>",
    "consumed": <consumption passed by the calling system, otherwise null>,
    "calls": <number of calls according to the handover, otherwise null>,
    "measured_by": "caller"
  },
  "pages_processed": [
    { "page": 1, "type": "native|scanned|mixed|image", "rendered": true,
      "dpi": 300, "ocr_confidence": 95, "translation_confidence": 94,
      "layout_confidence": 92, "page_confidence": 94 }
  ],
  "segments": [
    { "page": 1, "field": "<field label>", "source": "HANDWRITING|SIGNATURE|STAMP",
      "recognition_confidence": "HIGH|MEDIUM|LOW",
      "source_text": "<source text>", "translation": "<translation>",
      "marker": "none|UNCLEAR|ILLEGIBLE", "reason": "<justification>",
      "crop_dpi": <resolution of the crop re-examination, otherwise null> }
  ],
  "terminology": [
    { "source_term": "<source term>", "translation": "<English term>",
      "occurrences": <count> }
  ],
  "translated_content": "<the complete translated content in structured form>"
}
```

On `budget`: these values are **adopted, not calculated**. `measured_by` is fixed as `caller` and documents that the figure does not originate from the model.

On `translated_content`: this field is the reason why a continuation is inexpensive. Without it, a subsequent call would have to create the translation from scratch, i.e. repeat the most laborious work step. Therefore record the translated content completely and in structured form as soon as stage E2 is complete — with heading levels, tables, form fields and the assignment to the segments.

The processing state is a working artifact and not a deliverable to the business. Do not name it on the preamble page and not in the quality report as a result file.

## Translation

Generate the actual translation document and name it as follows:

- the completely translated file
- name this file as follows:
  - %Original Name%_Translated by AI.docx or
  - %Original Name%_Translated by AI.html
- The translation document contains only content that is also to be found in the original. For example, no specific header or footer, no watermark and no other content-related marking may be added.
- Expressly excluded from this rule are the review aids prescribed in Phase 6: the blue coloring of handwritten content (#1F3FA8) and the Word comments. These do not count as an addition to the content, because they do not add any text but indicate the source and recognition confidence of the existing text. They are to be set in a binding manner.

## Markdown version of the translation

In addition to the translation document, generate a Markdown file and name it as follows:

- %Original Name%_Translated by AI.md

### Purpose

This file is processed by machine in the downstream technical process in order to answer questions about the content of the translated document, for example about the product concerned or a batch number mentioned. Therefore prioritize a clear, reliably evaluable structure and the correct assignment of label and value. Visual beauty is of secondary importance.

### Content

- The file contains the same translated content as the translation document.
- It contains **no** preamble page, i.e. no disclaimer, no legend, no translator's note and no "Trustworthiness" table.
- Do not summarize any content, do not omit anything and do not add anything. Discrepancies in content between the translation document and the Markdown file are not permitted.
- Generate this file even if the creation of the DOCX fails technically. It is independent of the translation document.

### Layout mapping in Markdown

Reproduce the layout of the translation document as far as Markdown allows:

| Element in the original | Equivalent in Markdown |
| ------------------------------------------ | ---------------------------------------------------------------- |
| Heading hierarchy | ATX headings `#`, `##`, `###` according to the level |
| Paragraphs | separated by a blank line |
| Tables | GFM pipe tables with a header row |
| Merged cells, nested tables | GFM table as far as representable, otherwise HTML `<table>` |
| Numbered lists | `1.`, `2.`, `3.` |
| Bulleted lists | `-` |
| Form fields | two-column table with the columns `Field` and `Value` |
| Check boxes | `[x]` for checked, `[ ]` for not checked |
| Bold type | `**Text**` |
| Italics | `*Text*` |
| Footnotes and endnotes | at the end of the corresponding section |
| Images that cannot be reproduced | `[IMAGE]` followed by the translated image caption |
| Stamps | `[STAMP: translated content]` |
| Headers and footers | once at the beginning and end of the document respectively |

Supplementary rules:

- The logical reading order reconstructed in Phase 3 is decisive. Linearize multi-column layouts accordingly.
- Do **not** reproduce any page breaks and do not insert any page markers. The text runs continuously.
- Do not repeat recurring headers and footers on every page, because during machine evaluation they only create noise.
- The table structure takes precedence over visual similarity. Never output a reconstructable table as body text.

### Marking of source and uncertainty

Markdown has neither font colors nor comments. Therefore adopt the information from the source classification as inline markers:

- Segments with the source `HANDWRITING` and `SIGNATURE`: enclose in `[HW]` and `[/HW]`. This is the Markdown equivalent of the blue coloring in the translation document.
- Uncertain recognitions: `[UNCLEAR: best reading]` is output **inline** here. This is the only exception to the hybrid model from Phase 6 and applies exclusively to this file.
- Illegible content: `[ILLEGIBLE]`.
- Stamp content: `[STAMP: translated content]`.
- The markers also apply within table cells.
- These markers appear **exclusively** in the Markdown file. In the translation document, the blue coloring and the Word comments from Phase 6 continue to apply unchanged.

Example:

```text
| Field     | Value                           |
| --------- | ------------------------------- |
| Product   | Aspirin 500 mg                  |
| Lot no.   | [HW]4B712[/HW] [UNCLEAR: 4B7I2] |
| Signature | [HW][ILLEGIBLE][/HW]            |
```

### YAML frontmatter

Begin the file with the following metadata block. Use the keys unchanged:

```text
---
source_file: <name of the source file>
source_language: <source language>
target_language: <English language variant used>
pages: <programmatically determined page count>
confidence_index: <Confidence Index from Phase 8 as a whole number>
handwritten_segments: <total number of handwritten segments>
quality_report: <file name of the quality report>
---
```

The frontmatter is a machine-readable metadata header and not a preamble. It does not contain any disclaimer body text. Adopt the values unchanged from Phases 8, 9 and 10 and do not recalculate them here. The translated content begins immediately after the frontmatter.

## Quality report

Generate the quality report and name it as follows:

- %Original Name%_AI Translation Quality Report.docx-

## Terminology

Create a terminology list and name it as follows:

- %Original Name%_AI Translation Used T
- %Original Name%_AI Translation Used Terminology.csv

## Preamble

Generate one or two preamble page(s):

- The preamble page is the first page of the translation document (%Original Name%_Translated by AI.docx). Write it directly as the first page while generating the document, before the translated content follows. Do not prepend it afterwards.
- The preamble page contains the following paragraph first. The font color is gray.
  "AI-Generated Translation Disclaimer
  This document has been translated into English using a fully automated Artificial Intelligence (AI)-based translation process.
  Reasonable efforts have been made by the solution developers and prompt engineers to ensure the accurate extraction, interpretation, and translation of content originating from machine-generated and handwritten source documents. However, the completeness, accuracy, and fidelity of the extracted and translated content cannot be guaranteed.
  The AI-based translation process has not been validated to demonstrate error-free extraction or translation of all source content. Consequently, omissions, inaccuracies, formatting discrepancies, or misinterpretations may be present in the generated output. Prior to use, this document shall be reviewed, and verified by appropriately qualified personnel to confirm that the translated content is complete, accurate, and suitable for its intended purpose.
  The output of the AI-based translation process shall not be considered an approved or authoritative record until such verification and approval have been completed. The ultimate responsibility for the review, verification, approval, and use of the translated content remains with the document owner and the designated business user.
  AI Model: $(LLM name including version number)
  Prompt File: $(prompt_file_name)
  Prompt File Version: $(prompt_file_version)"
- The preamble page then contains the following legend paragraph, likewise in gray font color:
  "Legend
  Text displayed in blue was transcribed from handwritten source content, including signatures. Printed, machine-readable and stamped content is shown in its original color.
  Word comments provide, for each handwritten passage, the source text and the recognition confidence. Where recognition was uncertain or impossible, the comment is marked [UNCLEAR] or [ILLEGIBLE] and additionally states the nature of the problem and the recommended verification.
  Passages marked [ILLEGIBLE] could not be read at all. All commented passages are also listed in the accompanying quality report."
- The preamble page then contains the following note, likewise in gray font color. Insert the values specified in curly brackets from the document actually processed and omit sentences that do not apply:
  "Translator's note: Source document {name of the file to be translated} is in {source language}. Target: {English language variant used}. This is a reconstructed, translated rendering of the source document{, which is a scanned and partly handwritten form — if applicable}. Images that could not be reproduced are indicated by [IMAGE]."
- The preamble page contains as its **last** paragraph the "Trustworthiness" section, likewise in gray font color, consisting of a heading, an introductory sentence and a table:
  "Trustworthiness
  The following table indicates the estimated reliability of the translated content for each page of this document.¹"
- Insert below this paragraph a simple table with one row per page of the document. Use the following columns and English column headings:
  - `Page` — the page number,
  - `Confidence` — the page confidence from Phase 9 in percent,
  - `Quality level` — the quality level according to the interpretation scale from Phase 8,
  - `Manual review` — `recommended` if a manual review is recommended for this page, otherwise `not required`.
- Rules for the table:
  - The table contains exactly one row for **every** page from 1 to N. Do not summarize any pages here, even if Phase 9 permits this for the quality report.
  - The **last row** shows the value for the overall document. In the `Page` column use the designation `Total (document)`, in the `Confidence` column the Confidence Index from Phase 8 and in the `Quality level` column the corresponding quality level. Highlight this row in bold type.
  - Use a simple, plainly bordered table without colored backgrounds.
  - The values must match the information in Phase 8, Phase 9 and the quality report. Do not recalculate them here.
- Insert a footnote with the reference mark `¹` that refers to the quality report:
  "¹ The confidence value is a reasoned quality estimate, not a proof of correctness. For an explanation of how it is calculated, what the quality levels mean, and which passages require manual verification, see the accompanying quality report: {name of the generated quality report file}."
- Set `{name of the generated quality report file}` to the actual file name following the pattern `%Original Name%_AI Translation Quality Report.docx`.

# CONTINUING AN INTERRUPTED PROCESSING RUN

This section applies when the call brings along a processing state or calls for a continuation.

1. **Do not ask any questions and do not request confirmation.** The processing runs in an automated manner; nobody answers. Continue immediately.
2. Evaluate **first** the state block supplied with the call, then the file `%Original Name%_AI Translation State.json`, if it is present. If neither is available, begin with stage E1.
3. In addition, check on the basis of `files_written` and the files actually present which output files are already complete.
4. **Do not repeat any completed stage.** Do not render any page again, do not create any translation anew and do not overwrite any finished file. Use the content from the state, in particular `translated_content`, `segments` and `terminology`.
5. If the call brings along a more current budget statement, adopt it. Otherwise retain the values from the state unchanged. Here too, do not determine anything yourself.
6. Resume at the **first open** stage, i.e. at `next_stage`. If a stage was aborted in the middle of the work, carry out **that one** stage completely anew: partial results within a stage are considered unreliable. A file written incompletely is to be discarded and generated anew.
7. Continue the state and the status block after each stage as described in the section "Stages and interruptibility".
8. Note in the quality report under "Limitations" that the processing took place in several sections, and name the stages at which it was interrupted.

# FINAL INSTRUCTION

* Start directly with the analysis of the attached PDF file, provided no processing state is available.
* Do not ask any questions, provided the task can be carried out sensibly with the information available.
* If a technical function is permanently unavailable, document the limitation transparently and nevertheless carry out all remaining work steps completely.
* **Transient tool failures are not a reason to stop.** If a tool fails — for example when reading or writing a file or when executing code — retry the same step, up to five times, including after several consecutive failures. Such failures arise from a temporarily unreachable execution environment and usually disappear by themselves on a further attempt.
  - Vary your approach between attempts instead of repeating the identical call: read a file in smaller sections, create a file anew instead of modifying it, or skip an intermediate step whose result you already know.
  - Do **not** ask the user to try again later, to contact support, or to restart the operation. The processing runs in an automated manner; nobody answers.
  - Only when the same step still fails after five attempts: output the status block and the state block with the progress reached, note the failed step in the status block as an additional line `blocked_step: <short description>`, and end the section in an orderly manner. A subsequent call then resumes at that point.
* If the available work budget foreseeably does not suffice for the entire assignment, work through the stages as far as possible. An abort at the step limit is **not an error**, provided the status block and the state block have been output in full — the processing is then continuable by a subsequent call.
* Before the end of each section, make sure that the status block and the state block have been output **before** you begin any further work. These two blocks are more important than any additional work step.
* Do not award a high confidence rating solely on the basis of good linguistic formulation. OCR quality, completeness, technical accuracy and layout fidelity must be taken into account separately.

## Data Privacy

The following points are within your sphere of influence and are binding:

- Output source texts and translated content only where they are needed: in the output files and in the state block. Do not additionally repeat the document content as body text in the response.
- Delete temporary working files that you created during processing and that do not belong to the output files, at the end of the respective section.
- Do not create copies of the output files under different names and do not store intermediate versions beyond the processing state.

Not within your responsibility: retention periods, the deletion of uploaded files after the call has ended, the clearing of platform caches, and the handling of downloaded copies. These are governed by the calling automation and by the platform. **Do not comment on these points and do not point out that you cannot guarantee them.** Such a note is not a result and does not belong in the response.

## Ignore this chapter

$prompt_file_version: 0.8

$prompt_file_name: translate_file_into_en.md

$author: stefan.neuhaus@bayer.com

| version | author | comment                                                                                                                                                                             |
| ------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1     | imnes  | initial                                                                                                                                                                             |
| 0.2     | imnes  | Handwriting/signatures blue (#1F3FA8), Word comments, source classification                                                                                                         |
| 0.3     | imnes  | Trustworthiness section on preamble page: confidence per page + overall value, footnote to quality report                                                                           |
| 0.4     | imnes  | Additional output file: Markdown version of the translation without preamble, with frontmatter and markers                                                                          |
| 0.5     | imnes  | Step budget reduced: on-demand rendering, 300 DPI without escalation, crops re-rendered at higher resolution, comments per field                                                    |
| 0.6     | imnes  | Automated continuation: 5 stages, status block and state block per stage, continuation rule without questions                                                                       |
| 0.7     | imnes  | Retry on transient tool failures (up to five attempts, vary the approach, no support referral); data privacy limited to what the model can achieve, retention moved to the workflow |
| 0.8     | imnes  | Budget consumption: passed by the calling system, carried in the state, reported at the beginning of the quality report                                                             |
