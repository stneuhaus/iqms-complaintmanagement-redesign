# n8n Hub instance

Status: In use (personal-only — see [`README.md`](README.md) for why)
Last reviewed: 2026-11-05

Connects an AI client to the Bayer n8n Hub instance via MCP, so workflows can be read and built
directly instead of exporting/importing JSON.

## Prerequisites

Per the Hub documentation (*Establishing MCP Access for Citizen Developers via Hub Instance*):

- An approved n8n Hub account with the right project roles
- An approved use case
- A managed device
- **Instance-level MCP** enabled in the Hub settings
- The target workflow **explicitly shared for MCP** — project permission alone is not enough

```
Effective MCP access = your n8n permissions ∩ workflows explicitly enabled for MCP
```

A workflow you can see in the n8n UI but not via MCP almost always means it isn't shared for MCP.

## Server details

| | |
| --- | --- |
| Name | `n8n-mcp` |
| URL | `https://dev.citizen.n8n.int.bayer.com/mcp-server/http` |
| Transport | HTTP (streamable, `text/event-stream`) |
| Auth | `Authorization: Bearer <token>` |
| Server | n8n MCP Server 1.1.0, protocol `2025-06-18` |

This points at the **Dev** Citizen instance on purpose — build and test here first, never
directly in production.

## Setup

### 1. Get a token

n8n Hub portal → **Settings** → **Instance-level MCP** → **Connection details**. Copy the server
URL and the access token from there.

### 2. Set the token

```powershell
[Environment]::SetEnvironmentVariable('N8N_MCP_TOKEN', '<token>', 'User')
```

Restart your terminal / IDE afterwards so the new process environment picks it up.

### 3. Add the server

```bash
claude mcp add n8n-mcp --scope user --transport http \
  https://dev.citizen.n8n.int.bayer.com/mcp-server/http \
  -H 'Authorization: Bearer ${N8N_MCP_TOKEN}'
```

> **The token is a bearer secret tied to your identity.** Whoever has it has your MCP access —
> there is currently no per-client restriction. Never put it in a repo file, chat, or ticket. If
> it leaks anyway: revoke and reissue it in the Hub.

### 4. Verify

```bash
claude mcp list
```

`n8n-mcp` should show `✔ Connected`. Functional check:

```bash
curl -s -X POST "https://dev.citizen.n8n.int.bayer.com/mcp-server/http" \
  -H "Authorization: Bearer $N8N_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}'
```

Expect `serverInfo` with `"name":"n8n MCP Server"`. `{"message":"Unauthorized"}` means the token
is expired, revoked, or unset.

## What the server offers

Tools for building workflows with the **n8n Workflow SDK** — the SDK reference
(`get_workflow_sdk_reference`), per-technique best practices (`get_workflow_best_practices`), and
node search (`search_nodes`). The server's own instructions require reading the SDK reference
**before** writing workflow code — don't guess SDK syntax.

## Limits that apply to this project

- Every AI-generated workflow change is reviewed before saving — that's Hub policy, not a style
  choice.
- Production automation does not run under a personal identity; that needs a service account.
  This token is personal and for development only.
- The sandbox workflow in `n8n/sandbox/` stays the source of truth until the design spec is
  agreed — MCP doesn't replace review in this repo.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `{"message":"Unauthorized"}` | Token missing, expired, or revoked — get a new one |
| `${N8N_MCP_TOKEN}` shows up literally in the header | Variable wasn't set when the client started — set it, restart the editor |
| Connected, but no workflows visible | Workflow not shared for MCP, or missing project role |
| Workflows readable but not editable | Missing **MCP Builder** permission |

Further support: Slack `#n8n-hub-support`.

## Related

- [`README.md`](README.md) — shared Bayer proxy/certificate notes (not needed for this server;
  it's reachable without the proxy workaround)
- `n8n/sandbox/README.md` — the OCR+Transform sandbox workflow
- `docs/06-decisions/adr-001-n8n-platform.md` — n8n as the automation platform
