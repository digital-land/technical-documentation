# Python Best Practices

---

## Managing Python versions

> **Scope:** This applies to all repositories using Python

We use a mixture of Python versions across our repositories. To keep things manageable and reduce the support burden, we have agreed on a **maximum Python version** that should be used across all repos: **Python 3.13**.

The goal over time is to migrate all repositories to this version. When the team decides to raise the maximum version, this document will be updated to reflect that decision (see [ADR 21](../../architecture-and-infrastructure/architecture-decision-records/index.md#21-use-a-agreed-maximum-python-version-across-all-repositories)).

No repository should use a Python version higher than the agreed maximum. Repositories may use older versions during a migration period, or where there is a specific reason to do so (for example, if a platform constraint limits the available versions — such as the Python runtimes supported by AWS Lambda).

### Upgrading a repository's Python version

Any developer working on a repository can upgrade its Python version — you do not need to wait for a dedicated workstream. Before starting it is worth checking with other developers on the repo, as they may know of dependencies or constraints that could affect the upgrade (for example a library that hasn't yet released a compatible wheel for the new version).

**Steps to upgrade:**

1. Update the Python version in the relevant place(s) for that repo — common locations include:
   - `Dockerfile` (`FROM python:X.Y`)
   - `.github/workflows/*.yml` (`python-version`)
   - `pyproject.toml` (`requires-python`)
2. Re-generate pinned dependencies if the repo uses `pip-tools` (see [Pin dependencies](#pin-dependencies-in-applications-and-data-processing-tasks)).
3. Run the test suite and check for any deprecation warnings or breakages.
4. Open a pull request — the diff on dependency files gives reviewers a clear picture of what changed.

---

## Pin dependencies in applications and data processing tasks

> **Scope:** This applies to Python **applications** and **data processing pipelines** — services, APIs, scripts, and tools that are deployed or run in a controlled environment. It does **not** apply to Python **packages** (libraries intended to be installed by others), where pinning dependencies would cause conflicts for downstream users.

**Why:** Without pinned versions, `pip install` resolves the latest available package at build time. This means two builds from the same Dockerfile or environment can produce different results, making bugs hard to reproduce and CVEs in transitive dependencies hard to track or audit.

**How:** Use [`pip-tools`](https://pip-tools.readthedocs.io/) to maintain two files:

- `requirements/requirements.in` — the direct dependencies you care about (human-maintained)
- `requirements/requirements.txt` — the fully resolved, pinned dependency tree including all transitive dependencies (generated, committed to version control)

```
# requirements/requirements.in
datasette
uvicorn[standard]
gunicorn
```

```sh
# Install pip-tools (once, in your virtual environment)
pip install pip-tools

# Generate requirements.txt from requirements.in
pip-compile requirements/requirements.in
```

The generated `requirements.txt` pins every package in the dependency tree with an exact version and annotates where each dependency comes from:

```
datasette==0.65.2
    # via -r requirements.in
uvicorn[standard]==0.41.0
    # via -r requirements.in
websockets==16.0
    # via uvicorn
```

**To update dependencies:** edit `requirements/requirements.in` if needed, re-run `pip-compile`, and commit both files. The diff on `requirements.txt` gives you a clear record of exactly what changed and why.

It is also worth adding a Makefile target so the command is easy to find and consistent across the team:

```makefile
pip-compile:
	pip-compile requirements/requirements.in
```

**In a Dockerfile:**

```dockerfile
COPY requirements/requirements.txt .
RUN pip install -r requirements.txt
```

---

## References

- [pip-tools documentation](https://pip-tools.readthedocs.io/)
- [Python Packaging — Repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/)