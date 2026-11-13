# MCP connections

Connection guidance checked on 13 November 2026. Tool names, permissions and authentication can vary by client and provider plan. Confirm the current vendor instructions before changing a working connection.

## Hosted ChatGPT or Work

Install and connect Clay, Crustdata and treg through the available plugin or connector controls. Select them in the research session. Add Google Drive only when reading team files or exporting deliverables, and GitHub when maintaining this repository.

Account access does not transfer with a shared prompt or Git clone. Teammates authorize their own connections and use the correct paying workspace. A local Codex MCP configuration does not configure the hosted chat. [Official OpenAI MCP guidance](https://learn.chatgpt.com/docs/extend/mcp)

## Local Codex CLI

Inspect existing connections first.

```bash
codex mcp list
codex mcp --help
```

Add only missing connections. These server URLs are documented by the providers.

```bash
codex mcp add clay --url https://api.clay.com/v3/mcp
codex mcp login clay
codex mcp add treg --url https://treg.to/mcp/
codex mcp login treg
```

Clay's workspace administrator controls allowed MCP clients and credits. Its MCP for Reps toolset is separate from its API/CLI plugin. [Clay connection reference](https://university.clay.com/docs/connect-to-clay-mcp) · [Clay MCP settings](https://university.clay.com/docs/mcp-settings)

For Crustdata, the provider's documented file-based Codex setup uses an API key. Place the key in your local environment using your platform's secret-management method, then configure the bearer-token environment reference in your private Codex config.

```toml
[mcp_servers.crustdata]
url = "https://mcp.crustdata.com/mcp"
bearer_token_env_var = "CRUSTDATA_API_KEY"
```

`CRUSTDATA_API_KEY` must be available to the process launching Codex. The environment reference is supported by Codex, while Crustdata's example uses a literal Authorization header. Keep real credentials in local settings. [Crustdata MCP reference](https://mcp.crustdata.com/) · [Codex HTTP authentication options](https://learn.chatgpt.com/docs/extend/mcp)

treg's MCP endpoint supports OAuth. Confirm the selected team before any paid lookup. Follow its current search, read, call sequence. [treg setup and operating reference](https://treg.to/llms.txt)

Start Codex in the repository root and type `/mcp` in its interactive terminal to inspect the active tools. The exact names in hosted ChatGPT often include a connector namespace. Match tools by their documented capability. [Official OpenAI MCP guidance](https://learn.chatgpt.com/docs/extend/mcp)

## Preflight checks

| Connection | Minimum capability to verify | Permitted preflight |
| --- | --- | --- |
| Clay | Company search and saved-result retrieval | Read connected workspace metadata if exposed |
| Crustdata | Indexed people search, field documentation | Read plan access and credit balance if exposed |
| treg | Catalog search, endpoint detail, call | Inspect own tools, balance and endpoint prices |
| Web retrieval | Search and read source pages | Open one supplied public page |
| Drive, optional | Read team inputs or create specified exports | Read only the supplied input files |
| GitHub, optional | Read repo and create/update a branch or PR | Read current branch and permissions |

Preflight is capability discovery. A failed preflight becomes a documented fallback. Exact per-call prices come from the current workspace/provider response and the run ledger.
