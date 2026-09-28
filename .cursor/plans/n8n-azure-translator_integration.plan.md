# Spec — n8n ↔ Azure Translator (text / email / document translation to English)

**Status:** draft for decision (repo-less idea)  
**Date:** 2026-09-21  
**Assumptions (confirm before build):** content is Bayer-internal business text; target language English; translation is assistive (not certified/GxP linguistic validation); sync result needed in the same n8n run.

---

## 1. Reuse first

| Candidate | Verdict | Source |
| --- | --- | --- |
| Shared Bayer “translation-as-a-service” for automation | **Not found** in landscape | `find_prior_art` / `search_landscape` |
| n8n as cataloged Bayer platform | **Not found** | landscape search |
| Phoenix / Velocity Translation API | **Wrong job** — UI i18n message catalog, not machine translation of free text | [Using the Translation API](https://backstage.int.bayer.com/docs/default/component/clouddocs/general/phoenix/internationalization/api/); middleware [deprecated](https://github.com/bayer-int/phx-translation-api-middleware/tree/main/catalog-info.yaml) |
| AgrowSmart MS Translation bundle | **Adopt the pattern** — HTTP wrapper around Microsoft Translator Text API | [Ms Translation](https://backstage.int.bayer.com/docs/default/component/bayer-agrowsmart/apis/ms_translation/); component [agrowsmart](https://github.com/bayer-int/bayer-agrowsmart/tree/uat/catalog-info.yaml) owned by [nautilus](https://github.com/orgs/bayer-int/teams/nautilus) |

**Decision:** Reuse the **Microsoft Translator REST pattern** (AgrowSmart), not their app-specific Symfony bundle. Call Translator from n8n via HTTP Request. Aligns with [Reuse First (CP01)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/ea/CP01-reuse-first.md).

---

## 2. Governing standards (inputs to design)

| Id | Modality | How it shapes this design |
| --- | --- | --- |
| [G-ADR](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-ADR.md) | must | Choosing Translator + n8n is a significant tech/integration decision → commit an ADR when a product repo exists. Deviation sign-off: `@bayer-int/enterprise-architecture`. |
| [G-DATA-CLASS](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-DATA-CLASS.md) | must | Declare `data-classification` on the catalog entry for the flow/system; undeclared classification skips privacy/residency controls. |
| [G-CATALOG](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/guardrails/G-CATALOG.md) | must | When this becomes a lasting asset, place it in the catalog (owner + domain). |
| [GP-REGISTER-CONTROLLED-ASSET](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/golden-paths/GP-REGISTER-CONTROLLED-ASSET.md) | should | Seek reuse/collision guidance first; register in BEAT if it warrants its own application record. |
| [Zero Trust (TA01)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/ea/TA01-zero-trust.md) | should | Authenticate every Translator call; least-privilege keys; audit access. |
| [Composable Platforms (P02)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/P02-composable-platforms.md) / [Headless (P03)](https://github.com/bayer-int/impact-stack/blob/0220d60becc4b94060ddf6e83bf8bcda70a4a29a/architecture/principles/P03-headless-architecture.md) | should | Prefer a thin HTTP contract to Translator; avoid embedding MT logic only in UI. Long-term: consider a small reusable “translate” capability if multiple flows need it. |

**Placement note:** resolution ran root-anchored (`flaggedNeedsDomain`). Sharpen with a real domain (e.g. quality / automation) once the owning product is known.

---

## 3. Design

### 3.1 Target architecture

```
[Trigger] → [Normalize text] → [Data-class gate] → [HTTP: Azure Translator] → [Map result] → [Downstream]
                 ↑ secrets from Key Vault / n8n Credentials (never in flow JSON)
```

### 3.2 Azure side (SMART Azure)

1. In the team’s SMART Azure subscription, create resource **Azure AI Translator** (Cognitive Services / Translator) under a Resource Group. Portal / subscription basics: [Azure Basics](https://backstage.int.bayer.com/docs/default/component/cloud-docs/smart-azure/kb/how-to/AzureBasics/).
2. **Region:** prefer **West Europe** for EU-origin content (Bayer SMART Azure uses West Europe for Europe, East US 2 for NA — same doc). Match Translator region to content residency; document the choice in the ADR.
3. Prefer a **resource-specific endpoint** (`https://<name>.cognitiveservices.azure.com`) over the global endpoint when residency matters.
4. Auth: subscription key or Entra ID (managed identity / app registration). Store the key as a Key Vault secret — pattern from [Azure Key Vault (integration best practices)](https://backstage.int.bayer.com/docs/default/component/cloud-docs/api/mulesoft/integration-best-practices/azure-key-vault/). Do **not** hard-code credentials ([Azure Basics](https://backstage.int.bayer.com/docs/default/component/cloud-docs/smart-azure/kb/how-to/AzureBasics/) explicitly).
5. Inject into n8n via **Credentials** (or runtime pull from Key Vault if the host supports it). Rotate keys per vault practice.

### 3.3 n8n flow shape

| Step | Node | Behaviour |
| --- | --- | --- |
| 1 | Trigger | Webhook / email / file / schedule |
| 2 | Extract | Body text, subject, or document text (chunk if > API limit) |
| 3 | Gate | If classification is `pii` / `gxp` / regulated → **block or human path**; do not send by default (AgrowSmart docs: be mindful of sensitive data in text) |
| 4 | HTTP Request | `POST …/translator/text/v3.0/translate?to=en` with `Ocp-Apim-Subscription-Key`, optional `Ocp-Apim-Subscription-Region`, JSON body `[{ "text": "…" }]`. Optional `from=` or omit for auto-detect. |
| 5 | Parse | Read `translations[0].text`; keep `detectedLanguage` for audit |
| 6 | Errors | Retry on 429/5xx with backoff; fail flow on 401/403; log correlation id, never log full payload if sensitive |
| 7 | Optional cache | Hash(source+langs) → skip repeat calls (AgrowSmart best practice) |

**Documents (files):** use **Document Translation** (async: upload → poll → download) in a sub-flow, not the Text API. Emails/snippets stay on Text API.

**Prior-art contract (AgrowSmart):** inputs `text`, `sourceLang`, `targetLang` → translated text; env `MS_TRANSLATION_API_KEY`, `MS_TRANSLATION_ENDPOINT` — [Ms Translation](https://backstage.int.bayer.com/docs/default/component/bayer-agrowsmart/apis/ms_translation/).

### 3.4 Data classification

| Class | Recommendation |
| --- | --- |
| `internal` (assumed default) | Translator OK with EU region + secrets hygiene |
| `pii` | Prefer redact / anonymize first; or human translation; declare label per G-DATA-CLASS |
| `gxp` / validated docs | Machine translation is **not** a substitute for controlled linguistic process — out of this design |

### 3.5 Explicit non-goals

- Phoenix / Velocity i18n for free-text translation  
- Calling the AgrowSmart app API as a shared service  
- Building a new Bayer-wide translation platform in v1 (compose first; elevate to shared capability only if ≥2 consumers — P02 / CP01)

---

## 4. Compliance callout (design-time)

**Follows (intended):** G-ADR (ADR draft below), G-DATA-CLASS (declare when cataloged), TA01 (auth + least privilege + audit), CP01 (reuse MS Translator pattern), P02/P03 (HTTP contract).

**Gaps / risks:** n8n itself is **not** a cataloged Bayer golden-path orchestrator — justify n8n in the ADR or prefer an in-estate orchestrator if one is mandated for your org. Domain facet still unresolved → re-run standards with real domain before attestation.

**Does not apply yet:** G-CODEOWNERS / repo `.governance/` until a git product repo exists.

---

## 5. ADR draft

See companion section below (`0001-n8n-azure-translator.md` shape). Place in the product repo’s decisions folder when one exists; format from [templates/adr.md](https://github.com/bayer-int/ea-root-standards/blob/892c49ee3d1af593009b1181fa17ce31ed12dbd7/templates/adr.md).
