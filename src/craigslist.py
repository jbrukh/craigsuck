"""
Craigslist Apartments Scraper.
Copyright (c) 2011. Jake Brukhman <jbrukh@gmail.com>.

Please see LICENSE, README.
"""

from BeautifulSoup import BeautifulStoneSoup
import urllib2
import re

categories = { 	'aap': 'all apartments',
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

def listings(url, query='', srchType='A', bedrooms='', minAsk='1', maxAsk='', catAbb='aap', s=0):
	"""
	Scrapes the craigslist apartment search page and returns the listings from
	that page.  Listings are composed of date, title, and url.

        url			the search url, usually something like the following whence
					parameters are attached.
				
						http://newyork.craigslist.org/search/aap/brk

		query		the searh string
		srchType	either 'T' or 'A', as above
		minAsk		number, minimum asking price
		maxAsk		number, maximum asking price
		bedrooms	number, of bedrooms
		catAbb		as categories map above
		s			page offset, starts at the s-th listing
	
	This function may throw various kinds of Errors:

		* if it cannot open the url
		* if it cannot parse the data received

	"""

	# prepare the url
	full_url = "%s?format=rss&query=%s&catAbb=%s&srchType=%s&minAsk=%s&maxAsk=%s&bedrooms=%s&s=%s" %\
				(url.rstrip('/'), '+'.join(query.split(' ')), catAbb, srchType, minAsk, maxAsk, bedrooms, s)
	fetch(full_url)

def fetch(full_url):
	print full_url
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

