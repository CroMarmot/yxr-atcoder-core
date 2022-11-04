from dataclasses import dataclass
from typing import Dict, cast

from bs4 import BeautifulSoup
import bs4

from .constant import _SITE_URL
from .interfaces.HttpUtil import HttpUtilInterface, HttpRespInterface
from .url import url_2_contest_id
from .utils import HTML_PARSER


@dataclass
class SubmitResult:
  url: str


def fetch_fields(html: str) -> Dict[str, str]:
  soup = BeautifulSoup(html, HTML_PARSER)
  return {'csrf_token': cast(bs4.Tag, soup.find('input', attrs={'name': 'csrf_token'})).attrs['value']}


def problem_url_2_submit_url(problem_url: str) -> str:
  contest_id = url_2_contest_id(problem_url)
  return _SITE_URL + '/contests/' + contest_id + '/submit'


def fetch_submit(http_util: HttpUtilInterface, problem_url: str, lang_id: str, source_code: str) -> HttpRespInterface:
  problem_id = problem_url.split('/')[-1]
  submit_url = problem_url_2_submit_url(problem_url)
  html = (http_util.get(submit_url)).text
  post_data = {
      'sourceCode': source_code,
      'data.LanguageId': lang_id,
      'data.TaskScreenName': problem_id,
  }
  fields = fetch_fields(html)
  for key, val in fields.items():
    post_data[key] = val

  # TODO add test
  return http_util.post(url=submit_url, data=post_data)
