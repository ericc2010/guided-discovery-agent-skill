# Changelog

All notable changes to this skill are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). The version lives in
`metadata.version` in `skills/guided-discovery/SKILL.md`.

## [1.0.0] - 2026-10-10

First published version, built from the original `guided-discovery-skill.zip` draft.

### Fixed
- Skill folder renamed from `guided-discovery-skill` to `guided-discovery`. The
  Agent Skills spec requires the folder to match `name`, and `skills-ref validate`
  rejected the original.

### Added
- "Authorization is not information" section. A recommendation, a chosen option,
  or "just build it" no longer reads as approval to delete, deploy, publish,
  send, spend, or change access.
- User overrides: "use your recommendations" / "stop asking", changed answers,
  and conflicting requirements.
- An explicit three-part test for when a question is worth asking.
- Loop guard: after three questions with the task still unclear, summarize and
  ask once whether to proceed.
- Hand-off summary format: decisions, assumptions, open non-blocking items.
- Guidance for hosts with a native single-choice question tool.
- `license` and `metadata.version` frontmatter.
- Repository: README, examples, behavior scenarios, CI validation.

### Changed
- `description` now names explicit triggers and when not to activate.
- Example rewritten as a block-formatted transcript, ending in a hand-off.
