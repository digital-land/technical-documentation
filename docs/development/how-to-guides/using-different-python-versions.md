---
title: Using Multiple Python Versions
---

Across our projects there may be areas where you need to switch  between different python versions. For exampe the pipelline primarily uses 3.8 but apps tend to work better with 3.10. The  default python installed is quite often 3.10.

There are a lot of methods to do this including a pakcage called pyenv. pyenv has  proved difficult to use  for  us as  it  can leed to problems installing extensions in sqlite (specifically spatialite)

the approach  we ainly take is to install several versions of python and change the call that you  use when creating virtual environments.

## In Linux

The easiest way to install python 3.8 is from the [deadsnakes](https://github.com/deadsnakes) repository.

    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt install python3.8
    $ sudo apt install python3.8-venv

Then create [virtual environment](https://docs.python.org/3/library/venv.html) for Python 3.8 with
```python3.8 -m venv``` such as

    $ python3.8 -m venv .venv --clear --prompt $(basename $(pwd))
    
To check that the virtual environment is indeed using Python 3.8 run

    $ source .venv/bin/activate
    $ python -V

Which should display ```Python 3.8.18```


### Using a later version too

Even with python3.8 installed, the later (system) version of python will still be installed. In fact, this
will be the default version of python (unless someone has tinkered with the system). From ouside of any
virtual environment ```python -V``` should report the later version (currently ```Python 3.10.12```).

Virtual environments can be created for this version with ```python -m venv``` as usual.

It's worth noting that the system version of python can change with a Ubuntu update. If a specific version is required,
it would be best to install it from deadsnakes in a similar way to installing 3.8.

## In Homebrew

It is very simple using homebrew. run

    `brew install python@3.8`

then the python version can be accessed using python3.8

    `python3.8  --version`