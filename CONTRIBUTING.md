# Contributing

Thanks for helping improve the Metergraph skills.

1. Read [AGENTS.md](AGENTS.md). This repository is public.
2. Keep each skill short. Put long reference material in a `references/` file next to
   its `SKILL.md` and link to it.
3. Test a changed skill against a real or demo workspace with at least one agent
   (Claude Code, Claude Desktop, Codex or Cursor) and describe what you ran in the pull
   request. Use synthetic data in examples.
4. Run `node scripts/validate.mjs` and
   `python3 scripts/check_publication.py origin/main` before pushing.
