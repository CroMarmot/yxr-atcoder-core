from dataclasses import dataclass
import os
from typing import Dict
from tests.constant import test_dir

url2file: Dict[str, str] = {}
url2file['https://atcoder.jp/contests/abc259/tasks'] = 'abc259.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_a'] = 'abc259_a.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_b'] = 'abc259_b.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_c'] = 'abc259_c.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_d'] = 'abc259_d.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_e'] = 'abc259_e.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_f'] = 'abc259_f.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_g'] = 'abc259_g.html'
url2file['https://atcoder.jp/contests/abc259/tasks/abc259_h'] = 'abc259_h.html'
url2file['https://atcoder.jp/contests/practice/submit'] = 'submit.html'

site304: Dict[str, str] = {}


@dataclass
class MockResp:
  status_code: int
  text: str


class MockAsyncHttpUtil:

  def get(self, url: str) -> MockResp:
    if url in url2file:
      filename = url2file[url]
      filepath = os.path.join(test_dir, 'TestFiles', filename)
      with open(filepath, 'r') as f:
        html = f.read()
      return MockResp(status_code=200, text=html)
    if url in site304:
      return MockResp(status_code=304, text='')
    return MockResp(status_code=404, text='')

  def post(self, url: str) -> str:
    # TODO
    return ''
