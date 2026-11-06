# Azure DevOps

Status: In use (personal-only — see [`README.md`](README.md) for why)
Last reviewed: 2026-11-05

Connects an AI client to one or more Azure DevOps organizations via MCP, to read and edit work
items directly instead of switching to the browser.

## Package

`@tiberriver256/mcp-server-azure-devops` (via `npx`, no global install), stdio transport, PAT
auth. Chosen over the official `@azure-devops/mcp` because that package is built around the Azure
CLI credential chain, and the Azure CLI isn't installed on these machines.

**One server process serves exactly one organization.** That's not a package limitation — Azure
DevOps PATs are organization-bound, so a token for one org is worthless in another. Each
organization you want needs its own server entry, its own PAT, and its own env var name.

## Known servers (check `claude mcp list` for the current, authoritative set)

| Name | Org | Project | PAT env var |
| --- | --- | --- | --- |
| `azure-devops-bayer` | `ValDevOps-1` | `IQMS` | `ADO_PAT_BAYER_IQMS` |
| `azure-devops-clara` | `ValDevOps-P` | `CLARA` | `ADO_PAT_CLARA` |
| `azure-devops-privat` | `stefanneuhaus` | `imnestest` | `ADO_PAT_STEFANNEUHAUS` |

**Don't add a second entry for an org/project you already have.** `azure-devops-bayer` already
covers `ValDevOps-1`/`IQMS` — there's no separate `azure-devops-iqms` server, even though that
was this project's internal name for the same target while it was still declared in `.mcp.json`.
Run `claude mcp list` before adding a new org to avoid a duplicate under a different name.

## Setup (per organization)

### 1. Node on the Bayer proxy

See [`README.md`](README.md#bayer-proxy-and-certificates) — this step is the actual hurdle and
applies to every npm-based tool on a Bayer device, not just this one.

```powershell
[Environment]::SetEnvironmentVariable('NODE_OPTIONS', '--use-system-ca', 'User')
```

Setting it system-wide also helps every other npx-based tool; the server's own `env` block below
sets it again explicitly so it works even without this step.

### 2. Generate a PAT

`https://dev.azure.com/<org>/_usersSettings/tokens` → **New Token**.

- Scope: **Work Items → Read & write**. Nothing broader, especially not "Full access".
- Lifetime 90 days — note the expiry date; the server fails silently with `401` once it's gone.

### 3. Set the PAT

```powershell
[Environment]::SetEnvironmentVariable('ADO_PAT_<NAME>', '<token>', 'User')
```

Restart your terminal/IDE completely afterwards — the MCP server is spawned by the client, not
your shell, and won't inherit a variable set after it started.

> **The PAT carries your identity in Azure DevOps.** Whoever has it can read and change work
> items as you. Never in a repo file, chat, or ticket. If it leaks: revoke and reissue in the
> token settings.

### 4. Add the server

```bash
claude mcp add azure-devops-<name> --scope user \
  -e AZURE_DEVOPS_ORG_URL=https://dev.azure.com/<org> \
  -e AZURE_DEVOPS_DEFAULT_PROJECT=<project> \
  -e AZURE_DEVOPS_AUTH_METHOD=pat \
  -e AZURE_DEVOPS_PAT='${ADO_PAT_<NAME>}' \
  -e HTTPS_PROXY=http://10.185.190.10:8080 \
  -e NODE_USE_ENV_PROXY=1 \
  -e NODE_OPTIONS=--use-system-ca \
  -e NO_PROXY=localhost,127.0.0.1 \
  -- npx -y @tiberriver256/mcp-server-azure-devops
```

`AZURE_DEVOPS_ORG_URL` takes only the organization part of the URL — the project goes in
`AZURE_DEVOPS_DEFAULT_PROJECT` separately:

| Browser URL | `AZURE_DEVOPS_ORG_URL` | `AZURE_DEVOPS_DEFAULT_PROJECT` |
| --- | --- | --- |
| `https://dev.azure.com/ValDevOps-P/CLARA` | `https://dev.azure.com/ValDevOps-P` | `CLARA` |

Setting the full URL as `ORG_URL` makes every API call fail silently against the wrong path.

### 5. Verify

```bash
claude mcp list
```

Should show `✔ Connected`. Then check functionally: read a known work item by ID, make a test
edit to a Description field on a throwaway item, and confirm it in the browser.

## Why `--use-system-ca` and not `NODE_TLS_REJECT_UNAUTHORIZED=0`

Without the proxy settings from step 1, even `npm install` fails:

```
npm error code UNABLE_TO_VERIFY_LEAF_SIGNATURE
npm error reason: unable to verify the first certificate
```

Cause: `~/.npmrc` routes npm through the Bayer proxy (`http://10.185.190.10:8080`), which
terminates TLS and re-signs with a Bayer root certificate. That certificate lives in the Windows
certificate store, but Node by default only trusts its own bundled CA list and doesn't know about
it. `--use-system-ca` (Node 22.15/23+) makes Node read the Windows store too.

`NODE_TLS_REJECT_UNAUTHORIZED=0` is deliberately **not** used anywhere in this setup: it doesn't
fix the underlying trust gap, it turns certificate verification off entirely, so the process can
no longer distinguish the expected proxy from a real man-in-the-middle — and this process carries
a PAT. `~/.npmrc`'s existing proxy entries and `strict-ssl: true` stay untouched.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `UNABLE_TO_VERIFY_LEAF_SIGNATURE` at startup | `NODE_OPTIONS=--use-system-ca` missing — step 1, then restart the client |
| `401 Unauthorized` | PAT expired, revoked, or unset — reissue |
| `${ADO_PAT_<NAME>}` shows up literally as the token | Variable wasn't set when the client started — set it, restart the editor |
| Connected, but work items aren't found | `AZURE_DEVOPS_ORG_URL` accidentally contains the project name — see table above |
| Reads work, writes fail | PAT only has `Read`, not `Read & write` |

## Related

- [`n8n.md`](n8n.md) — same token-via-env-var pattern
