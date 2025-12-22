---
title: Installing GDAL
---

GDAL is a set of tools used for geospatial analysis and is needed across our  pipelines and in the main application.

There are a lot of  GDAL versions with some significant changes so be weary of different behaviour. The current version in the pipeline is 3.6.4 from ppa:ubuntugis/ppa in linux. This is because github actions is running an old version of linux and this is the most up to date gda available.

# on linux

run

```
    sudo add-apt-repository ppa:ubuntugis/ppa
    sudo apt-get update
	sudo apt-get install gdal-bin
```

# on Mac

This will install a more up to date version. For  the most part there are no significant changes but be weary

```
    brew  install gdal
```