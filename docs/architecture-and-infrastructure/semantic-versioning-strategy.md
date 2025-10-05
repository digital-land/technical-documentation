# Semantic Versioning Strategy (`SEMVER.md`)

## 1. Overview

Libraries and packages needed in this service follow **[Semantic Versioning](https://semver.org/)** (SemVer) for managing releases across all components (Python, JavaScript, etc.).

Semantic Versioning uses a **three-part number** to describe the version of a release:

```
MAJOR.MINOR.PATCH
```

Each part conveys a specific type of change:

| Part | Example | Meaning |
|------|----------|---------|
| **MAJOR** | `2.x.x` | Incompatible changes to public APIs or data contracts. |
| **MINOR** | `1.3.x` | Backward-compatible feature additions or enhancements. |
| **PATCH** | `1.2.4` | Backward-compatible bug fixes or maintenance updates. |

### Additional Suffixes

Pre-release and development versions may include suffixes such as:

| Suffix | Example | Meaning |
|---------|----------|----------|
| `-alpha`, `-beta`, `-rc` | `1.3.0-beta.1` | Indicates a pre-release version. |
| `.devN` or `+g<sha>` | `1.2.1.dev3+g123abc` | A development version based on the number of commits since the last tag and the Git commit SHA. |

> Notice: currently we are only using developer versions on majority of repos and we haven't adopted pre-release versions.

---

## 2. Git Tags and Release Management

Each release is marked in the **GitHub repository** using a **Git tag**.  
Tags serve as the **source of truth** for version numbers.

- Tags follow the SemVer format:  
  - `v1.0.0`  
  - `v1.2.3`  
- The leading `v` is conventional and supported by tooling like `setuptools-scm` and `npm`.

### Tagging Rules

1. Every release must have a corresponding tag.
2. Tags should always be created from the commit that represents the released code.
3. Development commits that are not yet tagged are treated as pre-release or `.dev` versions.

Example:

| Commit | Tag | Interpreted Version |
|---------|-----|---------------------|
| `abc123` | `v1.0.0` | 1.0.0 |
| `def456` | *(none)* | 1.0.1.dev1+gdef456 |
| `ghi789` | `v1.0.1` | 1.0.1 |

---

## 3. Python Versioning (using `setuptools-scm`)

The Python package automatically determines its version from Git tags using **[`setuptools-scm`](https://github.com/pypa/setuptools_scm)**.

### How it works

- `setuptools-scm` inspects Git metadata during installation or build.
- If a tag is present (e.g. `v1.2.0`), that becomes the package version.
- If additional commits exist after the tag, it generates a development version:

```
1.2.1.dev3+gabcdef
```
meaning “3 commits since v1.2.0”.

### Configuration

In your `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=64","setuptools-scm>=8"]
build-backend = "setuptools.build_meta"

[project]
name = "digital-land"
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "package_name/_version.py"
```

This automatically

* Downlods `setuptools_scm` when building the package
* Derives the version from Git tags.
* Writes it to `package_name/_version.py` for inclusion in builds. The file needs to be excluded in versionn control

To allow access to the version number at runtime the following code needs to be added to  `package_name/__init__.py`

```python
import logging
from importlib.metadata import version, PackageNotFoundError

logger = logging.getLogger(__name__)

PACKAGE_NAME="package-name"

try:
    __version__ = version(PACKAGE_NAME)
except PackageNotFoundError:
    # package is not installed
    logger.error(f"Package '{PACKAGE_NAME}' is not installed. So can not retieve version.")
    pass
```


Example Workflow (if version is 1.0.0):

1. Developer makes changes on brannch and merges into main. the version on the main branch becomes 1.0.1.devN+gSHA
2. When ready to release use the 'Publish' workflow in GitHub Actions to tag the main branch with the new version (also optionally release to PyPi). using that action you can choose which number to bump, by default the patch number is bumped.
3. on next installation from main version will be updated to 1.0.1 if default is used

---

