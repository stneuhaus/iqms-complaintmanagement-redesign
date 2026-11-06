# Veeva Vault AI MCP

Status: In use — **prerequisite on the Vault side unverified**, see below
Last reviewed: 2026-11-05

Connects an AI client live to a Veeva Vault instance's **Vault AI** agents — e.g. summarizing a
document or answering questions about one — instead of only reading static developer
documentation (that's [`veeva-vault-documentation.md`](veeva-vault-documentation.md)).

## Prerequisites — check these before expecting it to work

This only works if the target Vault has Vault AI licensed and configured. There is no way to
confirm this from the client side beyond trying it and reading the error:

- **Vault AI enabled** on the instance (Veeva: "only available to customers who have Vault AI
  enabled").
- At least one **Agent** with:
  - Agent status: **Active**
  - Action status: **Active**
  - Tool status: **Active**
  - Action **API Access**: **Yes** (only actions with this set appear in the MCP tool list)
- Your user has the permission sets:
  - **Application: API: Access API** (lets you generate an access token)
  - **Agents: Execute** (lets agent actions run as tools for you)

As of this writing, **whether the IQMS DEV sandbox
(`bayersbx-iqms-3-1-dev.veevavault.com`) meets these is not confirmed** — check with the Vault
admin, or just try the setup below: an empty `tools/list` after a successful connection means the
server is reachable but no active agent/action is exposed to you, not a configuration mistake
here.

## Server details

| | |
| --- | --- |
| Name | `vault-ai-<instance>` (e.g. `vault-ai-iqms-dev`) |
| URL | `https://{host}/api/ai/mcp` |
| Transport | HTTP |
| Auth | `Authorization: Bearer <access token>` — API access tokens only, **no** OAuth 2.0, **no** basic auth |
| Session | Expires 8 hours after initialization |
| Source | <https://general.veevavault.dev/mcp/vault-ai-mcp/> |

**The token is Vault-specific**: it's only valid for the Vault it was generated on. If the
token's Vault ID doesn't match the `{host}` in the URL, every request fails with `401
Unauthorized` — this is the most common setup mistake.

## Setup

### 1. Generate an access token

Vault UI → your user profile → generate an API access token (or via the Vault auth API — see
[Veeva's Help article on generating API access tokens](https://platform.veevavault.help/en/gr/7239)).
Copy it immediately; it cannot be retrieved again later.

### 2. Set the token

```powershell
[Environment]::SetEnvironmentVariable('VAULT_IQMS_DEV_ACCESS_TOKEN', '<token>', 'User')
```

Restart your terminal/IDE so the new process environment picks it up.

> **The token is a Vault-scoped bearer secret.** Whoever has it has your Vault AI access on that
> instance for up to 8 hours per session. Never in a repo file, chat, or ticket. If it leaks:
> regenerate it (the old one does not need explicit revocation if it already expired, but
> generate a fresh one and discard the old immediately if it's still live).

### 3. Add the server

```bash
claude mcp add vault-ai-iqms-dev --scope user --transport http \
  https://bayersbx-iqms-3-1-dev.veevavault.com/api/ai/mcp \
  -H 'Authorization: Bearer ${VAULT_IQMS_DEV_ACCESS_TOKEN}'
```

For a different Vault instance, repeat with a new server name, host, and env var — same pattern
as the multi-org Azure DevOps setup in [`azure-devops.md`](azure-devops.md).

### 4. Verify

```bash
claude mcp list
```

Should show `✔ Connected`. Then confirm tools actually exist — ask Claude something like:

> "Summarize document 1001_1_3 in Vault"

If this returns a real summary, Vault AI + at least one active agent are present. If the tool
list comes back empty or the request errors with "no matching tool", that's the open prerequisite
above, not a broken connection.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `401 Unauthorized` | Token invalid/expired, or token's Vault ID doesn't match the `{host}` in the URL |
| Connects, but no tools available | No active Agent/Action/Tool with API Access = Yes on this instance, or you lack **Agents: Execute** — a Vault-admin-side gap, not a client config issue |
| Works, then stops after ~8h | Session expired — reconnect (a fresh MCP session re-initializes automatically on the next call in most clients; if not, remove and re-add the server) |
| `${VAULT_IQMS_DEV_ACCESS_TOKEN}` shows up literally in the header | Variable wasn't set when the client started — set it, restart the editor |

## Related

- [`veeva-vault-documentation.md`](veeva-vault-documentation.md) — static developer docs, no auth,
  always available regardless of Vault AI licensing
- [`config/vault-metadata-api.md`](../../config/vault-metadata-api.md) — reading object field
  metadata directly from the same DEV sandbox via the plain Vault REST API, no MCP involved
