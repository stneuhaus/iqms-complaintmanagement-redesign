# Claude Code MCP setup

Status: In use
Last reviewed: 2026-11-05

Written for: anyone who wants to connect Claude Code (or another MCP client) to the external
services this project touches — Azure DevOps, the n8n Hub instance, and Veeva Vault.

## Why this is personal-only

None of these MCP servers are declared in this repository. No `.mcp.json` file, no server block,
no secret of any kind is checked in. Every server is added with **`--scope user`**, which writes
to your own `~/.claude.json` and therefore works the same way in every project on your machine,
not just this one. If you clone this repo on a new machine, nothing connects automatically —
follow the guide for each server you need.

| Guide | Server(s) | Auth |
| --- | --- | --- |
| [`n8n.md`](n8n.md) | `n8n-mcp` | Bearer token |
| [`azure-devops.md`](azure-devops.md) | one server per org (`azure-devops-bayer`, `azure-devops-clara`, …) | Personal Access Token |
| [`veeva-vault-documentation.md`](veeva-vault-documentation.md) | `vault-documentation-mcp` | None |
| [`veeva-vault-ai.md`](veeva-vault-ai.md) | `vault-ai-<instance>` | Vault access token |

Check what's currently connected and healthy with:

```bash
claude mcp list
```

## Bayer proxy and certificates

This is the one piece of plumbing every server below runs into, so it's explained once here
instead of four times.

**The problem:** Bayer's internal DNS (`BYRIP1.dnsrv.cnb`) does not resolve every external host —
notably `*.veevavault.dev` currently returns `NXDOMAIN` there, even though the host is reachable
from the public internet. Separately, `~/.npmrc` routes `npm`/`npx` through the Bayer proxy
(`http://10.185.190.10:8080`), which terminates TLS with a Bayer-internal root certificate that
Node does not trust by default.

**The fix, in every server's `env` block below:**

| Variable | Why |
| --- | --- |
| `HTTPS_PROXY=http://10.185.190.10:8080` | Routes the connection through a resolver that *can* reach the host, even when local DNS can't. |
| `NODE_USE_ENV_PROXY=1` | Node 24+ native support for honoring `HTTPS_PROXY`/`NO_PROXY` — required alongside the variable above. |
| `NODE_OPTIONS=--use-system-ca` | Lets Node read the Windows certificate store, where the Bayer root CA lives (needs Node 22.15/23+). Without it: `SELF_SIGNED_CERT_IN_CHAIN` or `UNABLE_TO_VERIFY_LEAF_SIGNATURE`. |
| `NO_PROXY=localhost,127.0.0.1` | Keeps purely local traffic off the proxy. |

**Do not** set `NODE_TLS_REJECT_UNAUTHORIZED=0` to work around certificate errors — it disables
certificate verification entirely, so the process can no longer tell the real proxy from a
man-in-the-middle. The four variables above are the complete, narrower fix.

**One exception:** `vault-documentation-mcp` is an HTTP-only server with no Vault-specific
secret, so it doesn't strictly need the proxy for authentication — only for DNS/TLS, same as
everything else. If a future DNS fix makes Bayer's resolver handle `*.veevavault.dev` directly,
these variables can likely be dropped for that one server; re-test with `claude mcp list` before
removing them.

**Diagnosing a `-32000: Connection closed` or similar failure** for any stdio server built on
`npx`:

```bash
# 1. Does local DNS resolve the host at all?
nslookup <host>

# 2. If NXDOMAIN, does it resolve via a public resolver? (confirms it's a Bayer DNS gap, not a dead host)
nslookup <host> 8.8.8.8

# 3. Does the proxy tunnel work without extra auth?
curl -sv --ssl-no-revoke -x http://10.185.190.10:8080 https://<host>/ -o /dev/null
```

If step 2 succeeds and step 1 doesn't, the fix is the proxy env block above — not a direct,
proxy-less connection, despite what you may have working for other hosts.

## Related

- [`config/README.md`](../../config/README.md) — environment notes and the older, project-scoped
  MCP docs this folder supersedes.
- [`config/vault-metadata-api.md`](../../config/vault-metadata-api.md) — direct Vault Metadata
  API access (not an MCP server, but the same DEV sandbox instance as `veeva-vault-ai.md`).
