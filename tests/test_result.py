import os
from ac_core.result import SubmissionResult, parse_result, _problem_url_to_sub_url, _parse_json_url
from tests.constant import test_dir


def test_parse_result_0():
  with open(os.path.join(test_dir, './TestFiles/abc275_f_result.json')) as f:
    html = f.read()
  result = parse_result(html)

  assert result.score == 500
  assert result.id == "36185704"
  assert result.status == SubmissionResult.Status.AC
  assert result.time_cost_ms == 84
  assert result.mem_cost_kb == 74320


def test_parse_result_1():
  with open(os.path.join(test_dir, './TestFiles/abc284_submissions_38109148.1.json')) as f:
    html = f.read()
  result = parse_result(html)

  assert result.score == 0
  assert result.id == "38109148"
  assert result.status == SubmissionResult.Status.RUNNING
  assert result.time_cost_ms == 0
  assert result.mem_cost_kb == 0
  assert result.msg_txt == '1/20'

  with open(os.path.join(test_dir, './TestFiles/abc284_submissions_38109148.2.json')) as f:
    html = f.read()
  result = parse_result(html)

  assert result.score == 300
  assert result.id == "38109148"
  assert result.status == SubmissionResult.Status.AC
  assert result.time_cost_ms == 7
  assert result.mem_cost_kb == 3776
  assert result.msg_txt == ''


def test_problem_url_to_submission_url():
  assert _problem_url_to_sub_url("https://atcoder.jp/contests/abc275/tasks/abc275_f"
                                 ) == "https://atcoder.jp/contests/abc275/submissions/me?f.Task=abc275_f"


def test_parse_json_url():
  with open(os.path.join(test_dir, './TestFiles/abc275_f_submission.html')) as f:
    html = f.read()
  assert _parse_json_url(html) == "https://atcoder.jp/contests/abc275/submissions/me/status/json?sids[]=36185704"
