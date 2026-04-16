# Pull Request Best Practices

---

## Requesting a review

Getting a review arranged early is one of the most effective ways to avoid delays in delivering work. A PR that sits unreviewed is a bottleneck — organise your reviewer as soon as the PR is ready, ideally in the same standup or shortly after.

**How:** Post in the relevant channel with the PR link and tag the individuals you'd like to review it. Tagging ensures they receive a notification and the request doesn't get lost in general conversation.

### Checklist for the person raising the PR

- [ ] The PR description clearly explains what the change does and why
- [ ] The PR is scoped to a single concern — avoid bundling unrelated changes
- [ ] The branch is up to date with the base branch
- [ ] You have self-reviewed the diff before requesting a review
- [ ] CI checks are passing
- [ ] A reviewer has been identified and organised — ideally in standup
- [ ] The PR link has been posted in the relevant channel with the reviewer(s) tagged

---

## Reviewing a PR

The reviewer's responsibility is to read the code, provide feedback, and approve or request changes. **Merging the PR is the responsibility of the person who raised it**, not the reviewer. Once a review is approved, the author decides when and whether to merge.

**Why:** The person raising the PR has the full context on whether the change is ready to go — they know about any dependencies, downstream effects, or timing considerations that a reviewer may not. Keeping the merge decision with the author avoids accidental merges and keeps accountability clear.

### Checklist for the person reviewing the PR

- [ ] You understand what the change is trying to do before reading the code
- [ ] The logic is correct and the approach makes sense
- [ ] Edge cases and error handling are considered
- [ ] No obvious security issues (e.g. untrusted input, exposed secrets, unsafe dependencies)
- [ ] Tests cover the change adequately
- [ ] The code is readable and consistent with the surrounding codebase
- [ ] Feedback is specific and actionable — avoid vague comments like "tidy this up"
- [ ] Once happy, approve the PR — do not merge it yourself unless explicitly asked to
