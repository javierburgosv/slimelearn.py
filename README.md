slimelearn.py
=============

A very easy to use API wrapper for SlimeLearn written in Python.

Installing
----------

**Python 3.9.1 or higher is required**

To install the library:
```sh
pip install slimelearnpy
```

Client Example
-----------

The following code recives updates from the server every 3 seconds, and executes a jump if the player is ready to do so.

```python
from slimelearnpy import SlimeLearn

sl = SlimeLearn()

conf = {
    "req": "config",
    "payload": {
        "mode": "sec",
        "delay": 3,
    }
}

def my_agent(input_data):
    
    if input_data["player"]["state"] == 'idle':
        sl.jump()

sl.run("//localhost:8080", config=conf, function=my_agent)
```

More examples can be found in the examples folder.