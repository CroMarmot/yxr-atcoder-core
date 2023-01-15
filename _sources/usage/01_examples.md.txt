# Examples

Your need to provide a http `instance`, simpler you can just use `requests.session()` as your `instance`

Custom instance example:

```py
from ac_core.interfaces.HttpUtil import HttpUtilInterface,HttpRespInterface
class Helper(HttpUtilInterface,HttpRespInterface):

    def __init__(self, session):
        self.session = session # not necessary
        self.text = '' # necessary
        self.status_code = 0 # necessary

    # necessary
    def get(self, url: str, allow_redirects=True) -> HttpRespInterface:
        resp = self.session.get(url=url, allow_redirects=allow_redirects)
        self.status_code = resp.status_code
        self.text = resp.text
        return self

    # necessary
    def post(self, url: str, data: str) -> HttpRespInterface:
        resp = self.session.post(url=url, data=data)
        self.status_code = resp.status_code
        self.text = resp.text
        return self
```


## auth

### login and check login

```py
from ac_core.auth import fetch_login, is_logged_in
import requests
h = requests.session()
#h = Helper(requests.session())
print(is_logged_in(h))
print(fetch_login(h, 'username', 'password'))
```

## contest

### parse tasks page

`from ac_core.contest import parse_tasks`

```py
import requests
from ac_core.contest import parse_tasks

r = requests.get('https://atcoder.jp/contests/abc260/tasks')
if r.status_code == 200:
    print(parse_tasks(r.text)) # pass html
```

### fetch contest

`from ac_core.contest import fetch_tasks`

```py
from ac_core.contest import fetch_tasks
import requests
h = requests.session()
#h = Helper(requests.session())
print(fetch_tasks(h, 'abc259')) # pass contest id
```

## problem

### parse task page

`from ac_core.problem import parse_task`

```py
import requests
from ac_core.problem import parse_task

r = requests.get('https://atcoder.jp/contests/abc260/tasks/abc260_a')
if r.status_code == 200:
    print(parse_task(r.text))
```

## url

### parse contest id

`from ac_core.url import url_2_contest_id`

```py
from ac_core.url import url_2_contest_id
print(url_2_contest_id('https://atcoder.jp/contests/abc260/tasks/abc260_b'))
```

## language

### fetch supported language and language id

