"""
Craigslist Apartments Scraper.
Copyright (c) 2011. Jake Brukhman <jbrukh@gmail.com>.

Please see LICENSE, README.
"""

from BeautifulSoup import BeautifulStoneSoup
import urllib2
import re

categories = {  'aap': 'all apartments',
                'nfa': 'all no fee apts',
                'fee': 'apts broker fee',
                'nfb': 'apts broker no fee',
                'abo': 'apts by owner',
                'aiv': 'apts registration fee',
                'hou': 'apts wanted',
                'swp': 'housing swap',
                'hsw': 'housing wanted',
                'off': 'office & commercial',
                'prk': 'parking and storage',
                'reb': 'real estate by broker',
                'reo': 'real estate by owner',
                'rea': 'real estate for sale',
                'rew': 'real estate wanted',
                'roo': 'rooms and shares',
                'sha': 'rooms wanted',
                'sbw': 'sublet/temp wanted',
                'sub': 'sublets & temporary',
                'vac': 'vacation rentals'
            }

searchType = {
                'T':   'titles only',
                'A':   'entire post'
             }

def fetch(full_url):
    if not re.search('format=rss', full_url):
        full_url += '&format=rss'
    page = urllib2.urlopen(full_url)
    
    # massage the pesky Craigslist CDATA tags so that entities are processed; TODO -- find out
    # if it would be better to sanitize entities separately.
    cdataMassage = [(re.compile('<!\[CDATA\[|]]>'), lambda match: '')]
    soup = BeautifulStoneSoup(page, markupMassage=cdataMassage,
                convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    for item in soup('item'):
        yield {
                'date':  item('dc:date')[0].string,
                'title': item.title.string,
                'link':  item.link.string
              }

def fetch_all(queries):
    for query in queries:
        for listing in fetch(query):
               yield listing
