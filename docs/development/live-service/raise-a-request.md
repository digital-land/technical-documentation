---
title: Raising a live service ticket
---

# Raising a live service ticket

Before raising a ticket, do a timeboxed investigation to confirm the issue where
you can. See
[Live service triage and prioritisation](https://digital-land.github.io/technical-documentation/development/live-service/triage-process/)
for the full process, including what to do with weird data issues.

## Notify the team

Post the detail in the relevant team Slack channel and notify the Tech
Lead, Product Manager and Delivery Manager.

If significant parts of the service are down or returning incorrect data, this
is an incident. Follow
[Managing technical incidents](https://digital-land.github.io/technical-documentation/run-book/managing-technical-incidents/)
rather than waiting for triage.

## Create the ticket

Create the ticket in the **Live Service** workstream and place it in the
**Sprint Backlog**, then flag it to the Product Manager for review and
prioritisation.

## Ticket template

```
### Summary description
_A brief overview of the issue at a relatively non-technical level, including
who discovered it and when._

### Source
_Where did this come from? e.g. LPA contact, #planning-data-alerts, internal
observation, another team. Include the LPA name if applicable._

### Environment
_e.g. OS, browser, device, app version, network_

### Steps to reproduce

### Expected behaviour
_Include screenshots if applicable._

### Actual behaviour
_Include screenshots if applicable._

### Frequency
_How often does it occur? How many users are affected? When does it occur?_

### Impact and priority
- [ ] P1 Critical - complete outage, or ongoing unauthorised access
- [ ] P2 Major - substantial degradation of service
- [ ] P3 Significant - users experiencing intermittent or degraded service
- [ ] P4 Minor - component failure that does not immediately impact a service

### Estimated time and complexity
_Include any resource dependencies on other teams._
```

Priority levels are defined in the
[incident priority table](https://digital-land.github.io/technical-documentation/run-book/managing-technical-incidents/#incident-priority-table).
Use the same scale throughout - the priority set here is the one the Product
Manager confirms at review.

Recording the **source** matters: we aim to resolve issues raised by LPAs within
5 working days, and we can't measure that if we don't capture where the issue
came from.
