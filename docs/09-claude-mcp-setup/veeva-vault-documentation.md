# Veeva Vault Documentation MCP

Status: In use (personal-only — see [`README.md`](README.md) for why)
Last reviewed: 2026-11-05

Gives an AI coding assistant direct access to Veeva's developer documentation (Vault API, Java
SDK, VQL, MDL, Direct Data API, Custom Pages, release notes) via MCP, instead of copy-pasting
docs pages into the chat.

## Server details

| | |
| --- | --- |
| Name | `vault-documentation-mcp` |
| URL | `https://docs.veevavault.dev/mcp` |
| Transport | stdio bridge (`mcp-remote`) over HTTP — see "Why the bridge" below |
| Auth | None |
| Tools | `search_documentation`, `search_release_notes` |
| Source | <https://general.veevavault.dev/mcp/vault-documentation-mcp/> |

Covers all Vault product families (Clinical, Commercial, Medical, Platform, Quality, QualityOne,
RIM, Safety, SiteVault).

## Setup

No token needed. One command:

```bash
claude mcp add vault-documentation-mcp --scope user \
  -e HTTPS_PROXY=http://10.185.190.10:8080 \
  -e NODE_USE_ENV_PROXY=1 \
  -e NODE_OPTIONS=--use-system-ca \
  -e NO_PROXY=localhost,127.0.0.1 \
  -- npx -y mcp-remote https://docs.veevavault.dev/mcp --transport http-only
```

### Why the bridge, not plain `--transport http`

Veeva's own Claude Code instructions suggest a direct HTTP server:

```bash
claude mcp add --transport http vault-documentation-mcp https://docs.veevavault.dev/mcp --scope user
```

That's simpler, but as of this writing Bayer's internal DNS does not resolve
`docs.veevavault.dev` (`nslookup` returns `NXDOMAIN`), so a direct connection fails outright. The
`mcp-remote` stdio bridge lets the request go through Node, where `HTTPS_PROXY` +
`NODE_USE_ENV_PROXY=1` route around the DNS gap via the Bayer proxy, and `NODE_OPTIONS=--use-system-ca`
satisfies the proxy's TLS interception. See [`README.md`](README.md#bayer-proxy-and-certificates)
for the full explanation and how to re-check if this is still necessary.

## Verify

```bash
claude mcp list
```

`vault-documentation-mcp` should show `✔ Connected`. Functional check — ask Claude something like:

> "update single user api uri path parameters"

Expect a structured answer with the API endpoint, HTTP method, parameters, and an example — not
a generic/guessed response.

## Using it well

- **Be surgical**: include concrete technical identifiers ("document", "picklist",
  "RecordService") rather than vague descriptions.
- **Use contextual keywords**: action verbs like "create", "update", "query", "execute" help the
  tool pick the right documentation source.
- You don't need to set `source`, `app_family`, or `release` yourself — the client infers them
  from the query, but a vague query gets a vague inference.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `-32000: Connection closed` / hangs with no output | Usually `ENOTFOUND <host>` under the hood — confirm with `nslookup docs.veevavault.dev` vs. `nslookup docs.veevavault.dev 8.8.8.8`; if only the second resolves, the proxy env block above is required (see [`README.md`](README.md#bayer-proxy-and-certificates)) |
| `SELF_SIGNED_CERT_IN_CHAIN` / `UNABLE_TO_VERIFY_LEAF_SIGNATURE` | `NODE_OPTIONS=--use-system-ca` missing from the `env` block |
| Connects, but answers are generic/wrong | Query too vague — add a specific technical noun (see "Using it well") |

## Related

- [`veeva-vault-ai.md`](veeva-vault-ai.md) — the other Veeva MCP server, for live Vault instance
  interaction instead of developer docs
- [`config/vault-metadata-api.md`](../../config/vault-metadata-api.md) — reading actual object
  field metadata from the IQMS Vault, not documentation
