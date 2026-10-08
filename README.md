# app

A Python project with an AI-assisted, controlled-release workflow.

## Everyday loop

```bash
git switch main && git pull          # 1. start from the latest main
opencode                             # 2. describe the feature; the agent follows AGENTS.md:
                                     #    branch → code → tests → commit → push → PR
gh pr view --web                     # 3. look at the PR and wait for CI to go green
gh pr diff | gemini -p "Review this diff for bugs and risky changes"   # 4. second-opinion review
gh pr merge --squash                 # 5. you merge (PR title becomes the commit message)
```

## Releasing

After each merge, the **Release** workflow opens or updates a PR called
`chore(main): release x.y.z` with the version bump and CHANGELOG.

- Merging it creates the GitHub release and tag.
- Not ready to release? Leave it open; it keeps collecting changes.
- GitHub doesn't run CI on PRs made by automation, so merge this one with
  `gh pr merge --squash --admin` (or tick "bypass rules" on the website).
  Use the bypass **only** for release PRs.

## Commands

| What | Command |
|---|---|
| Run the app | `uv run python -m app.main` |
| Tests | `uv run pytest` |
| Format + lint | `uv run ruff format . && uv run ruff check . --fix` |
| Add a library | `uv add <name>` |

## Undo

| Situation | Command |
|---|---|
| Throw away uncommitted AI changes | `git restore . && git clean -fd` |
| Abandon a branch | `git switch main && git branch -D <branch>` |
| Revert a merged change | `git switch -c fix/revert && git revert <commit> && git push -u origin HEAD && gh pr create --fill` |
