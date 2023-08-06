# lhcbstyle

[![PyPI version](https://badge.fury.io/py/lhcbstyle.svg)](https://pypi.org/project/lhcbstyle)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/lhcbstyle)](https://github.com/conda-forge/lhcbstyle-feedstock)
[![Python 3.7‒3.9](https://img.shields.io/badge/python-2.7%2C3.5%E2%80%923.9-blue)](https://www.python.org)

TODO

## Usage

TODO

## Contributing

Creating a development environment
```bash
ssh://git@gitlab.cern.ch:7999/lhcb-docs/lhcbstyle.git
cd lhcbstyle
mamba create --name test-env root pytest pip setuptools_scm
pip install -e .[testing]
pre-commit install
curl -o lb-check-copyright "https://gitlab.cern.ch/lhcb-core/LbDevTools/raw/master/LbDevTools/SourceTools.py?inline=false"
chmod +x lb-check-copyright
```

Running the tests:
```bash
pre-commit run --all-files
pytest
```
