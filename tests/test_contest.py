import os
from ac_core.contest import fetch_tasks, parse_tasks
from tests.Helper.MockHttpUtil import MockAsyncHttpUtil
from tests.constant import test_dir


def test_parse_tasks():
  with open(os.path.join(test_dir, './TestFiles/abc001.html')) as f:
    html = f.read()
  result = parse_tasks(html)

  assert result.url == "https://atcoder.jp/contests/abc001/tasks"
  assert result.start_time == 1381579200
  assert result.end_time == 1381586400
  assert result.name == "AtCoder Beginner Contest 001"

  assert len(result.problems) == 4
  problems = result.problems

  assert problems[0].id == 'A'
  assert problems[0].url == 'https://atcoder.jp/contests/abc001/tasks/abc001_1'
  assert problems[0].name == '積雪深差'
  assert problems[0].time_limit_msec == 2000  # ms
  assert problems[0].memory_limit_kb == 64000  # kb

  assert problems[1].id == 'B'
  assert problems[1].url == 'https://atcoder.jp/contests/abc001/tasks/abc001_2'
  assert problems[1].name == '視程の通報'
  assert problems[1].time_limit_msec == 2000  # ms
  assert problems[1].memory_limit_kb == 64000  # kb

  assert problems[2].id == 'C'
  assert problems[2].url == 'https://atcoder.jp/contests/abc001/tasks/abc001_3'
  assert problems[2].name == '風力観測'
  assert problems[2].time_limit_msec == 2000  # ms
  assert problems[2].memory_limit_kb == 64000  # kb

  assert problems[3].id == 'D'
  assert problems[3].url == 'https://atcoder.jp/contests/abc001/tasks/abc001_4'
  assert problems[3].name == '感雨時刻の整理'
  assert problems[3].time_limit_msec == 2000  # ms
  assert problems[3].memory_limit_kb == 64000  # kb


def test_fetch_tasks():
  http_util = MockAsyncHttpUtil()
  result = fetch_tasks(http_util, 'abc259')

  assert result.url == "https://atcoder.jp/contests/abc259/tasks"
  assert result.start_time == 1657368000
  assert result.end_time == 1657374000
  assert result.name == "AtCoder Beginner Contest 259"

  assert len(result.problems) == 8
  problems = result.problems
  assert problems[5].id == 'F'
  assert problems[5].url == 'https://atcoder.jp/contests/abc259/tasks/abc259_f'
  assert problems[5].score == 500
  assert problems[5].name == 'Select Edges'
  assert problems[5].memory_limit_kb == 1024000
  assert problems[5].time_limit_msec == 3000
  assert problems[5].tests[1].output == '2184\n'

  assert problems[7].id == 'Ex'
  assert problems[7].url == 'https://atcoder.jp/contests/abc259/tasks/abc259_h'
  assert problems[7].score == 600
  assert problems[7].name == 'Yet Another Path Counting'
  assert problems[7].memory_limit_kb == 1024000
  assert problems[7].time_limit_msec == 2000
  assert problems[7].tests[0].input == "2\n1 3\n3 1\n"
