---
title: Onboarding Checklist
---

> NOTE  
> This is currently a Work In Progress

This is a curated task list aimed at developers joining the team. It covers general tasks that everyone should complete, followed by role-specific checklists for software developers, data engineers, and DevOps engineers.

---

## General (everyone)

### People and access
- Meet with your technical lead to understand the team structure and current priorities
- Meet with the product manager to understand the product vision and roadmap
- Create a GitHub account (or use an existing one) and ask your technical lead to get you added to the organisation with the correct permissions — **remove any personal access tokens from an existing account before using it**
- Get access to the relevant Slack channels — ask your technical lead if you are unsure which ones

### Reading
- Read the [Planning Data Handbook](https://team-playbook.planning-data.dev/)
- Read the [key development principles](/development/key-principles/)
- Review the [deploy and release procedure](/development/deploy-and-release-procedure/)
- Review the [Pull Request best practices](/development/best-practice/pull-requests/)
- Review the [CI/CD strategy](/architecture-and-infrastructure/ci-cd-strategy/)
- Read through [Onboarding in Data Operations](/data-operations-manual/Tutorials/Onboarding/) for a broad overview of the platform and the questions worth asking as you get started

---

## Software Developer (frontend and/or backend)

### Machine setup
- [ ] Run through the [Set Up for Mac](/development/tutorials/set-up-for-mac/) tutorial to install the base-level dependencies needed across most of our repositories

### Key repositories to clone
- [ ] [Planning Data platform](https://github.com/digital-land/digital-land.info) — the main website
- [ ] [Submit service](https://github.com/digital-land/submit) — tools to help data providers submit URLs for collection

### Get the applications running
- [ ] Follow the [Submit Service tutorial](/development/tutorials/submit-tutorial/) for an overview of the application architecture and instructions to get it running locally

### Best practices and conventions
- [ ] Review the [best practices documentation](/development/best-practice/) — all projects should follow these
- [ ] Confirm you can start a service using the standard make targets:
  ```bash
  make init
  make run
  ```

---

## Data Engineer

### Machine setup
- [ ] Run through the [Set Up for Mac](/development/tutorials/set-up-for-mac/) tutorial to install the base-level dependencies needed across most of our repositories

### Key reading
- [ ] Review the [data architecture overview](/architecture-and-infrastructure/data-architecture/)
- [ ] Work through the [Data Operations Manual](/data-operations-manual/) — pay particular attention to the Key Concepts and How-To Guides sections

### Key repositories to clone
- [ ] [Digital Land Python](https://github.com/digital-land/digital-land-python) — the core CLI and data processing library
- [ ] [Makerules](https://github.com/digital-land/makerules) — shared make targets used across data pipeline repositories
- [ ] [Specification](https://github.com/digital-land/specification) — dataset specifications and schemas
- [ ] [AWS Batch Docker](https://github.com/digital-land/aws-batch-docker) — Dockerfiles and entrypoints for batch processing tasks

### Get oriented
- [ ] Run through the [Running a Collection](/development/tutorials/running-a-collection/) tutorial
- [ ] Confirm you can set up a repository locally using:
  ```bash
  make init
  make test
  ```

---

## DevOps

### Key reading
- [ ] Review the [infrastructure documentation](/architecture-and-infrastructure/infrastructure/) in full, including deployment diagrams, code structure, security approach, and how-to guides
- [ ] Review the [CI/CD strategy](/architecture-and-infrastructure/ci-cd-strategy/) in depth — you will own and maintain these pipelines
- [ ] Review the [alerting and monitoring strategy](/architecture-and-infrastructure/alerting-and-monitoring/)
- [ ] Review the [architecture checklist](/architecture-and-infrastructure/architecture-checklist/)

### Key repositories
- [ ] Clone the infrastructure repository and review the structure with your technical lead — this is the primary repo you will work in
- [ ] Review the [Makerules](https://github.com/digital-land/makerules) repository as it underpins the CI/CD workflows across all other repositories
- [ ] Review the [AWS Batch Docker](https://github.com/digital-land/aws-batch-docker) repository

### Access and tooling
- [ ] Set up [AWS Vault](/architecture-and-infrastructure/infrastructure/how-to-guides/setup-aws-vault/) for secure credential management
- [ ] Confirm access to the relevant AWS environments with your technical lead
