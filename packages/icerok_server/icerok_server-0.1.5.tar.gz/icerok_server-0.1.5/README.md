[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]


# icerok-server
Receive data from the icerok circuits on the FPGA

## Installation

```
pip install -U icerok_server
```


## Developers

### First clone

Make sure you create a virtual environment

* Install `python3-venv`

```
sudo apt install python3-venv
```

* Create the virtual environment

```
cd icerok-server-python
. env/bin/activate
```

* Install `flit`

```
pip install flit
```

### Run all the checks

```
tox
```

### Execute `icerok-server`

```
python3 icerok_server/main.py
```

### Publish in TestPyPi

```
flit publish --repository pypitest
```

### Publish package

* Increase version number in `icerok_server/__init__.py`
* Execute:
```
flit publish
```

## Credits

* Thanks to [Anton Zhiyanov](https://github.com/nalgeon) for this wonderful article: [How to make an awesome Python package in 2021](https://antonz.org/python-packaging/) 

<!-- Badges -->
[pypi-image]: https://img.shields.io/pypi/v/icerok_server
[pypi-url]: https://pypi.org/project/icerok_server/
[build-image]: https://github.com/FPGAwars/icerok-server-python/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/FPGAwars/icerok-server-python/actions/workflows/build.yml