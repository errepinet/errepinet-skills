---
name: errepinet-openspec-generate-specs
description: Reverse-engineers OpenSpec baseline specifications from an existing (brownfield) codebase. Writes finished spec.md files directly into openspec/specs/<capability>/ describing what the code currently does — unlike the propose/apply/archive workflow, this writes canonical "current truth" specs, not a change proposal. Use this whenever the user wants to bootstrap OpenSpec on a project that already has code, wants to "document the current behavior", "generate a baseline", "onboard an existing repo into OpenSpec", or when openspec/specs/ is empty but the codebase is not. Also use it to refresh/update specs for one or more capabilities after manual code changes that were not run through the propose/apply/archive cycle.
---

# OpenSpec: Generate Baseline Specs from Existing Code

This skill produces OpenSpec-compatible spec files that describe a codebase **as it
currently behaves**, not as a proposed change. It is the brownfield "cold start" tool:
run it once (or per-capability) to get `openspec/specs/` populated before starting the
normal `/opsx:propose → /opsx:apply → /opsx:archive` loop, or after manual edits that
left the specs stale.

It does **not** create a `openspec/changes/` folder. It writes directly to
`openspec/specs/<capability>/spec.md`, because these documents describe existing,
shipped behavior, not something awaiting review.

## Preconditions

- `openspec/` must already exist in the project (run `openspec init` first if not).
- If `openspec/config.yaml` or `openspec/project.md` exist, read them first — they may
  contain project-specific conventions, tech stack notes, or a preferred schema that
  should shape how you describe requirements (e.g. "prefer Given/When/Then", "always
  document error paths").

## Step 1 — Gather context

Before touching any code, collect whatever project context already exists. Read, if
present (skip silently if absent, don't ask the user to create them first):

- `openspec/project.md`
- `openspec/config.yaml`
- `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`
- `docs/` (any architecture notes, ADRs)

Then scan the codebase structure itself:

- Top-level source tree (`src/`, `crates/*/src/`, or language-appropriate layout)
- Entry points (main.rs, lib.rs, index.ts, app.py, etc.)
- Public types/interfaces/traits that define module boundaries
- Existing tests — they're often the best evidence of *intended* behavior, not just
  implementation detail, and are a good source for scenario writing

If the project uses a version control system, `git log --oneline -20` and open
issues/PRs (if a GitHub remote is configured and a tool is available) can add useful
"why" context that pure static reading of the code won't reveal — use them if easily
accessible, but don't block on it if not.

## Step 2 — Identify capabilities

A "capability" is a cohesive area of functionality — usually one per major module,
subsystem, or bounded context. Aim for something a new contributor would recognize as
one unit, not one-per-file and not one-for-the-whole-project.

Examples of good capability granularity: `job-queue`, `actor-runtime`, `redis-reliability`,
`grpc-api`, `retry-policy` — not `mpsc.rs` (too small) and not `backend` (too broad).

**Always confirm the capability list with the user before generating anything.**
Present it as a short numbered list with a one-line description each, and let them
select all, a subset, or suggest corrections. Do not skip this confirmation step even
if the capability boundaries seem obvious — the user's mental model of the system may
differ from what static analysis suggests, and generating specs for the wrong
boundaries wastes their review time more than one extra question would.

Use kebab-case for capability names.

## Step 3 — Handle existing specs

For each selected capability, check whether `openspec/specs/<capability>/spec.md`
already exists.

- **If it doesn't exist**: proceed to generate it fresh.
- **If it exists**: ask the user, per capability (or once for all, if they prefer
  bulk handling): **Overwrite** (replace entirely with the newly generated spec),
  **Merge** (add missing requirements/scenarios, preserve existing content and any
  manual edits the user may have made), or **Skip** (leave untouched). Default
  suggestion: Merge, since it's the least destructive to human-authored content that
  may already be in there.

## Step 4 — Write each spec

Follow the standard OpenSpec spec format. Structure:

```markdown
# {Capability Name} Specification

> Generated from source analysis on {date}
> Source files: {comma-separated list of primary files/modules}

## Purpose

{2-3 sentences: what this capability handles and why it exists}

## Requirements

### Requirement: {RequirementName}

{Description using RFC 2119 keywords: SHALL / MUST NOT / SHOULD / MAY}

#### Scenario: {ScenarioName}

- **GIVEN** {precondition}
- **WHEN** {action}
- **THEN** {expected outcome}
- **AND** {additional assertion, optional}

## Technical Notes

- **Implementation**: `{file paths}`
- **Dependencies**: {related capabilities/modules this one relies on or is relied on by}
```

Guidelines while writing requirements:

- Describe **observed behavior**, not aspirational behavior. If the code has a bug or
  an inconsistency, document what it actually does and optionally flag it in Technical
  Notes as a known issue — don't silently "fix" it in the spec.
- Use `SHALL`/`MUST` for behavior the code enforces unconditionally, `SHOULD` for
  documented-but-not-enforced conventions, `MAY` for genuinely optional behavior.
- Write scenarios at the level a human reviewer can verify by reading the code or
  running the system — not so granular that every branch gets its own scenario, not so
  vague that the scenario could describe several different implementations.
- If tests exist for the capability, cross-check that your scenarios don't contradict
  what the tests actually assert — tests are evidence, but code behavior is ground
  truth if the two disagree (flag the discrepancy in Technical Notes rather than
  silently picking one).

Write the file, then confirm it was written (re-read it back or check existence) and
report brief progress before moving to the next capability. If you have access to a
todo-tracking mechanism, use it to track progress across capabilities — this task is
naturally interruptible and resumable.

## Step 5 — Validate

If the `openspec` CLI is available (`openspec validate --strict`, or per-capability
if supported), run it against the newly written specs and fix any structural issues
before finishing. If the CLI isn't available in this environment, at minimum
self-check: every Requirement has at least one Scenario, every Scenario has
GIVEN/WHEN/THEN, and heading levels match the format above exactly (`###` for
Requirement, `####` for Scenario).

## Step 6 — Summarize

End with a table:

| Capability | Requirements | Scenarios | Status |
|------------|-------------|-----------|--------|
| ...        | N           | M         | New / Merged / Overwritten / Skipped |

Followed by: "Files written to `openspec/specs/`. Review them before treating them as
ground truth for future `/opsx:propose` changes — reverse-engineered specs describe
what the code does, not necessarily what it *should* do."

## Notes on scope

- This skill is for **initial bootstrap or targeted refresh**, not a replacement for
  the day-to-day `/opsx:propose → /opsx:apply → /opsx:sync → /opsx:archive` loop. Once
  a capability has a baseline spec, future changes to it should go through that normal
  cycle so the delta-spec history stays meaningful.
- If the user only made a small manual edit to one file and wants a quick
  reconciliation rather than a full capability regeneration, it's faster to just
  read the affected spec, compare it to the diff, and patch the relevant
  Requirement/Scenario directly — you don't need to run this full skill for that case.
