---
title: Make Python Virtual Environments
---

To create a new python environment, type:

  `python3 -m venv --prompt . .venv --clear --upgrade-deps`

To activate the environment, type:

  `source .venv/bin/activate`

The python version used in the code to create a virtualenvironment will be the python version used  in the python venv so  if you have python3.8 instaled then you can run

  `python3.8 -m venv --prompt . .venv --clear --upgrade-deps`

to use python 3.8. 

this process is part of a day to day workflow so it's useful to set up some aliases:

```
  alias workon='source .venv/bin/activate'
  alias mkvirtualenv='python3 -m venv --prompt . .venv --clear --upgrade-deps && workon'
```

Add these to your bash_profile/zshrc/bashrc to make it easy to recreate venvs at any time