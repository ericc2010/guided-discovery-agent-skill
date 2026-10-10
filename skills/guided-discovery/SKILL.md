---
name: guided-discovery
description: Adaptive intake for ambiguous or underspecified requests. Asks one multiple-choice question at a time, each with a recommended option, until the task is clear, then proceeds. Use when a missing decision about goal, audience, scope, platform, constraints, budget, risk, or output would change the result; when requirements conflict; or when the user asks to be interviewed, asks "what do you need to know?", or invokes guided discovery. Do not use when the request or context already answers what matters, or the user says "just build it" or "use your recommendations".
license: MIT
metadata:
  version: "1.0.0"
  repository: "https://github.com/ericc2010/guided-discovery-agent-skill"
---

# Guided Discovery

Resolve only the decisions that change the outcome, with the least user effort. Ask one question at a time, recommend an answer, and start work as soon as the task is clear enough.

This is not an interview script. Every question must earn its place.

## When to ask, when not to

Ask only if all three are true:
1. The answer is not already in the request, the conversation, the files, or the project.
2. Different answers would lead to materially different work.
3. No safe, reversible default exists, or a wrong guess would be expensive to undo.

Otherwise pick a sensible default, record it as an assumption, and keep going. A fully specified request gets zero questions.

## Process

1. **Read first.** Gather the objective, facts, constraints, implied preferences, and deliverable from everything available. Inspect files and context before asking about them.
2. **Rank the gaps privately.** List the missing decisions by impact and dependency. Never show the list as a questionnaire.
3. **Ask the single highest-value question** (format below).
4. **Interpret the reply.** Accept a letter, an option name, free text, a correction, or delegation ("you decide"). Delegation means applying your recommendation.
5. **Recompute.** After each answer, re-rank what is still missing. Drop questions that the answer made moot. Never re-ask a settled question.
6. **Stop** when the exit criteria are met, summarize, and proceed.

## Question format

**Question N: [one decision, one sentence]**

A. **[option]**: [trade-off]
B. **[option]**: [trade-off] (**Recommended**: [one-sentence reason])
C. **[option]**: [trade-off]

*Reply with a letter, your own answer, or "you decide".*

- Give 3 to 5 options that differ meaningfully. No filler options.
- Mark exactly one as **Recommended**, with a reason tied to what you know. If the recommendation depends on an assumption, say so.
- Number questions in order (1, 2, 3...). Never say "N of M", because the total is not fixed.
- If the host has a native single-choice question tool, use it. Put the recommended option first and label it "(Recommended)". Free text must still be possible.

## User overrides

- "Use your recommendations", "you decide the rest", "just build it", "stop asking": stop the intake. Apply your recommended defaults, summarize them, and proceed.
- An override ends *questions*, not *safety*. It does not authorize the actions listed under Authorization.
- If the user changes an earlier answer, update it, re-check only the decisions that depended on it, and say briefly what changed.
- If new information contradicts an earlier answer, or two requirements conflict, ask one question that names the conflict and offers resolutions. Do not silently pick one side.

## Authorization is not information

Two different kinds of gap exist:
- **Informational:** what to build, for whom, how. Defaults and "you decide" can settle these.
- **Authorization:** permission to act. A recommendation, a selected option, or "just build it" is not permission for an action whose effects reach beyond the working copy or are hard to undo.

Get explicit approval for that specific action, immediately before doing it, when it would:
- delete or overwrite data, or cause any other irreversible change;
- deploy, publish, push, send messages, or otherwise act outside the local workspace;
- spend money, change billing, or make purchases;
- change credentials, permissions, access, or security settings.

Approval for one such action does not carry over to the next. If the environment or the user has already granted standing permission, follow it.

## Exit criteria

Stop asking when any of these is true:
- The goal, deliverable, and critical constraints are clear enough that further answers would not change the work.
- What remains is low-impact or reversible and can be stated as an assumption.
- The user has told you to proceed.

Loop guard: if three or more questions have gone by and the task is still unclear, stop. Summarize what you know, state the defaults you would use, and ask once whether to proceed. Never ask a question you already asked, and never ask more questions just to fill a plan.

If one high-impact decision is still open and guessing would be unsafe or very likely wrong, you may ask it even after an override. Explain in one line why it cannot be defaulted.

## Hand-off

Before starting the work, give a short summary:

- **Decisions:** what the user chose.
- **Assumptions:** the defaults you applied, each one changeable.
- **Open, non-blocking:** items you can settle later.

Then start the work in the same response, if you are allowed to. If an authorization gate is next, stop at that gate and ask for that action only.

## Anti-patterns

- More than one question in a message, or a form.
- Asking about anything the context already answers.
- Presenting options as equal when one is clearly better.
- Asking the user to confirm minor defaults.
- Questioning after the task is actionable.
- Treating "Recommended" or "just build it" as approval for a consequential action.
- Inventing constraints or facts to justify a question.

## Example

User: "Build me a customer portal."

> **Question 1: Who will use the portal first?**
> A. **Existing customers**: account and order self-service (**Recommended**: most portals exist to cut support load for current customers)
> B. **Prospective customers**: sign-up and lead capture; closer to a marketing site
> C. **Internal staff**: an admin tool; different security and UI needs
> D. **Mixed roles**: widest scope; needs role-based access from day one
>
> *Reply with a letter, your own answer, or "you decide".*

User: "A. Use your recommendations for the rest and build it."

> **Decisions:** existing customers.
> **Assumptions:** Next.js and Postgres, email login, views for orders and account details, local dev only.
> **Open, non-blocking:** branding, payment integration.
>
> Starting with the project scaffold. I will ask before deploying anything.
