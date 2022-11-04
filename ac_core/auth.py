from logging import getLogger
from typing import cast
from bs4 import BeautifulSoup
import bs4

from .constant import _SITE_URL
from .interfaces.HttpUtil import HttpUtilInterface
from .utils import HTML_PARSER

logger = getLogger(__name__)


def is_logged_in(http_util: HttpUtilInterface) -> bool:
  html = http_util.get(f"{_SITE_URL}/home").text
  soup = BeautifulSoup(html, HTML_PARSER)
  dropdown_menus = soup.find_all('ul', class_="dropdown-menu")
  found_user_link = False
  for menu in dropdown_menus:
    a_s = menu.find_all('a')
    for a in a_s:
      if a['href'].startswith('/users/'):
        found_user_link = True

  return found_user_link


def fetch_login(http_util: HttpUtilInterface, username: str, password: str) -> bool:
  try:
    res = http_util.get(_SITE_URL + '/login')
    soup = BeautifulSoup(res.text, HTML_PARSER)
    csrf_token = cast(bs4.Tag, soup.find(attrs={'name': 'csrf_token'})).get('value')
    post_data = {
        'csrf_token': csrf_token,
        'username': username,
        'password': password,
    }
    res2 = http_util.post(url='https://atcoder.jp/login', data=post_data)
  except Exception as e:
    logger.exception(e)
  return is_logged_in(http_util)


class InvalidSessionError(Exception):
  DEFAULT_MESSAGE = "Your login session is invalid. please relogin."

  def __init__(self, message: str = DEFAULT_MESSAGE) -> None:
    super().__init__(message)


# TODO logout?
