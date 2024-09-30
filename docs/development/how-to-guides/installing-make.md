# Installing Make

Make is used pretty consistently across our projects for making similar commands across applications or for executing the pipeline on a single machine.

1. check version of make

Make is installed on most machines so you may already have it.

```
make --version
```

This will print something similar to the below if it's installed or an error if not

```
GNU Make 4.4.1
Built for x86_64-apple-darwin23.4.0
Copyright (C) 1988-2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

If you get the  above and it's GNU Make then your already done. If it fails or the version you have is not GNU make then you need to install a more recent  version.

2. Install make

## On Linux

 To install the make package, enter:

    `sudo apt install make`

## On Mac (using brew)

run  

    `brew install make`

this will install the up to date version under `gmake` rather than `make` you can test using `--version` to ensure  your calling the right make either always use gmake or add

    `PATH="/usr/local/opt/make/libexec/gnubin:$PATH"`

to your bash_profile/bashrc/zshrc