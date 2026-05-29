# Git Best Practices

---

## Branch naming

> **Scope:** This applies to all repositories using GitHub

Branch names should follow the format:

```
{issue-number}-{short-description}
```

Where:
- `{issue-number}` is the GitHub issue number the branch relates to
- `{short-description}` is a brief, kebab-case summary of the change

**Examples:**

```
123-add-user-authentication
456-fix-date-parsing-bug
789-update-python-to-3-13
```

This format matches what GitHub auto-generates when you create a branch directly from an issue, so using that feature will give you a compliant branch name with no extra effort.

**If a branch is not tied to an issue**, use a short kebab-case description that makes the purpose clear:

```
docs-add-git-best-practice
hotfix-correct-broken-redirect
```

---

## Squash commits when merging to main

> **Scope:** This applies to all repositories using GitHub

When merging a pull request into `main`, **squash and merge** should be used rather than a standard merge or rebase.

**Why:** Squashing collapses all commits on a branch into a single commit on `main`. This keeps the main branch history clean and readable — each entry represents a complete, intentional change rather than a trail of work-in-progress commits. It also gives developers more freedom on their branch to commit freely, fix mistakes, and iterate without worrying about the permanent record.

**How:** Use GitHub's **Squash and merge** option when merging a pull request. The squashed commit message should clearly describe what the change does — GitHub will pre-populate it from the PR title, which should be descriptive enough to stand alone in the commit history.

![GitHub squash and merge option](https://docs.github.com/assets/cb-67313/mw-1440/images/help/pull_requests/select-squash-and-merge-from-drop-down-menu.webp)

> **Tip:** To enforce this, repository admins can restrict the allowed merge strategies under **Settings → General → Pull Requests** to "Squash merging" only.

---

## References

- [Pull request best practices](./pull-requests.md)
