# pytvm

[![PyPI version](https://badge.fury.io/py/pytvm.svg)](https://badge.fury.io/py/pytvm) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytvm)](https://pypi.org/project/pytvm/)
[![Downloads](https://static.pepy.tech/badge/pytvm)](https://pepy.tech/project/pytvm)
[![Downloads](https://static.pepy.tech/badge/pytvm/month)](https://pepy.tech/project/pytvm)
[![](https://img.shields.io/badge/%F0%9F%92%8E-TON-grey)](https://ton.org)

> :warning: **WARNING: The pytvm library is currently in active development. Features and functionality may change frequently. Please keep this in mind when using this library.**

**pytvm** - is a Python bindings to C++ TON Virtual Machine (TVM) emulator. **pytvm** allows you:

* Run Get-Methods locally (for trustless and fast data retrieval)
* Emulate messages (`Internal` and `External`)
* Emulate transactions
* Emulate transactions traces

## Usage

Find examples in the [examples](examples/) folder.

## Installation

### From PyPi

```commandline
pip install pytvm 
```

### From source
Currently, **pytvm** compatible with Python3.9 - Python3.11 on platforms:
* Linux (x86_64)
* Windows (x86_64)
* MacOS (x86_64, arm64)

If your system is not compatible with the pre-built wheels, you can install **pytvm** from source:

1) Compile `emulator` target TON Blockchain [repo](https://github.com/ton-blockchain/ton) or download `libemulator` binaries from
[latest release](https://github.com/ton-blockchain/ton/releases/latest).
2) Install **pytvm** from source:

    ```commandline
    pip install pytvm
    ```

3) Create engine providing path to `libemulator` binaries to `EmulatorEngineC`:

```python
from pytvm.engine import EmulatorEngineC
from pytvm.transaction_emulator import TransactionEmulator
engine = EmulatorEngineC('path/to/libemulator.so')
emulator = TransactionEmulator(engine=engine)
```

## Donation

TON wallet: `EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG`
