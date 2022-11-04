from dataclasses import dataclass
from logging import getLogger
import re
from typing import Dict, Iterator, List, NamedTuple, Optional, Tuple

from bs4 import BeautifulSoup
import bs4
from ac_core import contest
from ac_core.constant import _SITE_URL

from ac_core.utils import HTML_PARSER, get_direct_children_text, remove_prefix, remove_suffix
from ac_core.utils.html_parse_helper import parse_start_end, parse_url

logger = getLogger(__name__)


class SampleParseError(RuntimeError):

  def __init__(self, message: str = 'failed to parse samples'):
    super().__init__(message)


@dataclass
class TestCase():
  title: str
  input: str = ''
  output: str = ''


@dataclass
class ProblemResult():
  id: str
  url: str
  name: str
  score: int
  tests: List[TestCase]
  contest_name: str
  contest_url: str
  contest_start: int
  contest_end: int
  memory_limit_kb: int
  time_limit_msec: int


def _parse_score(soup: bs4.BeautifulSoup) -> Optional[int]:
  task_statement = soup.find('div', id='task-statement')
  p = task_statement.find('p')  # first
  if p is not None and p.text.startswith('配点 : '):
    score = remove_suffix(remove_prefix(p.text, '配点 : '), ' 点')
    try:
      return int(score)
    except ValueError:
      # some problems have scores like "<p>配点 : \(100\) 点</p>", not "<p>配点 : 100 点</p>"
      # example: https://atcoder.jp/contests/wupc2019/tasks/wupc2019_a
      pass
  return None


# Title in/out content
def _find_sample_tags(soup: BeautifulSoup) -> Iterator[Tuple[str, int, str]]:
  input_strings = ('入力例', 'Sample Input')
  output_strings = ('出力例', 'Sample Output')
  expected_strings = input_strings + output_strings

  def h3_2_title_inout(s: str) -> Tuple[str, int]:
    for prefix in input_strings:
      if s.startswith(prefix):
        return (s[len(prefix):].strip(), 0)
    for prefix in output_strings:
      if s.startswith(prefix):
        return (s[len(prefix):].strip(), 1)

    raise SampleParseError('Unknown input or output:' + str(h3))

  def get_header(tag, expected_tag_name):
    if tag and tag.name == expected_tag_name and tag.string and any(s in tag.string for s in expected_strings):
      return tag
    return None

  for pre in soup.find(id='task-statement').find_all('pre'):
    logger.debug('pre tag: %s', str(pre))

    # the standard format: #task-statement h3+pre
    # used by AtCoder's JavaScript, sometimes used with .prettyprint
    # example: https://atcoder.jp/contests/abc114/tasks/abc114_d
    # NOTE: The AtCoder's JavaScript (at https://atcoder.jp/public/js/contest.js?v=201911110917 version) supports:
    #     -   "#task-statement h3+pre" format for Copy buttons of <h3> and <pre> tags
    #     -   "pre.prettyprint" format for Copy buttons of <pre> tags
    h3 = get_header(tag=pre.find_previous_sibling(), expected_tag_name='h3')
    if h3:
      yield h3_2_title_inout(h3.text) + (pre.text, )
      continue

    # a old format: #task-statement h3+section>pre:first-child
    # partially supported by AtCoder's JavaScript
    # NOTE: The relaxed format "#task-statement h3+section>pre" may cause false-positive. e.g. https://atcoder.jp/contests/abc003/tasks/abc003_4
    # NOTE: The format "h3+section>pre.prettyprint" sometimes cause false-negative. e.g. https://atcoder.jp/contests/tdpc/tasks/tdpc_fibonacci
    # example: https://atcoder.jp/contests/abc003/tasks/abc003_4
    if pre.find_previous_sibling() is None and pre.parent.name == 'section':
      h3 = get_header(tag=pre.parent.find_previous_sibling(), expected_tag_name='h3')
      if h3:
        yield h3_2_title_inout(h3.text) + (pre.text, )
        continue

    # a very old format: #task-statement p+pre.literal-block
    # entirely unsupported by AtCoder's JavaScript
    # example: https://atcoder.jp/contests/utpc2011/tasks/utpc2011_1
    if 'literal-block' in pre.attrs.get('class', []):
      p = get_header(tag=pre.find_previous_sibling(), expected_tag_name='p')
      if p:
        yield h3_2_title_inout(p) + (pre.text, )
        continue


def _parse_sample_cases(soup: BeautifulSoup) -> List[TestCase]:
  """
    :raises SampleParseError:
  """
  s_dict: Dict[str, TestCase] = {}

  for title, inout, content in _find_sample_tags(soup):
    if title not in s_dict:
      s_dict[title] = TestCase(title=title)
    if inout == 0:
      s_dict[title].input = content.lstrip()
    elif inout == 1:
      s_dict[title].output = content.lstrip()
    else:
      assert (False)

  samples: List[TestCase] = []
  for title, inout, content in _find_sample_tags(soup):
    if inout == 0:
      samples.append(s_dict[title])

  return samples


def parse_task(html: str) -> ProblemResult:
  soup = BeautifulSoup(html, HTML_PARSER)
  h2 = soup.find('span', class_='h2')

  alphabet, _, name = get_direct_children_text(h2).strip().partition(' - ')

  time_limit, memory_limit = h2.find_next_sibling('p').text.strip().split(' / ')
  for time_limit_prefix in ('実行時間制限: ', 'Time Limit: '):
    if time_limit.startswith(time_limit_prefix):
      break
  else:
    assert False
  if time_limit.endswith(' msec'):
    time_limit_msec = int(remove_suffix(remove_prefix(time_limit, time_limit_prefix), ' msec'))
  elif time_limit.endswith(' sec'):
    time_limit_msec = int(float(remove_suffix(remove_prefix(time_limit, time_limit_prefix), ' sec')) * 1000)
  else:
    assert False

  # When login as the admin, a link is added after memory limit. See https://github.com/online-judge-tools/api-client/issues/90
  parsed_memory_limit = re.search(r'^(メモリ制限|Memory Limit): ([0-9.]+) (KB|MB)', memory_limit)
  assert parsed_memory_limit

  memory_limit_value = parsed_memory_limit.group(2)
  memory_limit_unit = parsed_memory_limit.group(3)
  if memory_limit_unit == 'KB':
    memory_limit_byte = int(float(memory_limit_value))
  elif memory_limit_unit == 'MB':
    memory_limit_byte = int(float(memory_limit_value) * 1000)
  else:
    assert False

  tests: List[TestCase] = []

  try:
    tests = _parse_sample_cases(soup)  # type: Optional[List[TestCase]]
  except SampleParseError as e:
    logger.error(str(e))
    pass

  score = _parse_score(soup)
  url = parse_url(soup)
  contest_info = soup.find(class_="contest-title")
  contest_name = contest_info.text
  contest_url = _SITE_URL + contest_info["href"]
  start_time, end_time = parse_start_end(soup)

  return ProblemResult(
      id=alphabet,
      url=url,
      name=name,
      time_limit_msec=time_limit_msec,
      memory_limit_kb=memory_limit_byte,
      tests=tests,
      score=score,
      contest_name=contest_name,
      contest_url=contest_url,
      contest_start=start_time,
      contest_end=end_time,
  )

