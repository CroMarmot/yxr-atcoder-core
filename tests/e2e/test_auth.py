
def test_auth():
  from ac_core.auth import fetch_login, is_logged_in
  from tests.e2e.cfg import e2e_username, e2e_password
  import requests
  s = requests.session()
  assert not is_logged_in(s)
  assert fetch_login(s, e2e_username, e2e_password)
