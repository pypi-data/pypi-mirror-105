# icerok-server
Receive data from the icerok circuits on the FPGA

* Package in pypi: [icerok_server](https://pypi.org/project/icerok_server/)

## Installation

TODO


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