# acdumo

This app is a simple implementation of the [Accelerated Dual Momentum](https://engineeredportfolio.com/2018/05/02/accelerating-dual-momentum-investing/) investment strategy. It
queries a Yahoo Finance API for historical ticker price data, calculates ADM
statistics, and suggests a strategy.

## Installation

Install with pip:

```sh
pip3 install acdumo
```
or
```sh
pip3 install --user acdumo
```

Installation will require an extra step on macOS systems. Run the included `acdumo-install-certifi` command.

```sh
acdumo-install-certifi
```


## Usage

