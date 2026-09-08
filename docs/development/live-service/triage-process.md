---
title: Live service triage and prioritisation
---

# Live service triage and prioritisation

This page describes how we handle issues that might be bugs, weird data, or live
service problems - from someone noticing something to a fix being picked up.

## Scope

This process covers issues in the platform team's remit:

- data pipelines
- Manage
- Check and Provide
- DevOps

It does **not** yet cover the remit of the Consumers or Design teams. This still needs to be agreed with those teams.

Issues typically reach us from:

- local planning authorities (LPAs) getting in touch
- someone in the team, or another team, noticing something that looks wrong
- alerts in `#planning-data-alerts`

If the service is actively degraded or down, this is an incident - go straight to
[Managing technical incidents](https://digital-land.github.io/technical-documentation/run-book/managing-technical-incidents/).

## 1. Investigate

Whoever finds the issue should do a **timeboxed investigation** to confirm it,
where possible. The
[run book](https://digital-land.github.io/technical-documentation/run-book/how-to-resolve-certain-issues/)
lists procedures for common problems.

If it looks like a **weird data** issue, flag it with the Senior Data Manager for initial
investigation. See also the
[data quality analysis and investigations](https://digital-land.github.io/technical-documentation/data-operations-manual/Tutorials/Monitoring-Data-Quality/Analysis-Investigations/)
guidance.

Many issues are resolved at this stage through configuration changes and go no
further.

## 2. Raise a ticket

If investigation points to something we need to fix, and it can't be resolved
easily through config changes or similar:

1. Create a ticket in the **Live Service** workstream, using the template in
   [Raising a live service ticket](https://digital-land.github.io/technical-documentation/development/live-service/raise-a-request/).
2. Place it in the **Sprint Backlog**.
3. Flag it to the Product Manager.

## 3. Review and prioritise

The Product Manager reviews the ticket, does a small refinement, and assigns a
priority. What happens next depends on that priority.

| Priority | Meaning | What happens |
| --- | --- | --- |
| P1 / P2 | Significant parts of the service are down or incorrect | The Product Manager flags it in the team channel with `@here`. We expect the team to drop current tickets to focus on it, and to follow the [incident response procedure](https://digital-land.github.io/technical-documentation/run-book/managing-technical-incidents/). |
| P3 / P4 | Everything else | Stays on the board for discussion at the next stand up (see below). |

Priority levels are defined in the
[incident priority table](https://digital-land.github.io/technical-documentation/run-book/managing-technical-incidents/#incident-priority-table).

## 4. Decide at stand up

Anything that isn't a P1 or P2 is discussed at the next stand up. There, we
decide whether it goes into:

- the **Sprint Backlog** for the relevant team, or
- the **Backlog**

Factors that influence this include:

- **Source of the issue.** We aim to resolve issues raised by LPAs within
  **5 working days**.
- Current team priorities.
- What other tickets are already being worked on.

## 5. Pick up the work

If a ticket is prioritised, a relevant team member picks it up once - and only
once - they have finished their current ticket.

We do not abandon in-progress tickets for live service work, other than in the
P1 or P2 situation described above.

## Summary

```
                  Issue noticed
                        |
             Timeboxed investigation
          (weird data -> Data Manager first)
                        |
              Fixable via config? --- yes ---> done
                        |
                        no
                        |
        Ticket raised in Live Service workstream
              -> Sprint Backlog -> flag to PM
                        |
                 PM reviews + prioritises
                        |
            +-----------+-----------+
            |                       |
          P1/P2                   P3/P4
            |                       |
     @here in channel        Discussed at stand up
     drop current work              |
     follow incident         Sprint Backlog or Backlog
     procedure                      |
                             Picked up after current
                             ticket is finished
```
