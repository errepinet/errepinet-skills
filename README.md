# errepinet-skills

OpenCode skills maintained by ErrepiNet.

| Skill ID | Description |
| --- | --- |
| `errepinet-cve-audit` | Audit, triage, and fix CVEs in external dependencies of Rust, Python (uv), Flutter, and Node projects. |
| `errepinet-openspec-generate-specs` | Generate OpenSpec baseline specs from an existing (brownfield) codebase. |

## Install and update with OpenCode

OpenCode V2 discovers skills from local directories and from HTTP catalogs. This
repository publishes an [`index.json`](index.json) catalog, so one entry keeps
every skill installed and updated.

### Option A — HTTP catalog (recommended)

Add the catalog URL to your global `~/.config/opencode/opencode.json` (or a
project `opencode.json`):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["https://raw.githubusercontent.com/errepinet/errepinet-skills/main/"]
}
```

OpenCode downloads every skill listed in `index.json` and refreshes it whenever
its `version` changes. Configuration changes reload automatically; use `/reload`
to force a reload.

> The catalog installs all skills in this repository. OpenCode catalog entries
> are not individually selectable.

### Option B — Local clone

```sh
git clone https://github.com/errepinet/errepinet-skills.git ~/src/errepinet-skills
```

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["~/src/errepinet-skills"]
}
```

Update with:

```sh
git -C ~/src/errepinet-skills pull
```

## Use a skill

Ask for the task normally, or mention the skill explicitly:
`@errepinet-cve-audit`, `@errepinet-openspec-generate-specs`.

Paths inside a `SKILL.md` are relative to the directory containing that file.
The CVE audit scripts require Python 3.8+ and the relevant audit CLIs
(`cargo audit`, `pip-audit`, `npm`/`pnpm`/`yarn`, `trivy`, `grype`).

## Development

- Run the CVE audit tests: `python3 errepinet-cve-audit/tests/run.py`
- After editing any skill file, regenerate the catalog: `python3 tools/sync_catalog.py`
- Verify the catalog is current: `python3 tools/sync_catalog.py --check`
- Every skill must live at the repository root as `<skill-id>/SKILL.md`, with a
  lowercase kebab-case ID.
- `version` in `index.json` is a content hash, so it changes automatically when
  a skill's files change.

## License

MIT — see [LICENSE](LICENSE).
