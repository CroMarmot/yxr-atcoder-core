from ac_core.language import fetch_language
from tests.Helper.MockHttpUtil import MockAsyncHttpUtil


def test_fetch_language():
  http_util = MockAsyncHttpUtil()

  result = fetch_language(http_util)
  assert len(result) == 68
  check_cnt = 0
  for item in result:
    if item.value == '4003':
      assert item.text == 'C++ (GCC 9.2.1)'
      check_cnt += 1
    elif item.value == '4004':
      assert item.text == 'C++ (Clang 10.0.0)'
      check_cnt += 1

  assert check_cnt == 2
