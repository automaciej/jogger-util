import requests
import urllib.parse

from jogger import models
from jogger import html_proc


class Error(Exception):
  """Generic error."""


class WebError(Error):
  """Problem occurred on the website."""


class JoggerAdminPanel(object):
  """Encapsulates calling the right URLs on Jogger."""

  def __init__(self, jabberid, password):
    self.session = requests.Session()
    self.Login(jabberid, password)

  def Login(self, jabberid, password):
    response = self.session.post(
        "https://login.jogger.pl/login/",
        data={
          'loginType': 'on',
          'op': 'login',
          'login_jabberid': jabberid,
          'login_jabberpass': password,
          # Join the existing session. Do not log out the user if the user is
          # logged in via the web interface.
          'login_session': '1',
          'login_openid': '',
          'login_remember': '1',
        },
    )
    cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
    if 'logged' not in cookies:
      logging.error(cookies)
      raise WebError('Not logged in.')

  def PanelHomepage(self):
    response = self.session.get('https://login.jogger.pl/entries/browse/')
    response.encoding = 'utf-8'
    return response.text

  def EntriesPageNo(self, page_no, token):
    qs = urllib.parse.urlencode([('page', page_no), ('token', token)])
    response = self.session.get(
        'https://login.jogger.pl/entries/browse/?%s' % qs)
    response.encoding = 'utf-8'
    return response.text

  def EntryById(self, entry_id, token):
    qs = urllib.parse.urlencode([('id', entry_id), ('token', token)])
    response = self.session.get(
        'https://login.jogger.pl/entries/compose/edit/?%s' % qs)
    response.encoding = 'utf-8'
    return response.text

  def SaveEntry(self, jogger_entry):
    """Saving an entry."""
    data = html_proc.EntryToData(jogger_entry)
    url = 'https://login.jogger.pl/entries/compose/edit/'
    response = self.session.post(url, data=data)
    response.encoding = 'utf-8'
    if response.status_code != 200:
      raise WebError('Saving entry failed.')
    return response.text
