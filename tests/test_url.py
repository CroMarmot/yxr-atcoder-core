from ac_core.url import url_2_contest_id


def test_url_2_contest_id():
  assert url_2_contest_id('https://kupc2014.contest.atcoder.jp/tasks/kupc2014_d') == 'kupc2014'
  assert url_2_contest_id('https://atcoder.jp/contests/agc030') == 'agc030'
  assert url_2_contest_id('https://atcoder.jp/contests/abc260/tasks/abc260_b') == 'abc260'
