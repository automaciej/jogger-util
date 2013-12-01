#!/usr/bin/env python

"""Mass edit blog entries on jogger.pl.

You can create:

  jogger.ini

With content:

  jabberid = you@somedomain.somewhere
  password = your_password
"""

import argparse
import bs4
import configparser
import logging
import requests
import sys
import urllib

from jogger import html_proc
from jogger import models
from jogger import panel


def main():
  logging.basicConfig(level=logging.INFO)
  parser = argparse.ArgumentParser(
      description='Mass edit blog entries on jogger.pl')
  parser.add_argument('allow_comments', help='Set comment permissions',
      choices = sorted(html_proc.ALLOW_COMMENTS.keys()))
  parser.add_argument('--jabberid', help='Jabber ID.', type=str)
  args = parser.parse_args()
  if args.jabberid:
    password = input('Password for %s > ' % args.jabberid)
    jabberid = args.jabberid
  else:
    config = configparser.SafeConfigParser()
    config.read('jogger.ini')
    if not config.has_section('credentials'):
      parser.print_help()
      logging.error('JABBERID not set')
      sys.exit(1)
    jabberid = config.get('credentials', 'jabberid')
    password = config.get('credentials', 'password')

  # The numeric value.
  allow_comments = html_proc.ALLOW_COMMENTS[args.allow_comments]

  # We must fetch the panel homepage once to figure out how many pages of
  # entries there are.
  jogger_panel = panel.JoggerAdminPanel(jabberid, password)
  homepage = jogger_panel.PanelHomepage()
  last_page, token = html_proc.ExtractLastPageNumber(homepage)
  for page_no in range(1, last_page + 1):
    logging.info('Processing page %s / %s', page_no, last_page)
    entries_page_html = jogger_panel.EntriesPageNo(page_no, token)
    entry_ids = html_proc.ExtractPostIds(entries_page_html)
    for entry_id_dict in entry_ids:
      entry_id = entry_id_dict['id']
      token = entry_id_dict['token']
      post_entry_html = jogger_panel.EntryById(entry_id, token)
      post_entry = html_proc.ExtractEntryData(post_entry_html)
      logging.info('Processing entry %r', post_entry.title)
      post_entry = post_entry._asdict()
      # The entry can be modified here.
      post_entry['allow_comments'] = allow_comments
      # Saving the entry again.
      post_entry = models.JoggerEntry(**post_entry)
      jogger_panel.SaveEntry(post_entry)


if __name__ == '__main__':
  main()
