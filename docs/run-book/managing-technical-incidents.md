---
title: Managing technical incidents
---

Our incident management focuses on restoring normal operations quickly with minimal impact on users.

## Define incident priority

Define technical incident priority levels for your service’s applications. For example potential incidents include:

- system access problems
- wider technical failures with possible reputational impact to MHCLG
- denial of service (DoS)
- data breach or leak
- defacement
- unauthorised use of systems
- suspicious activity, such as traffic from an unknown source

Assign a priority level to incidents based on their complexity, urgency and resolution time. Incident severity also determines response times and support level.

### Incident priority table

|Classification|Type|Example|Response time|Update frequency|
|---|---|---|---|---|
|#P1|Critical|Complete outage, or ongoing unauthorised access|20 minutes (office and out of hours)|1 hour|
|#P2|Major|Substantial degradation of service|60 minutes (office and out of hours)|2 hours|
|#P3|Significant|Users experiencing intermittent or degraded service due to platform issue|2 hours (office hours only)|Once after 2 business days|
|#P4|Minor|Component failure that does not immediately impact a service, or an unsuccessful DoS attempt|1 business day (office hours only)|Once after 5 business days|

## Incident response procedure

When an incident occurs the following process should be followed.

1. [Establish an incident lead](#1.-establish-an-incident-lead).
1. [Inform your team](#2.-inform-your-team).
1. [Prioritise the incident](#3.-prioritise-the-incident).
1. [Form an incident response team](#4.-form-an-incident-response-team).
1. [Investigate](#5.-investigate).
1. [Contain](#6.-contain).
1. [Eradicate](#7.-eradicate).
1. [Recover](#8.-recover).
1. [Communicate to a wider audience](#9.-communicate-to-a-wider-audience).
1. [Resolve the incident](#10.-resolve-the-incident).

### 1. Establish an incident lead

Establish who your incident lead is. Find out who noticed the problem and if anyone else is investigating and fixing it. If that person is you, assume the role of incident lead.

### 2. Inform your team

Inform the team using the below template in the [#planning-data-live-service-and-continuous-improvement](https://communities-govuk.slack.com/archives/C06RS99Q98A) channel in Slack. You can copy and paste it, then fill in the information in the square brackets.

```
🚨 *Incident Alert* 🚨
 
- *Issue detected:* [Brief description, e.g., High CPU usage, database lock, cache miss]
- *Current impact:* [Brief description, e.g., Users experiencing slowness]
- *Actions taken so far:* [E.g., scaling up ECS nodes, investigating locks]
- *Next steps:* [E.g., Monitoring, preparing to terminate blocking queries]
- *Estimated time to resolution:* [E.g., 10–15 minutes, under investigation]
```

If the incident involves a data or security breach, you must also notify:

- {the MHCLG security team?}
- {anyone else?}

### 3. Prioritise the incident

Prioritise the incident using the [incident priority table](#incident-priority-table) and start tracking actions, updates and communications. Make a copy of the [incident report template](https://docs.google.com/document/d/1qSOwjZYNMUzQcoWZNjiKvpVRVWjykVWAZmhrRn1ixhc/edit?tab=t.0) and use it to track updates and progress.

###  4. Form an incident response team

[Start a huddle](https://app.slack.com/huddle/T02BTKSTTRU/C06RS99Q98A) in the team channel and form a team with both an incident lead and a communications lead. The communications lead will make sure relevant parties are updated according to the incident priority table.

Make sure the scribe keeps the incident report document up to date, regularly adding new observations, actions and results (successful or unsuccessful). This means noting down anything said or done in the huddle. You can copy text from the chat too.

### 5. Investigate

Investigate the potential cause of the incident. Check the [run book](/run-book/) for a list of helpful procedures to try.

Make sure you keep your incident report up to date. If the incident involves a personal data breach follow your team’s GDPR documentation.

If the incident is a personal data or security breach you should follow steps 6, 7 and 8.
If the incident is not cyber security-related, skip to [step 9](#9.-communicate-to-a-wider-audience).

### 6. Contain

You should determine the right containment procedures. In some cases, you may require a forensic clone.

#### 6.1 Short-term containment

You should start short-term containment measures as soon as you detect an incident. This could help minimise impact and maintain availability. Make sure that all affected systems are isolated from the non-affected systems.

#### 6.2 Long-term containment

You’ll need to make sure long-term containment is in place.

You should take the system offline if possible. Once the system is offline, you can proceed to step 7.

If the system has to remain in production, remove all malware and other artifacts from the affected systems, and harden the affected systems from further attacks. You should reimage the affected systems, or restore from the last known good backup.

#### 6.3 Forensic clone

As well as gathering evidence to help resolve an incident, you should collect evidence to support any potential follow-on disciplinary or legal proceedings.

To maintain the forensic integrity of the environment you should:

- document all commands used during the investigation and keep the documentation up to date - include how the evidence has been preserved
- store any forensic images taken during the investigation in a secure location, to prevent accidental damage or tampering

### 7. Eradicate

Eradication may be necessary to remove components of the incident that remain on your systems, such as traces of malware. To help with eradication you should:

- identify all affected hosts
- remove all malware and other artifacts left behind by the attackers
- reimage and patch the affected system
- check backups, code, images and the affected systems are protected against further attacks

### 8. Recover

Recovery is necessary to reduce the impact on user confidence and to reduce the likelihood of further successful attacks.

You should:

- confirm the affected systems are patched and hardened against the recent attack, and possible future attacks
- decide what day and time to restore the affected systems back into production (if they were taken offline)
- check the systems you’re restoring to production are not compromised in the same way as the original incident
- consider how long to monitor the restored systems for, and what to look out for

### 9. Communicate to a wider audience

If the incident is serious (P1 or P2) you’ll need to contact a wider MHCLG audience and potentially your service users.

Your communications lead must manage:

- external and internal communications
- incident escalations

**External and internal communications**

Make sure internal and external parties, like Information Security or your service users are fully informed at every stage of your incident management process.

- Notify the service owner first
- Post a message in the wider team Slack channel
- Notify local planning authorities in the [#group-data-support channel on Open Digital Planning Slack](https://communities-govuk.slack.com/archives/C05NQJK5S9L)

**Incident escalations**

Notify the service owner of all high priority incidents (P1/P2). 

<!-- **Report cyber security incidents**

The incident lead, guided by the Information Security team, must inform the National Cyber Security Centre (NCSC) of any category 1, 2 or 3 incidents. The NCSC defines security incidents in its [categorisation system prioritisation framework](https://www.ncsc.gov.uk/news/new-cyber-attack-categorisation-system-improve-uk-response-incidents).

Depending on the incident, the NCSC may be able to provide technical support. -->

### 10. Resolve the incident

Work to resolve the incident and return the service to normal operations, where possible. Once the incident has been resolved it is a good idea to take a break.

Next, hold an incident and lessons learned review following a [blameless post mortem culture](https://codeascraft.com/2012/05/22/blameless-postmortems/) so your service can improve. 

Make sure that any actions to prevent similar incidents in the future are [written up as GitHub issues](https://github.com/orgs/digital-land/projects/9) and can be brought into future sprints.

## Incident roles

* **Incident lead**:  The role of the incident lead is to direct the incident response and lead on diagnosis and resolution. They may also make changes to application code and deployed infrastructure.
  * Requires read-write access to the AWS account hosting the applications that are experiencing an incident.
  * Requires read-write access to any GitHub repositories hosting code for the applications that are experiencing an incident.
* **Scribe**: The role of scribe is to maintain the incident report document during diagnosis and resolution of the incident. This also means keeping track of changes made to applications and infrastructure code. The scribe may also be the comms lead if a product or delivery manager is not available.
  * Requires edit access to the Google document tracking the incident.
  * Requires read-write access to the technical documentation repository.
* **Actor**: The role of actor is to assist in the incident response, approving any pull requests where needed.
  * Requires read-only access to the AWS account hosting the applications that are experiencing an incident.
  * Requires read-write access to any GitHub repositories hosting code for the applications that are experiencing an incident.
* **Comms lead**: The role of the comms lead is to make sure that internal and external parties are notified, and that P1 or P2 incidents are escalated to the service owner.
  * Requires edit access to the Google document tracking the incident.
  * Requires access to [#planning-data-live-service-and-continuous-improvement](https://communities-govuk.slack.com/archives/C06RS99Q98A) channel, wider team channel, and [#group-data-support channel](https://communities-govuk.slack.com/archives/C05NQJK5S9L) on Slack.