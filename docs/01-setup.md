# 1. Set up the workspace

## What you do

1. Clone/open `AYassin01/swvl-gtm-research-playbook` in the same environment where your Codex connections are configured. Keep existing local work; ask Codex to use an isolated worktree if needed.
2. Save the task PDF locally outside Git. Give Codex its actual path. Cloud-chat attachment paths are not laptop paths.
3. Agree a distinct buyer hypothesis with your teammates. Suggested title family: Transport Manager, Transportation Manager, Transportation Supervisor, Head of Transportation. Select your own family before buyer retrieval.
4. Choose your personal Clay workspace and authorize the account connection. Do not paste credentials into the repo or prompt.
5. Enable a browser-control tool in Codex that can operate your Clay app session. Log in yourself when required. Codex should handle creating/importing the table; you should not have to perform a manual CSV import as the default workflow.
6. Open [the full prompt](../prompts/codex.md), or paste the launcher from the README. Let Codex prepare the actual quote; approve the numerical cap only after the scope and evidence are visible.

Check configured connections with `codex mcp list`; inside Codex, `/mcp` shows active MCP servers. Configured names do not establish that required tools work. [Official Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp)

## What Codex verifies

| Capability | Required for | How to handle a missing capability |
| --- | --- | --- |
| Clay company/people search | Primary market and buyer results | Connect/authorize Clay; do not substitute fabricated results |
| Browser control of the Clay app | Create/import/verify the table when write tools are absent; displayed totals | Ask only for enabling browser control or account login; continue independent preparation |
| Pricing and usage access | A supported quote and actual cost evidence | Inspect current provider responses/docs/app; label genuinely unavailable figures |
| Local files/Python | Sanitized files, counts, checks and reports | Use standard-library scripts; no extra research platform |
| Git/GitHub | Working branch, PR, evidence index and merge | Preserve local changes; request only a real authentication/access handoff |

The connected Clay table operations currently documented here read existing tables and do not create/populate them. Therefore the prompt explicitly uses browser interaction when it lacks a genuine write-capable tool. It does not invent a create-table API. Verify the live capability before each run. [Clay table documentation](https://developers.clay.com/tables.md)

If neither a supported table-write tool nor browser control is available, the table stage is blocked by access. Codex must explain that specific blocker before paid research and ask you to enable the needed connection. It must not claim a local CSV fulfills the table requirement.

## Optional tools

If available, `$deepline-gtm`, treg, Exa, Firecrawl and PDL have the limited jobs in [the tool guide](04-tools-and-credits.md). Their absence does not block the primary Clay/browser workflow. A shared repo does not share your accounts, credits, tokens or billing approvals.

## One setup message

```text
Task PDF path: [actual local path]
Clay workspace: [actual workspace]
Company ICP: [adopt the proposed definition / give a revision]
Team-agreed title family: [actual titles and coordination status]
Buyer rule: [my chosen threshold and relevance definition]
Browser control: [available tool/session, or help me enable it]
Spending: prepare an evidence-backed Clay quote and ask for my approval.
```
