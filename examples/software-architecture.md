# Example: software architecture

Shows: reading the context first, a dependent follow-up question, and an
authorization gate that a "you decide" does not get past.

**Context:** a repository containing a Django monolith with a Postgres database
and Celery workers.

**User:** "We need to add real-time notifications."

The agent reads the repository before asking anything. It finds Django,
Postgres, Celery with Redis as the broker, and no WebSocket code. So it does not
ask about the stack. One decision decides the design:

> **Question 1: What must "real-time" mean for these notifications?**
> A. **In-app, while the page is open**: server-sent events or WebSockets via Django Channels (**Recommended**: Redis is already running as the Celery broker, so Channels adds little new infrastructure)
> B. **In-app, plus browser push when the tab is closed**: adds a service worker and push subscriptions
> C. **Polling every 15–30 s**: simplest, no new infrastructure, higher latency and load
> D. **Mobile push**: needs APNs/FCM credentials and a mobile app
>
> *Reply with a letter, your own answer, or "you decide".*

**User:** "A, but we're on Heroku."

The answer changes one dependent decision. Heroku's router supports WebSockets,
but it closes connections that stay idle for 55 seconds, so the transport choice
matters:

> **Question 2: Which transport?**
> A. **Server-sent events**: one-way, plain HTTP, reconnects on its own (**Recommended**: notifications only flow from server to client, and SSE is simpler to run behind Heroku's router)
> B. **WebSockets via Channels**: two-way; needs heartbeats to survive Heroku's idle timeout
> C. **You decide**
>
> *Reply with a letter, your own answer, or "you decide".*

**User:** "You decide. Just build it."

> **Decisions:** in-app notifications only; Heroku.
> **Assumptions:** SSE endpoint served by Django Channels, with Redis as the channel layer; a `Notification` model plus a migration; a 30 s heartbeat.
> **Open, non-blocking:** notification preferences UI, email fallback.
>
> Building it on a branch now. The new Heroku dyno type and the production migration need your approval when we get there.

The override ended the questions. It did not approve the production change.
