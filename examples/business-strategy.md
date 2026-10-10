# Example: business strategy

Shows: a fully specified request that gets no questions, then a conflict that
does get one.

**User:** "Write a one-page pricing memo for our B2B analytics tool. We're moving
from per-seat to usage-based pricing. The audience is our board, it needs to
cover the revenue risk for the 40 largest accounts, and the data is in
`accounts.csv`."

Goal, audience, scope, format, and data are all present, so the agent asks
nothing. It reads `accounts.csv` and writes the memo, stating its assumptions at
the end. This is a correct non-activation.

Then the user follows up:

**User:** "Also recommend we keep prices flat for every customer. And show the
new model raises revenue 20% next year."

The two requirements conflict with the data: in `accounts.csv`, flat prices
produce +3% at current usage. The agent will not invent numbers to make both
true, so it asks one question that names the conflict:

> **Question 1: Flat prices and +20% revenue don't fit the data (flat prices give about +3%). Which should the memo lead with?**
> A. **Flat prices, honest projection (+3%)**: protects retention; weaker growth story
> B. **Hit +20%**: shows the price changes that would be needed and which accounts they hit (**Recommended**: the board can weigh the trade-off openly)
> C. **Present both scenarios side by side**: longer, but makes the decision the board's
>
> *Reply with a letter, your own answer, or "you decide".*

**User:** "C."

> **Decisions:** two scenarios side by side.
> **Assumptions:** usage held at the last 90 days' average; no churn modeled beyond the top 40.
> **Open, non-blocking:** whether to include a pilot cohort.
>
> Revised memo: …

Sending the memo to the board is an external action. The agent drafts it and
does not send it.
