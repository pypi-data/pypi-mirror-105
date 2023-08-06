[![Pyversions](https://img.shields.io/pypi/pyversions/template-configurator.svg)](https://pypi.python.org/pypi/template-configurator)
![](https://github.com/linkml/template-configurator/workflows/Build/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/template-configurator.svg)](https://pypi.python.org/pypi/template-configurator)

# template-configurator
Configuration tool for LinkML model based templates.  This tool applies a configuration file, as defined in the
LinkML [configuration model](https://linkml.github.io/configurator-model/docs) and applies it to the supplied 
templates.


```text
usage: configure [-h] [--templatedir TEMPLATEDIR] [-t TARGETDIR] [--reset]
                 configfile

Configure a LinkML model repository

positional arguments:
  configfile            Model configuration file

optional arguments:
  -h, --help            show this help message and exit
  --templatedir TEMPLATEDIR
                        Template source directory (Default: template_configurator/templates)
  -t TARGETDIR, --targetdir TARGETDIR
                        Output target directory (Default: current working directory)
  --reset               Hard reset -- regenerate all files from scratch
```


__Note:__ This could really be generalized with very little effort.
