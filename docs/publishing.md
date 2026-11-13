# Put this repository on GitHub

The shared team repository is [AYassin01/swvl-gtm-research-playbook](https://github.com/AYassin01/swvl-gtm-research-playbook). Ahmed created it as a public repository. Use branches and PRs for ongoing work.

The connected GitHub tools available during preparation can update files, branches, commits, issues and PRs in accessible repositories. They do not expose creating a new repository. Create the repository once through GitHub, then use the connection for ongoing work.

## GitHub website route

For a separate team copy, create a repository under your account, choose visibility, and initialize it with a README. Share the repository URL with the agent so it can verify access and upload the prepared text files. Existing unrelated repositories should keep their own project scope.

## Local GitHub CLI route

For a separate copy, run these commands from a prepared local Git repository after authenticating GitHub CLI on your machine. Choose an unused repository name if the suggested one already exists in your account.

```bash
gh auth status
gh repo create swvl-gtm-research-playbook --private --source . --remote origin --push
```

After creation, open the repo and verify README, Mermaid, files and Actions. Add teammates through GitHub's collaborator controls using their verified handles. A repo URL alone does not grant access to a private repo.

For the current team project, clone the existing repository using docs/how-to-run.md. A fork is another way to develop your own changes and propose them back to the team.
