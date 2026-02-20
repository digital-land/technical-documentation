# Docker Best Practices

A reference for standard practices applied to our Dockerfiles, covering security and image hygiene.

---

## Run as a non-root user

**Why:** By default, Docker containers run as root. If an attacker exploits a vulnerability in your application (e.g. a CVE in a dependency), they inherit root privileges inside the container. On AWS, this increases the blast radius — a root process has more ability to interact with the instance metadata service and attached IAM roles.

**How:** Create a dedicated system user after all installation steps, transfer ownership of the app directory, then switch to that user before the entrypoint:

```dockerfile
RUN groupadd --system appuser && \
    useradd --system --gid appuser --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["bash", "startup.sh"]
```

**Key points:**
- All `apt-get` and `pip install` steps must run before `USER appuser` as they write to system paths
- `--system` creates a low-UID user with no login shell, reducing attack surface
- `--no-create-home` avoids creating an unnecessary home directory
- Port numbers above 1024 (e.g. 5000) can be bound by non-root users — this is not a problem

---

## Use COPY instead of ADD

**Why:** `ADD` has two behaviours beyond a simple file copy — it automatically extracts tar archives and can fetch files from remote URLs. The URL fetching in particular is a security risk (bypasses the build cache, introduces a remote dependency at build time). Using `ADD` where `COPY` suffices is also confusing to readers.

**Rule of thumb:** Always use `COPY`. Only use `ADD` when you explicitly need tar extraction.

```dockerfile
# Prefer this
COPY templates /app/templates

# Avoid this unless you need tar extraction
ADD templates /app/templates
```

---

## Clean up apt cache in the same layer

**Why:** Each `RUN` instruction creates a new image layer. If you install packages and delete the cache in separate `RUN` steps, the cache files are still stored in the earlier layer, increasing image size.

**How:** Chain the install and cleanup in a single `RUN`:

```dockerfile
RUN apt-get update && \
    apt-get install -y some-package && \
    rm -rf /var/lib/apt/lists/*
```

---

## Consider a read-only root filesystem (further hardening)

For higher-security environments, you can prevent the container process from writing to the filesystem at all. This limits what an attacker can do even if they achieve code execution.

In ECS task definitions:
```json
"readonlyRootFilesystem": true
```

In `docker-compose.yml`:
```yaml
read_only: true
tmpfs:
  - /tmp   # allow writes to /tmp if the process needs it
```

Note: Python processes may require `/tmp` for bytecode cache and temp files, so a `tmpfs` mount there is usually needed alongside a read-only root.

---

## References

- [Docker Official Docs — Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [OWASP Docker Security Cheat Sheet](https://cheats.owasp.org/)
- [AWS ECS Security Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/security-tasks-containers.html)