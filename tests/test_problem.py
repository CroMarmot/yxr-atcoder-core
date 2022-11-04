from py import test
from ac_core.problem import parse_task
from tests.constant import test_dir
import os


def test_parse_task():
  with open(os.path.join(test_dir, './TestFiles/abc003_4.html')) as f:
    html = f.read()
  result = parse_task(html)

  assert result.id == "D"
  assert result.url == "https://atcoder.jp/contests/abc003/tasks/abc003_4"
  assert result.name == "AtCoder社の冬"
  assert result.memory_limit_kb == 64000
  assert result.time_limit_msec == 2000
  assert result.contest_start == 1386853200
  assert result.contest_end == 1386860400
  assert result.contest_name == "AtCoder Beginner Contest 003"
  assert result.contest_url == "https://atcoder.jp/contests/abc003"

  assert len(result.tests) == 4
  tests = result.tests
  assert tests[0].input == "3 2\n2 2\n2 2\n"
  assert tests[0].output == "12\n"
  assert tests[1].input == "4 5\n3 1\n3 0\n"
  assert tests[1].output == "10\n"
  assert tests[2].input == "23 18\n15 13\n100 95\n"
  assert tests[2].output == "364527243\n"
  assert tests[3].input == "30 30\n24 22\n145 132\n"
  assert tests[3].output == "976668549\n"

def test_parse_task2():
  with open(os.path.join(test_dir, './TestFiles/abc276_e.html')) as f:
    html = f.read()
  result = parse_task(html)

  assert result.id == "E"
  assert result.url == "https://atcoder.jp/contests/abc276/tasks/abc276_e"
  assert result.name == "Round Trip"
  assert result.memory_limit_kb == 1024000
  assert result.time_limit_msec == 2000
  assert result.contest_start == 1667653200
  assert result.contest_end == 1667659200
  assert result.contest_name == "AtCoder Beginner Contest 276"
  assert result.contest_url == "https://atcoder.jp/contests/abc276"

  assert len(result.tests) == 3
  tests = result.tests
