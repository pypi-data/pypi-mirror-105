# halca1006

This module provides support for the HAL CA1006 protocol.
It is intended to provide a device driver capability to allow integration of HAL CA1006 multi-zone
amplifiers into home automation systems like Home Assistant.
It can also be run in a standalone mode in order to test connectivity and protocol support.

## Installation

Run the following to install:

```python
pip install halca1006
```

## Standalone Usage
```bash
usage: hal.py [-h] [--log_level {debug,info,warning,error,critical}]
              [--hal_host HAL_HOST] [--hal_port HAL_PORT]

Expose HAL CA1006 multi-zone amplifier

optional arguments:
  -h, --help            show this help message and exit
  --log_level {debug,info,warning,error,critical}
                        Set logging level. Defaults to error.
  --hal_host HAL_HOST   The hostname or IP address of the HAL CA1006. Defaults
                        to localhost.
  --hal_port HAL_PORT   The HAL CA1006 IP port. Defaults to 7000.
```

## Integrated Usage

```python
from halca1006 import HALProtocol

# TODO: Add function examples - see if this can be self documenting from the code?
```
