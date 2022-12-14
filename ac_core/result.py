from dataclasses import dataclass
from enum import Enum
import json
import os
import re

from bs4 import BeautifulSoup
from .constant import _SITE_URL
from .interfaces.HttpUtil import HttpUtilInterface


@dataclass
class SubmissionResult:

  class Status(Enum):
    INIT: str = 'Init'
    PENDING: str = 'Waiting for Judging'
    RUNNING: str = 'Judging'
    RE: str = 'Runtime Error'
    AC: str = 'Accepted'
    WA: str = 'Wrong Answer'
    CE: str = 'Compilation Error'
    TLE: str = 'Time Limit Exceeded'

  id: str = ''
  url: str = ''
  score: int = 500
  status: Status = Status.INIT
  time_cost_ms: int = 0
  mem_cost_kb: int = 0


def watch_result(url: str) -> str:  # sock url, single submissions
  return ''


# title=\"Compilation Error\"\u003eCE\u003c/span\u003e\u003c/td\u003e","Score":"0"
def parse_result(resp: str) -> SubmissionResult:
  res = json.loads(resp)["Result"]
  sub_id = list(res.keys())[0]
  soup = BeautifulSoup(res[sub_id]["Html"], "lxml")
  tds = soup.find_all('td')
  status = str(tds[0].find('span').attrs.get('title'))
  try:
    score = int(res[sub_id]["Score"])
  except:
    score = 0
  try:
    time_cost_ms = int(tds[1].text.split(" ")[0])
  except:
    time_cost_ms = 0

  try:
    mem_cost_kb = int(tds[2].text.split(" ")[0])
  except:
    mem_cost_kb = 0
  return SubmissionResult(
      id=sub_id,
      score=score,
      status=SubmissionResult.Status(status),
      time_cost_ms=time_cost_ms,
      mem_cost_kb=mem_cost_kb,
  )


def fetch_result_by_url(http_util: HttpUtilInterface, json_url: str) -> SubmissionResult:
  print(json_url)
  response = http_util.get(url=json_url)
  ret = parse_result(resp=response.text)
  ret.url = json_url
  return ret


def _problem_url_to_sub_url(problem_url: str) -> str:
  # problem_url https://atcoder.jp/contests/abc275/tasks/abc275_f
  r = re.match('^(.*)/tasks/(.*)$', problem_url)
  assert r is not None
  prefix = r.group(1)
  problem_suffix = r.group(2)
  # https://atcoder.jp/contests/abc275/submissions/me?f.Task=abc275_f
  return os.path.join(prefix, f'submissions/me?f.Task={problem_suffix}')


def _parse_json_url(html: str):
  soup = BeautifulSoup(html, 'lxml')
  # <a href='/contests/abc101/submissions/5371227'>Detail</a>
  r = re.search('<td class="text-center">.*?"/contests/(.*?)/submissions/([0-9]*?)\">Detail</a>', str(soup),
                re.DOTALL | re.MULTILINE)
  assert r is not None # no submission
  return os.path.join(_SITE_URL, f"contests/{r.group(1)}/submissions/me/status/json?sids[]={r.group(2)}")


# problem_url https://atcoder.jp/contests/abc275/tasks/abc275_f
def fetch_result(http_util: HttpUtilInterface, problem_url: str) -> SubmissionResult:
  # https://atcoder.jp/contests/abc275/submissions/me?f.Task=abc275_f
  submission_url = _problem_url_to_sub_url(problem_url)
  # <a href='/contests/abc101/submissions/5371227'>Detail</a>
  # https://atcoder.jp/contests/abc101/submissions/me/status/json?sids[]=5371077
  print(submission_url)
  resp = http_util.get(submission_url)
  json_url = _parse_json_url(resp.text)
  return fetch_result_by_url(http_util, json_url)
