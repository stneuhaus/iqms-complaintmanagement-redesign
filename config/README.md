# Config

Status: In use  
Last reviewed: 2026-11-05

Environment examples (for example `.env.example`) and notes about outbound connections.

| File | Contents |
| --- | --- |
| [`mcp-n8n.md`](mcp-n8n.md) | Superseded — pointer to [`docs/09-claude-mcp-setup/n8n.md`](../docs/09-claude-mcp-setup/n8n.md) |
| [`mcp-azure-devops.md`](mcp-azure-devops.md) | Superseded — pointer to [`docs/09-claude-mcp-setup/azure-devops.md`](../docs/09-claude-mcp-setup/azure-devops.md) |
| [`vault-metadata-api.md`](vault-metadata-api.md) | Reading IQMS Vault object fields (type, required, editable) via the Metadata API — session handling and the `vault-object-fields.py` script |

No MCP server is declared in this repository anymore — every MCP server (n8n, Azure DevOps, and
the two Veeva Vault servers) is set up personally, per machine, with `claude mcp add --scope
user`. See [`docs/09-claude-mcp-setup/`](../docs/09-claude-mcp-setup/README.md) for setup
instructions.

Do not store real API keys, vault tokens, or passwords here.
