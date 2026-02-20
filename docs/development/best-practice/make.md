Make is an extremely useful tool across our codebase. It has two primary usecases:
- orchestrate complex data processing tasks, including running them in paralell on a single machine
- create phony targets for quick access to development commands

This page primarily focusses on the latter. 

## Make Versions

It's worth noting that macs come equiped  with GNU make v3.x instead of GNU 4.x . This is because of licence changes between the two versions. Our code bases use v4.x onwards so if you're on a mac it's worth upgrading see our guide [here](https://digital-land.github.io/technical-documentation/development/how-to-guides/installing-make/)

## Common Make Targets

This is the key section for developers. Almost every repo uses make to shorthand particular development commands. Over time a lot of targets have been created this guide aims to explain the meaning of each target in an attempt to create universal targets in each repo. 


```
make init
```

By far the most common target. It is primarily aimed at local and test environments. it's aim is to reduce the burden on developers when setting up a project/repo locally although it can also be used in other environments. it should install dependencies where possible, or at least flag that they will be needed in order to run the project by erroring and providing links to guidance on where to access them.

```
make test
```

Run unit, integration and acceptance tests for the repository. In a perfect world this can be ran directly after running init. It should also calculate test coverage for the repo and is how the CI/CD workflows run tests

```
make test-unit
make test-integration
make test-acceptance
```

These run the associated type of tests but DO NOT need to check coverage as we only measure coverage across all tests.

```
make upgrade
```

This should be used to upgrade dependency locks so as those in `requirement.txt`.