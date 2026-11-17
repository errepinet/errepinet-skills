# errepinet-skills

OpenCode skills maintained by ErrepiNet.

| Skill ID | Description |
| --- | --- |
| `errepinet-cve-audit` | Audit, triage, and fix CVEs in external dependencies of Rust, Python (uv), Flutter, and Node projects. |
| `errepinet-openspec-generate-specs` | Generate OpenSpec baseline specs from an existing (brownfield) codebase. |

Repository layout:

```text
skills/
├── index.json
├── errepinet-cve-audit/
│   ├── SKILL.md
│   ├── scripts/
│   └── tests/
└── errepinet-openspec-generate-specs/
    └── SKILL.md
```

## Install and update

### Option A — `skills` CLI (recommended)

Requires Node.js 22.20+ or Bun. The CLI installs individual skills, records them
in a lock file, and updates them in place. Private repositories reuse your
existing Git credentials.

```bash
# List the skills in this repository
bunx skills@latest add errepinet/errepinet-skills --list

# Install one skill globally for OpenCode
bunx skills@latest add errepinet/errepinet-skills \
  --skill errepinet-cve-audit -a opencode -g -y

# Install both skills globally for OpenCode
bunx skills@latest add errepinet/errepinet-skills \
  --skill '*' -a opencode -g -y

# Check for and apply updates
bunx skills@latest check -g
bunx skills@latest update -g
```

Omit `-g` to install into the current project instead of
`~/.config/opencode/skills/`. The default method is a symlink to a canonical
copy, so updates apply everywhere; add `--copy` for independent copies.

### Option B — OpenCode HTTP catalog

Add the catalog URL to your global `~/.config/opencode/opencode.json` (or a
project `opencode.json`):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["https://raw.githubusercontent.com/errepinet/errepinet-skills/main/skills/"]
}
```

OpenCode downloads every skill listed in
[`skills/index.json`](skills/index.json) and refreshes it whenever its
`version` changes. Configuration changes reload automatically; use `/reload` to
force a reload. The catalog is not individually selectable — use Option A if you
want only some skills.

### Option C — Local clone

```sh
git clone https://github.com/errepinet/errepinet-skills.git ~/src/errepinet-skills
```

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["~/src/errepinet-skills/skills"]
}
```

Update with:

```sh
git -C ~/src/errepinet-skills pull
```

Use one installation method per skill: the `skills` CLI, the HTTP catalog, and a
local clone all register the same skill IDs.

## Use a skill

Ask for the task normally, or mention the skill explicitly:
`@errepinet-cve-audit`, `@errepinet-openspec-generate-specs`.

Paths inside a `SKILL.md` are relative to the directory containing that file.
The CVE audit scripts require Python 3.8+ and the relevant audit CLIs
(`cargo audit`, `pip-audit`, `npm`/`pnpm`/`yarn`, `trivy`, `grype`).

## Development

- Run the CVE audit tests: `python3 skills/errepinet-cve-audit/tests/run.py`
- After editing any skill file, regenerate the catalog: `python3 tools/sync_catalog.py`
- Verify the catalog is current: `python3 tools/sync_catalog.py --check`
- Every skill must live at `skills/<skill-id>/SKILL.md`, with a lowercase
  kebab-case ID.
- `version` in `skills/index.json` is a content hash, so it changes
  automatically when a skill's files change.

## License

MIT — see [LICENSE](LICENSE).
