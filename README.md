# ikeys-cli
[![Build Status](https://travis-ci.org/MrLYC/ikeys-cli.svg?branch=master)](https://travis-ci.org/MrLYC/ikeys-cli)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a60c4c155da142a7beea2d454495f347)](https://www.codacy.com/app/imyikong/ikeys-cli?utm_source=github.com&utm_medium=referral&utm_content=MrLYC/ikeys-cli&utm_campaign=badger)
[![codecov](https://codecov.io/gh/MrLYC/ikeys-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/MrLYC/ikeys-cli)
[![PyPI](https://img.shields.io/pypi/pyversions/ikeys-cli.svg)](https://pypi.python.org/pypi/ikeys-cli)

## Quick start

```python
from ikeys_cli import IKeytoneAPI
api = IKeytoneAPI(url=settings.IKEYTONE_URL)
api.authenticate(
    domain="server_domain",
    user="server_user",
    password="server_password",
    project="server_project",
)
result = api.domain.request.verify({
    "domian": "client_domain",
    "user": "client_user",
    "project": "client_project",
    "expires": "client_expires",
    "nonce": "client_nonce",
    "signature": "client_signature",
})

assert(result.errno == 0, result.errmsg)
print result.data
```
