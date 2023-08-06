# BDSpace

![Build](https://github.com/bond-anton/BDSpace/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/bond-anton/BDSpace/branch/master/graph/badge.svg)](https://codecov.io/gh/bond-anton/BDSpace)

**BDSpace** is a python package to simplify positioning, movement, and trajectory calculation for many
different technical problems. It is mainly for multiple interacting bodies systems like coordinate stages
and machining tools, robotic arms, manipulators, etc.

**BDSpace** provides following basic features:

|Feature                               |Staus             |
|--------------------------------------|------------------|
|Cartesian coordinate systems          |done              |
|Spherical coordinates                 |done              |
|Cylindrical coordinates               |done              |
|Conversion between coordinate systems |done              |
|Multiple nested coordinate systems    |done              |
|Parametric curves                     |done              |
|Trajectory builder (Pathfinder module)|endless work      |
|Planes and plane geometry             |work in progress  |
|...                                   |discussion is open|

## Installation

BDSpace depends on numpy and [BDQuaternions](https://github.com/bond-anton/BDQuaternions) packages only.
It is compatible with Python 2 and Python 3.

To install BDSpace type in a shell
```shell
pip install BDSpace
```
or in the root directory of BDQuaternions distribution run
```shell
python setup.py install
```
## Usage

Please see the demo directory for the usage examples.

## License

BDSpace is free open source software licensed under Apache license version 2.0
