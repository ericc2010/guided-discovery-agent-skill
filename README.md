# Guided Discovery

An [Agent Skills](https://agentskills.io/specification) skill that changes how an AI coding agent handles vague requests. It asks one multiple-choice question at a time, recommends an answer, and starts work as soon as it knows enough.

Plain Markdown. No scripts, no dependencies.

## The problem

Given a vague request, agents tend to fail in one of two ways:

- **They guess.** They build the wrong thing quickly, and you find out after the work is done.
- **They interrogate.** They send ten questions at once, including ones the context already answers and ones a sensible default would cover.

Guided Discovery sits in between. It asks only questions whose answers would change the work, one at a time, and makes each one quick to answer.

## What it does

- **Reads first.** It checks the request, the conversation, and the project before asking anything.
- **Asks only what matters.** A question must be unanswered by the context, must change the result, and must lack a safe default.
- **One question per message**, with 3–5 options, a trade-off for each, and one marked **Recommended** with a reason.
- **Free-text answers and delegation.** You can type your own answer or say "you decide".
- **Adaptive.** After each answer it re-ranks what is still open and drops questions that became moot. It never repeats a question.
- **Handles changes and conflicts.** If you change an answer, it re-checks only what depended on it. It surfaces conflicting requirements instead of silently picking one.
- **Knows when to stop.** It stops once the task is clear or when you say "just build it". A loop guard ends stalled intakes.
- **Hands off clearly.** It lists decisions, assumptions, and open non-blocking items, then starts the work.
- **Keeps a recommendation separate from permission.** "You decide" settles *what* to build. It does not approve deleting, deploying, publishing, sending, spending, or changing access.

## Example

Without the skill, "Build me a customer portal" usually produces either a generic app built on guesses or a long list of questions. With it:

> **You:** Build me a customer portal.
>
> **Agent:** The repo is empty, so I have no existing code or stack to go on. One question before I start:
>
> **Question 1: What should customers mainly do in the portal?**
> A. **Manage orders and account**: view order history and status, update profile and addresses (**Recommended**: this is the most common reason for a portal and works without any outside services)
> B. **Manage billing and subscriptions**: invoices, payment methods, plan changes; most likely built on Stripe
> C. **Get support**: open tickets, message your team, browse help articles
> D. **Track projects or service requests**: request work and follow its status and documents
>
> *Reply with a letter, your own answer, or "you decide".*
>
> **You:** A
>
> **Agent:** **Question 2: Where does the order and customer data come from?**
> A. **The portal's own database**: I build the data model and seed sample data; you connect real data later (**Recommended**: nothing exists yet to integrate with, and this is the fastest route to a working portal)
> B. **Shopify**: customers see their Shopify orders through the Customer Account API
> C. **Your existing system or API**: an ERP or custom backend (tell me which)
> D. **Spreadsheets or CSV exports**, imported regularly
>
> *Reply with a letter, your own answer, or "you decide".*
>
> **You:** Use your recommendations for the rest and build it.
>
> **Agent:** **Decisions:** order and account self-service; the portal's own database.
> **Assumptions:** Next.js, SQLite via Prisma, email magic-link login, seeded demo data.
> **Open, non-blocking:** branding, Shopify import.
> Starting with the scaffold. I'll ask before deploying anything.

Both questions are real Claude Code output from one test session (Claude Code 2.1.296), lightly trimmed. The final hand-off is illustrative, written in the format the skill prescribes. More walkthroughs are in [examples/](examples/):

- [Software architecture](examples/software-architecture.md): a dependent follow-up, and an approval gate that "you decide" does not get past.
- [Product design](examples/product-design.md): a custom answer, and a changed earlier answer.
- [Business strategy](examples/business-strategy.md): a fully specified request that gets no questions, then a conflict that gets one.

## Installation

### Claude Code plugin marketplace

The skill is also published in the [agent-skills](https://github.com/ericc2010/agent-skills) library:

```
/plugin marketplace add ericc2010/agent-skills
/plugin install guided-discovery@ericc2010-skills
```

### Manual copy

The skill is one folder, `skills/guided-discovery/`. Install it by copying that folder into a directory your agent scans:

```bash
git clone https://github.com/ericc2010/guided-discovery-agent-skill.git /tmp/guided-discovery-agent-skill
```

#### Claude Code

```bash
# For you, in every project
mkdir -p ~/.claude/skills
cp -R /tmp/guided-discovery-agent-skill/skills/guided-discovery ~/.claude/skills/

# Or for one project only (commit it to share with the team)
mkdir -p .claude/skills
cp -R /tmp/guided-discovery-agent-skill/skills/guided-discovery .claude/skills/
```

#### Codex

```bash
# For you
mkdir -p ~/.agents/skills
cp -R /tmp/guided-discovery-agent-skill/skills/guided-discovery ~/.agents/skills/

# Or for one repository
mkdir -p .agents/skills
cp -R /tmp/guided-discovery-agent-skill/skills/guided-discovery .agents/skills/
```

Restart Codex if the skill does not appear in `/skills`.

#### OpenCode

OpenCode reads its own skills folder, and also `~/.claude/skills` and `~/.agents/skills`. If you already installed the skill for Claude Code or Codex, OpenCode will find it. Otherwise:

```bash
mkdir -p ~/.config/opencode/skills
cp -R /tmp/guided-discovery-agent-skill/skills/guided-discovery ~/.config/opencode/skills/
```

Project-level folders also work: `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/`.

### Other agents

Any agent that implements the Agent Skills format should load the folder from its skills directory. For an agent without skill support, paste the body of `SKILL.md` (everything after the frontmatter) into its system prompt or `AGENTS.md`. In that case it is always on, rather than activating when relevant.

### Updating

Pull the repository and copy the folder again. Check `metadata.version` in `SKILL.md` against [CHANGELOG.md](CHANGELOG.md).

## Activation

### Automatic

At startup, the agent sees only the skill's `name` and `description`. It decides on its own to load the full instructions when a request matches the description: one with a missing decision that would change the result, or with conflicting requirements.

Limitations, observed in testing:

- **Activation is the model's call, not a guarantee.** In the test runs, a vague "build me a customer portal" activated the skill in all three agents. A request with conflicting requirements did not activate it in Claude Code, although the agent still named the conflict and offered options.
- **The safety rules apply only while the skill is active.** For clear, fully specified requests the skill correctly stays off, and approval prompts then come from the agent and its permission settings, not from this skill. Do not rely on this skill as a safety layer.

### Manual

| Agent | How to invoke |
|---|---|
| Claude Code | `/guided-discovery`, optionally followed by the request |
| Codex | `$guided-discovery`, or pick it from `/skills` |
| OpenCode | Ask for it by name ("use the guided-discovery skill"). The agent loads it through its `skill` tool. |

### Controlling it mid-conversation

These phrases work whether the skill activated on its own or was invoked:

- "Use your recommendations" / "you decide the rest" / "just build it" / "stop asking": questions end, defaults apply, and work starts. Approval gates still apply.
- "Change my answer to …": updates that answer and re-checks only what depended on it.
- "What do you still need to know?": prompts another round of discovery.

## Configuration

The skill has no settings file. Customize it by editing `SKILL.md`:

| What | Where in `SKILL.md` |
|---|---|
| Number of options per question (default 3–5) | "Question format" |
| Loop guard (default: stop after 3 questions without progress) | "Exit criteria" |
| Which actions need explicit approval | "Authorization is not information" |
| Hand-off summary shape | "Hand-off" |
| When it activates | the `description` frontmatter field |

**Making it manual-only in Claude Code.** Add `disable-model-invocation: true` to the frontmatter. This field is Claude Code-specific. `skills-ref validate` rejects it, and other agents ignore it, so keep that change in your local copy and out of this repository.

**Project overrides.** A project-level copy (`.claude/skills/`, `.agents/skills/`) is used instead of the user-level one. That lets a team tune the defaults per repository.

## Compatibility

"Tested" means the scenarios in [tests/behavior-scenarios.md](tests/behavior-scenarios.md) were run against that agent on 2026-10-10, with the skill installed at project level. Full results are in the results table there.

| Environment | Status | What was verified |
|---|---|---|
| Claude Code 2.1.296 (headless `-p`, Opus 5.5) | **Tested** | Auto-activation; question format; follow-up after an answer; delegation; no questions for clear requests; push/tag held for approval, both with and without the skill active |
| Codex CLI 0.159.0 (`codex exec`, default model) | **Partly tested** | Auto-activation; one question with Recommended marked; no questions for a clear request. Its formatting differed (bullets, not lettered options). |
| OpenCode 2.0.20 (`opencode run`, DeepSeek V4 Pro) | **Partly tested** | Auto-activation through its `skill` tool; asked through its native question tool; no questions for a clear request. Question content not visible in headless mode. |
| Claude Code interactive, with native question UI | Untested | |
| User-level install folders (`~/.claude/skills`, `~/.agents/skills`, `~/.config/opencode/skills`) | Untested | Paths are from each agent's documentation. Testing used project-level folders. |
| Cursor, Gemini CLI, GitHub Copilot, other Agent Skills clients | Untested | Should work if the client implements the spec; not verified |
| Installer tools such as `npx skills add`, the Claude Code plugin marketplace | Untested | |

All twelve scenarios have been run in Claude Code. Multi-turn behavior (custom and changed answers, the loop guard) was only exercised there. Results vary by model.

## Repository layout

```text
skills/guided-discovery/SKILL.md   the skill (the only file an agent needs)
examples/                          worked walkthroughs
tests/behavior-scenarios.md        manual behavior tests and results
scripts/validate.py                repository checks (stdlib Python)
.github/workflows/validate.yml     CI: skills-ref + repository checks
CHANGELOG.md                       version history
```

## Validation

```bash
# Spec check with the Agent Skills reference validator (not on PyPI; install from source)
pip install "git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref"
skills-ref validate skills/guided-discovery

# Size, version/changelog match, required files, links
python3 scripts/validate.py
```

CI runs both on every push and pull request. Behavior is checked by hand with the scenarios in `tests/`.

## Contributing

1. Open an issue describing the behavior you saw: agent, model, the prompt, and the reply.
2. Keep `SKILL.md` short. Every line is loaded into context on activation.
3. If you change behavior, add or update a scenario in `tests/behavior-scenarios.md` and record a result.
4. Bump `metadata.version` and add a `CHANGELOG.md` entry. CI fails if they disagree.

## License

[MIT](LICENSE)
