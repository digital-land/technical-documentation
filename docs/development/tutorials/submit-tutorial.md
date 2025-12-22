---
title: Working on the Submit Service
---

## How the app is wired
- The service is a Node + Express app, started from `index.js`.
- App setup is split into small “setup” modules (middleware, routes, templating, session, error handling).
- Runtime config comes from `config/` based on `NODE_ENV` (with `.env` overrides via `dotenv`).
- All requests are sent to the [async service](https://github.com/digital-land/async-request-backend), this can be run locally or with the docker file. This actual 'computation' happens in this service with the idea that no business logic other than UI is done on this service.

## Middleware structure (how routes work)
- Most pages are built as **middleware chains**: small, focused middleware functions composed in order.
- Common responsibilities are split up (validate inputs → fetch data → transform into template params → render).
- Shared helpers live in `src/middleware/common.middleware.js` and the “builder” helpers live in `src/middleware/middleware.builders.js`.

## Datasette
- The service reads most of its data by querying [**Datasette**](datasette.planning.data.gov.uk).
- Some queries are dataset-scoped (e.g. `digital-land`, `performance`), and a small set of reads use a platform API instead of SQL.
- There is a interest to move all queries to (pipeline API)[https://github.com/digital-land/pipeline-internal-api] / or use the main platform API for speed and cost savings.

## Data Storage
- **Sessions**: User journey state (including HMPO wizard state) is stored in the Express session. When Redis is configured and available, sessions are persisted in Redis; otherwise the app falls back to an in-memory session store.
- **Redis-backed caches (performance)**: Redis is also used to cache a few “reference lists” to reduce repeat work and expensive queries.
  - Organisation list for the organisations page: cached for **6 hours**.
  - Dataset subject map (the grouped dataset list shown in the UI): cached with a shorter TTL in `local`/`development` and a longer TTL in other environments (currently **~1 minute** locally vs **~1 hour** elsewhere).
- **What’s stored**: These caches store non-sensitive, derived data (lists/mappings) rather than uploaded files.
- **Failure mode**: If Redis is unavailable, the service will still run, but will rebuild these lists more often (slower page loads, more upstream calls).

## HMPO form wizard (multi-step journeys)
- Multi-page flows use `hmpo-form-wizard`.
- There are two main wizards:
  - `/check` (the check tool)
  - `/submit` (endpoint submission form; typically feature-flagged)
- Each wizard is defined by:
  - `steps.js` (the journey / routing between steps)
  - `fields.js` (field validation rules)
  - controllers for step-specific behaviour and session-backed state

## Important Links
-   [Architecture Diagrams](/architecture-and-infrastructure/solution-design/check-service/)
-   [Debugging Async Service](/development/live-service/debugging-live-services/) Important to know how to use the Async service as well for this service, Postman is useful for checking what data is being sent between the services.