# Rules for AI coding agents

These rules apply to every AI agent working in this repo (OpenCode, Gemini CLI, Codex, Copilot, Claude, and others).

## Workflow

1. **Never commit to `main`.** Before changing anything, create a branch:
   `git switch -c feat/<short-name>` (or `fix/…`, `docs/…`, `chore/…`).
2. **Keep each task small.** One feature or fix per branch.
3. **Use Conventional Commits.** Release notes and version numbers are generated from them:
   - `feat: add CSV export` → new feature (minor version bump)
   - `fix: handle empty input` → bug fix (patch bump)
   - `docs:`, `test:`, `refactor:`, `chore:` → no release
   - `feat!:` or a `BREAKING CHANGE:` footer → major bump
4. **Run the checks before you say you're done.** They must all pass:
   ```bash
   uv run ruff format .
   uv run ruff check . --fix
   uv run pytest
   ```
5. **When done:** commit, push the branch, and open a pull request:
   `git push -u origin HEAD && gh pr create --fill`
   Do not merge it. The human reviews and merges.

## Code rules

- Python 3.12+. Code goes in `src/app/`, tests in `tests/`.
- Add or update a test for every behavior you add or change.
- Manage dependencies only with `uv add <pkg>` / `uv remove <pkg>`, never by editing `pyproject.toml` by hand. **Ask before adding a dependency.**
- Never commit secrets, API keys or `.env` files. Read config from environment variables.
- Don't edit `CHANGELOG.md`, version numbers, `.release-please-manifest.json` or `.github/`. Those are managed by automation or by the human.
- Prefer simple, readable code over clever code. The human is a hobbyist.

## When unsure

Stop and ask rather than guessing, especially before deleting files, changing the project structure or touching anything in `.github/`.
