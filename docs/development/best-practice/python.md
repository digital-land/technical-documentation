# Python Best Practices

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