# texttaglib

a Python library for managing and annotating text corpuses in different formats (ELAN, TIG, TTL, et cetera).

[![ReadTheDocs Badge](https://readthedocs.org/projects/texttaglib/badge/?version=latest&style=plastic)](https://texttaglib.readthedocs.io/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/letuananh/texttaglib.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/letuananh/texttaglib/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/letuananh/texttaglib.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/letuananh/texttaglib/context:python)

## Warning

⚠️ `texttaglib` package is now in maintenance mode for supporting legacy software only. All new development will be moved to [speach](https://pypi.org/project/speach/) library.

Migration from `texttaglib` to `speach` should be trivial

```python
# just change import statements from something like
from texttaglib import elan
# to 
from speach import elan
```

Installation

```bash
# change
pip install texttaglib 
# into
pip install speach
```

For more information, please visit: https://github.com/neocl/speach

## Legacy

texttaglib legacy releases (>= 0.1.1, < 0.2) use embedded chirptext-0.1 and puchikarui-0.1 for supporting legacy APIs.

Here is the sample code:

```python
from texttaglib import ttl
from texttaglib.chirptext import chio
from texttaglib.chirptext import deko
from texttaglib.puchikarui import Schema
```

Legacy documentation: https://texttaglib.readthedocs.io
