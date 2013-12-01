import urllib.parse
import bs4
import logging

from jogger import models


ALLOW_COMMENTS = dict(
    all=0,
    jogger=1,
    nobody=2,
)


def ExtractPostIds(html):
  soup = bs4.BeautifulSoup(html)
  ids = []
  for entry in soup.select('div#content > div.wrap > form > div.entry.columns'):
    link = entry.select('div.sidebar > div.padding > ul.actions > li.default > a')[0]
    parsed = urllib.parse.urlparse(link.get('href'))
    d = urllib.parse.parse_qs(parsed.query)
    d2 = dict(id=d['id'][0], token=d['token'][0])
    ids.append(d2)
  return ids

def ExtractLastPageNumber(html):
  """Returns page number and token."""
  soup = bs4.BeautifulSoup(html)
  page_links = soup.select('div[class=division] div[class~="pager"] ul li a')
  logging.debug('page links: %r', page_links)
  if not page_links:
    return 1
  page_indexes = []
  for link in page_links:
    url = link.get('href')
    parsed = urllib.parse.urlparse(url)
    d = urllib.parse.parse_qs(parsed.query)
    page_index = int(d['page'][0])
    token = d['token'][0]
    page_indexes.append((page_index, token))
  return max(page_indexes, key=lambda x: x[0])

def ExtractEntryData(html):
  def IsChecked(checkbox):
    return checkbox.get('checked') == 'checked'
  soup = bs4.BeautifulSoup(html)
  notify = False
  categories = []
  for checkbox in soup.select('input[type=checkbox]'):
    value = checkbox.get('value')
    if value == 'miniblog':
      miniblog = IsChecked(checkbox)
    elif value == 'techblog':
      techblog = IsChecked(checkbox)
    elif checkbox.get('name') == 'entryNotify':
      if IsChecked(checkbox):
        notify = True
    elif checkbox.get('name') == ('entryCategory[]'):
      if IsChecked(checkbox):
        categories.append(int(value))

  allow_comments = None
  for comment_button in soup.select('input[name=allowComments]'):
    if comment_button.get('checked') == 'checked':
      allow_comments = comment_button.get('value')
  if allow_comments is not None:
    allow_comments = int(allow_comments)

  level = None
  for option in soup.select('select#entryLevel > option'):
    if option.get('selected') == 'selected':
      level = option.get('value')
  if level is not None:
    level = int(level)

  permalink = soup.select('input#entryPermalink')[0].get('value')

  return models.JoggerEntry(
    token=soup.select('input#token')[0].get('value'),
    op=soup.select('input[name=op]')[0].get('value'),
    entry_id=soup.select('input[name=entryID]')[0].get('value'),
    draft_id=soup.select('input[name=draftID]')[0].get('value'),
    title=soup.select('input#entryTitle')[0].get('value'),
    body=soup.select('textarea#entryBody')[0].text,
    permalink=permalink,
    tags=soup.select('input#entryTags')[0].get('value'),
    trackback=soup.select('input#entryTrackback')[0].text,
    miniblog=miniblog,
    techblog=techblog,
    allow_comments=allow_comments,
    level=level,
    notify=notify,
    categories=categories,
  )

def EntryToData(jogger_entry):
  """Encodes an entry named tuple into key/values."""
  data = [
      ('token', jogger_entry.token),
      ('op', jogger_entry.op),
      ('entryID', str(jogger_entry.entry_id)),
      ('draftID', str(jogger_entry.draft_id)),
      ('entryTitle', jogger_entry.title),
      ('entryBody', jogger_entry.body),
      ('submitEntry', 'Zapisz zmiany'),
      ('entryPermalink', jogger_entry.permalink),
      ('entryTags', jogger_entry.tags),
      ('entryTrackback', jogger_entry.trackback),
      ('allowComments', str(jogger_entry.allow_comments)),
      ('entryLevel', str(jogger_entry.level)),
      ('addCategory', ''),
  ]
  if jogger_entry.miniblog:
    data += [('specialCategory[]', 'miniblog')]
  if jogger_entry.techblog:
    data += [('specialCategory[]', 'techblog')]
  for category in jogger_entry.categories:
    data += [('entryCategory[]', str(category))]
  return data
