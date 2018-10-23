# kubectl-py

[![Build Status](https://travis-ci.com/plombardi89/kubectl-py.svg?branch=master)](https://travis-ci.com/plombardi89/kubectl-py)

Tiny library that makes the Kubernetes command line too `kubectl` a little easier to use inside a Python program.

Nothing here is sophisticated or fancy, it is just code I found myself writing over and over again in various projects.

# Usage

```python
from kubectl import kubectl

res = kubectl("get pods")
```

# License

Apache 2.0, read [LICENSE](LICENSE) for complete details.
