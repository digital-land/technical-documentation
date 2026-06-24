---
title: Python Virtual Environments
---

A virtual environment (venv) is an isolated Python installation for a single project. It keeps that project's dependencies separate from every other project on your machine, so installing or upgrading a package in one repo can't break another.

Every Python repo in our codebase expects you to have a virtual environment set up before running it.

## Creating a virtual environment

Run the following in the root of the repo:

```sh
python -m venv .venv
```

This creates a `.venv` folder containing a copy of the Python interpreter and an isolated `site-packages` directory. The Python version used is whichever `python` resolves to in your current shell — if you're using pyenv with a `.python-version` file in the repo, that version is used automatically.

## Activating a virtual environment

```sh
source .venv/bin/activate
```

Once activated, your shell prompt will change to show the environment name. From this point, `python` and `pip` refer to the versions inside `.venv`, not the system ones.

## Installing dependencies

Most repos include a `requirements.txt` or use `make` to handle setup. With your venv activated:

```sh
pip install -r requirements.txt
```

or check the repo's `Makefile` for an `init` or `setup` target:

```sh
make init
```

## Deactivating a virtual environment

```sh
deactivate
```

This returns your shell to its normal state. The `.venv` folder stays in place so you can reactivate it later.

## Aliases

Working with venvs involves the same commands repeatedly. The `setup.sh` script adds two aliases to `~/.zshrc` to make this faster:

```sh
alias mkvenv='python -m venv .venv && source .venv/bin/activate'
alias workon='source .venv/bin/activate'
```

If you're setting up manually, add those lines to your `~/.zshrc` and run `source ~/.zshrc`.

With them in place:

* `mkvenv` — creates a fresh `.venv` in the current directory and activates it. Run this once when you first clone a repo (or when you want to start from scratch).
* `workon` — activates the existing `.venv`. Run this at the start of each terminal session when working on a project.

## Tips

**Recreating a venv** — delete the `.venv` folder and run `mkvenv` again. This is the fastest way to resolve dependency conflicts or a broken environment.

**One venv per repo** — don't share a venv across repos. Each project pins its own dependency versions and they will conflict.

**Don't commit `.venv`** — it is already listed in the root `.gitignore` in our repos, but worth knowing. Venvs are machine-specific and should always be recreated locally.

**pyenv and venvs** — if the repo has a `.python-version` file, pyenv will have already switched to the correct Python version before you run `mkvenv`. You don't need to do anything extra.
