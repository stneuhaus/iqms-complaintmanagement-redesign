# Design specification

Status: Later  
Last reviewed: 2026-09-18

Fill this **after** architecture and the functional specification exist.

This document states **how** the solution will be built: n8n workflows, integrations, error handling, and operational concerns.

Exported workflow JSON belongs in `/workflows`, not in this file.

## Contents

| File | Purpose |
| --- | --- |
| [design-specification.md](design-specification.md) | Main design specification (to be filled) |
| [promtpts for text recogniztion/](promtpts%20for%20text%20recogniztion/README.md) | Translation prompt — German master plus versioned English translations, and the rule that every English change becomes a new file |
| [resume-loop.md](resume-loop.md) | What the **n8n workflow** must do so the translation prompt completes after a step-limit interruption |
| [manual-test.md](manual-test.md) | How to run the same prompt **by hand** in myGenAssist, including what to do on an interruption |
