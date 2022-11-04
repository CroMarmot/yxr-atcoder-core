from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup
from ac_core.constant import _SITE_URL

from ac_core.interfaces.HttpUtil import HttpUtilInterface


@dataclass
class LanguageKV:
  value: str
  text: str


def fetch_language(http_util: HttpUtilInterface) -> List[LanguageKV]:
  url = _SITE_URL + '/contests/practice/submit'
  resp = http_util.get(url)
  assert resp.status_code == 200
  soup = BeautifulSoup(resp.text, 'lxml')
  result: List[LanguageKV] = []
  tags = soup.find('div', attrs={'id': 'select-lang-practice_1'}).find('select')
  if tags:
    options = tags.find_all('option')
    for child in options:
      result.append(LanguageKV(value=child.get('value'), text=child.string))
  return result


# TODO get language list
# TODO add test