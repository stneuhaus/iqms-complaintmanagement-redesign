# Spec — n8n ↔ ChatGPT-class LLM translation (GxP content)

**Status:** draft for decision (repo-less idea)  
**Date:** 2026-09-21  
**Data classification:** `gxp` (confirmed by requester)  
**Contrast to prior sketch:** Azure Translator (deterministic MT, `internal`) → LLM (generative), GxP controls dominate.

---

## Verdict (read this first)

**Do not** send GxP text to consumer ChatGPT (`chat.openai.com` / public OpenAI API) from n8n.

**Do** (if LLM translation is still required):

1. Call Bayer’s **myGenAssist (BayChatGPT)** via its **API** (same family of models, in-estate GenAI surface).
2. Treat every output as a **draft** — **human-in-the-loop (HITL)** before any GxP-controlled use.
3. Log prompt, model version, input/output hashes, and reviewer decision ([Governed AI](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/ea/TA03-governed-ai.md)).
4. Declare `data-classification: gxp` on the catalog entry ([G-DATA-CLASS](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-DATA-CLASS.md)).

Unsupervised “LLM translates → write back to controlled record” is **not** aligned with Bayer AI guidance (“AI can and will be wrong… review any of its output” — [AI Dev Tools Security](https://backstage.int.bayer.com/docs/default/component/ai-dev-tools-docs/security/security/)) or content-safety HITL ([Content Safety](https://backstage.int.bayer.com/docs/default/component/agentic-ai-docs/architecture/components/governance-framework/content-safety/)).

---

## 1. Reuse first

| Option | Verdict | Grounding |
| --- | --- | --- |
| Public ChatGPT / raw OpenAI.com | **Reject for GxP** | Controlled/Secret data → check tool approval ([Security](https://backstage.int.bayer.com/docs/default/component/ai-dev-tools-docs/security/security/)); public ChatGPT is not a cataloged Bayer GxP path |
| **myGenAssist (BayChatGPT)** API | **Preferred GPT surface** | Bayer GenAI platform; API usable from automation ([MyGenAssist Integration](https://backstage.int.bayer.com/docs/default/component/cloud-docs/general/how-to/mygenassist-integration/) — `bayer-int/mygenassist-action`); named BayChatGPT in [ADR-0010](https://backstage.int.bayer.com/docs/default/component/ai-dev-tools-docs/architecture-agent/design/decisions/0010-mygenassist-as-internal-chat-surface/) |
| CS CX AI agent + myGenAssist model | Alternative compose path | Multi-model support includes myGenAssist ([Getting Started](https://backstage.int.bayer.com/docs/default/component/cs-cx-ai-platform/01-getting-started/)) |
| Self-hosted LLM on EKS | Fallback if estate GPT not approved for GxP residency | [cs-cx-sre-selfhost-ai-model](https://github.com/bayer-int/cs-cx-sre-selfhost-ai-model/tree/main/catalog-info.yaml) (vLLM + gateway) |
| Langfuse | Observability (not the translator) | [langfuse](https://github.com/bayer-int/langfuse/tree/main/catalog-info.yaml) — “Open Source LLM Engineering Platform for Bayer”; enable tracing per AI platform docs |
| Phoenix i18n | Wrong job | UI string catalog, not free-text MT |

---

## 2. Governing standards (GxP + AI)

| Standard | Modality | Design implication |
| --- | --- | --- |
| [G-DATA-CLASS](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-DATA-CLASS.md) | must | Label `gxp` — scopes privacy/residency rules onto the flow |
| [G-ADR](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-ADR.md) | must | Record LLM-vs-MT and HITL decision |
| [G-CATALOG](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-CATALOG.md) | must | Place the automation when it becomes a lasting asset |
| [Governed AI (TA03)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/ea/TA03-governed-ai.md) | should | Log inputs/outputs/model version; escalate outside pre-approved policy |
| [Zero Trust (TA01)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/ea/TA01-zero-trust.md) | should | Authenticate every call; least privilege; audit |
| [AI-First, Human-Centric (P01)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/P01-ai-first-human-centric.md) | should | Humans own outcomes; agents compose — HITL fits |

Also apply: content-safety HITL ([Content Safety](https://backstage.int.bayer.com/docs/default/component/agentic-ai-docs/architecture/components/governance-framework/content-safety/)); human–AI collaboration patterns ([Human-AI Collaboration](https://backstage.int.bayer.com/docs/default/component/agentic-ai-docs/architecture/components/user-experience/human-ai-collaboration/)).

**Hard Quality caveat (outside landscape but material):** Machine/LLM translation of GxP-controlled wording is typically **draft assist**, not a validated linguistic process. Quality/CSV sign-off is required before treating English output as controlled content.

---

## 3. Design (n8n + myGenAssist)

```
[Trigger] → [Extract text] → [GxP gate / purpose check]
        → [HTTP: myGenAssist API — pinned model + prompt, temp≈0]
        → [Langfuse / audit record]
        → [HITL: SME approve / edit / reject]
        → [Only if approved: downstream GxP use]
```

### 3.1 LLM call (ChatGPT-class, in-estate)

- **Endpoint:** myGenAssist API (automation pattern: [mygenassist-action](https://backstage.int.bayer.com/docs/default/component/cloud-docs/general/how-to/mygenassist-integration/)).
- **n8n:** HTTP Request with Entra/service credentials in Credentials store (not flow JSON).
- **Prompt:** dedicated “translate to English, preserve meaning, no elaboration” system prompt; **temperature near 0** (same doc recommends low temp for reliable outputs).
- **Pin:** model id + prompt version id in every audit row (TA03 lineage).
- **Do not** enable tools/browsing that could exfiltrate GxP context.

### 3.2 Mandatory GxP controls in the flow

| Control | Implementation |
| --- | --- |
| Classification | Flow/system tagged `gxp`; reject payloads that fail purpose check |
| No auto-release | Wait node / approval task / ticket — reviewer must accept English draft |
| Audit | Store: source hash, prompt version, model version, raw LLM output, reviewer id, decision, timestamp |
| Observability | Langfuse project for traces ([Getting Started · Enable Observability](https://backstage.int.bayer.com/docs/default/component/cs-cx-ai-platform/01-getting-started/)) |
| Retention | Align retention of prompts/outputs with GxP record retention (confirm with Quality) |
| Secrets | Key Vault / n8n credentials — never hard-code |

### 3.3 Explicit non-goals

- Consumer ChatGPT as the LLM host  
- Auto-updating IQMS/controlled documents with unreviewed LLM English  
- Using LLM as certified translation for regulatory submissions without Quality process  

---

## 4. Compliance callout

**Follows (intended):** G-DATA-CLASS (`gxp`), G-ADR, TA03 (traceability), TA01 (auth), P01 (human owns outcome), Content Safety HITL.

**Violates if built naively:** unsupervised LLM write-back to GxP records; public ChatGPT for Controlled Data without tool approval.

**Deviation path:** If Quality forbids LLM on GxP entirely → fall back to professional linguistic service or Azure Translator **with the same HITL**, and record ADR. Sign-off for G-ADR deviations: `@bayer-int/enterprise-architecture`.

---

## 5. ADR draft (summary)

Chosen: **myGenAssist API from n8n + mandatory HITL + Langfuse**, not public ChatGPT, because GxP requires in-estate GenAI, auditability, and human ownership of controlled content.
