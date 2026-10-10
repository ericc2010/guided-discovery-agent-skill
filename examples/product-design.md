# Example: product design

Shows: a custom answer, a changed earlier answer, and stopping early.

**User:** "Design an onboarding flow for our budgeting app."

> **Question 1: What should onboarding achieve first?**
> A. **Link a bank account**: fastest route to value; many users drop off at the credential step
> B. **Set a first budget manually**: gets users invested without a privacy hurdle (**Recommended**: lowers early drop-off, and bank linking can come second)
> C. **Import a spreadsheet**: suits power users switching tools
> D. **Product tour only**: cheapest to build, weakest at activation
>
> *Reply with a letter, your own answer, or "you decide".*

**User:** "Neither. Most of our users are couples, so inviting a partner is the moment it clicks."

That is a custom answer. The agent accepts it and re-ranks what is still open.
Shared ownership now matters more than the account-linking question, so it asks:

> **Question 2: When should the partner invite appear?**
> A. **First screen**: puts the shared value up front; solo users may bounce
> B. **After the first budget**: the inviter has something to show (**Recommended**: the invite lands with context)
> C. **Only in settings**: least friction, lowest invite rate
>
> *Reply with a letter, your own answer, or "you decide".*

**User:** "B. Actually, make bank linking the first step after all; legal approved Plaid."

The user has changed an earlier answer. The agent updates it and checks what
depended on it: the invite still follows a moment of value (the linked account).
It asks nothing new.

> **Decisions:** bank linking via Plaid first; partner invite after the first budget.
> **Assumptions:** mobile-first screens, skip link on every optional step, five screens at most.
> **Open, non-blocking:** copy tone, illustration style.
>
> Here is the flow: …

Two questions were enough. Copy tone was defaulted, not asked.
