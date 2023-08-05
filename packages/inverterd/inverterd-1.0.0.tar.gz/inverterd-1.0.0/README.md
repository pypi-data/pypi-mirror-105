# inverterd-client

This is a Python [inverterd](https://github.com/gch1p/inverter-tools) client library.

## Installation

It's available on Pypi:

```
pip install inverterd
```

## Usage example
```python
from inverterd import Client

c = Client(8305, '127.0.0.1')
c.format('json')
print(c.exec('get-status'))
print(c.exec('get-year-generated', (2021,)))
```

## License

MIT