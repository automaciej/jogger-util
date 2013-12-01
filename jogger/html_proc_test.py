import unittest
import os.path

from jogger import html_proc
from jogger import models

EXAMPLE_ENTRY = models.JoggerEntry(
    token='fake-token', op='add',
    entry_id='502734', draft_id='0',
    title='W Szczebrzeszynie chrząszcz brzmi w trzcinie',
    body='<p>Pchnąć w tę łódź jeża lub <span style="font-weight: '
    'bold;">ośm</span> skrzyń fig.</p>\n',
    permalink='w-szczebrzeszynie-chrzaszcz-brzmi-w-trzcinie', tags='tag1 tag2',
    trackback='', miniblog=True, techblog=False, allow_comments=0, level=2,
    notify=False,
    categories=[0, 1])

class ExperimentUnitTest(unittest.TestCase):

  def test1(self):
    datafile = os.path.join(os.path.dirname(__file__), 'testdata/page-1.html')
    with open(datafile) as fd:
      page1 = fd.read()
    # This might be too sensitive.
    expected = [
        {'id': '502734', 'token': 'fake-token'},
        {'id': '502733', 'token': 'fake-token'}]
    self.assertEqual(expected, html_proc.ExtractPostIds(page1))

  def testExtractEntryData(self):
    datafile = os.path.join(os.path.dirname(__file__), 'testdata/entry-no.html')
    with open(datafile) as fd:
      entry_html = fd.read()
    self.assertEqual(
        list(EXAMPLE_ENTRY._asdict().items()),
        list(html_proc.ExtractEntryData(entry_html)._asdict().items()))

  def testEncodeForm(self):
    expected = [
        ('entryID', '502734'),
        ('entryTitle', 'W Szczebrzeszynie chrząszcz brzmi w trzcinie'),
        ('entryTrackback', ''),
        ('draftID', '0'),
        ('allowComments', '0'),
        ('entryBody', '<p>Pchnąć w tę łódź jeża lub <span style="font-weight: bold;">ośm</span> skrzyń fig.</p>\n'),
        ('addCategory', ''),
        ('op', 'add'),
        ('entryLevel', '2'),
        ('submitEntry', 'Zapisz zmiany'),
        ('entryTags', 'tag1 tag2'),
        ('token', 'fake-token'),
        ('entryPermalink', 'w-szczebrzeszynie-chrzaszcz-brzmi-w-trzcinie'),
        ('entryCategory[]', '0'),
        ('entryCategory[]', '1'),
        ('specialCategory[]', 'miniblog'),
    ]
    saveDiff = self.maxDiff
    self.maxDiff = None
    self.assertEqual(
        sorted(expected),
        sorted(html_proc.EntryToData(EXAMPLE_ENTRY)))
    self.maxDiff = saveDiff

if __name__ == '__main__':
  unittest.main()
