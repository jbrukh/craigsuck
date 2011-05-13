'''
Created on Jun 26, 2010

@author: jbrukh

Craigslist Mailer
Copyright (c) 2010-2011 Jake Brukhman
LICENSE: Public domain.

Periodically checks a Craigslist RSS feed for new listings and e-mails
them to a recipient. Set all configuration in conf.py. See README.
'''

import optparse
import conf
import sys
import random
import time

from BeautifulSoup import BeautifulStoneSoup

def main(opts):

	if not opts.query:
		opts.query = [""]

	# infinite loop...
	while True:
		for query in opts.query:
			try:
				retrieve(opts.url, query, opts.min_ask, opts.max_ask, opts.bedrooms)
			except Error, err:
				print "Error", err
		sleep_randomly()

def retrieve(url, query, min_ask, max_ask, bedrooms):
	# at least one argument needs to be non-trivial for RSS to be returned;
	# this is ensured by default min_ask
	full_url = "%s?format=rss&query=%s&minAsk=%d&maxAsk=%d&bedrooms=%d" %\
                (url, query.replace(' ','+'), min_ask, max_ask, bedrooms)
	print "Retrieving", full_url

	# parse the page
	page = BeautifulStoneSoup(urllib2.urlopen(full_url))
	items = [(item('dc:date')[0].string, strip_cdata(item.title.string), item.link.string) for item in page('item')]

	new_listings = []
    for item in items:
        title = ("%s %s" % (item[0], item[1])).encode("ascii","ignore")
        if not title in titles:
            print title
            new_listings.append(item)
            titles.add(title)

    # store the new listings from this round
    LISTINGS[query] += new_listings

    if len(LISTINGS[query])>=conf.BATCH_SIZE:
        # send the e-mail
        msg = get_msg(LISTINGS[query], query)
        try:
            send_email(conf.SENDER, conf.RECIPIENTS.split(';'), msg)
            LISTINGS[query]=[]
        except:
            print "Could not send email: ", sys.exc_info()[0]
    else:
        print "Not enough new listings. (%d, while BATCH_SIZE is %d.)"\
                    % (len(LISTINGS[query]), conf.BATCH_SIZE)

    # persist
    if len(titles)>conf.CACHE_SIZE:
        # keep the cache at conf.CACHE_SIZE
        # you want to keep this number relatively large: if the cache is too small
        # the application will forget that it has already seen certain recent listings
        # and will e-mail them again
        titles = set(list(titles)[1:conf.CACHE_SIZE])
    cache(titles)

def sleep_randomly():
    """Sleep for 1-5 minutes."""
    sleep_time = random.randint(60,60*5)
    print "Sleeping %d seconds before next retrieve..." % sleep_time
    time.sleep(sleep_time)

def assert_conf():
    """Make sure configuration variables are set."""
    try:
        conf.SMTP_USER
        conf.SMTP_PASS
        conf.SMTP_SERVER
        conf.RECIPIENTS
        conf.BATCH_SIZE
        conf.CACHE_FILE
        conf.CACHE_SIZE
    except AttributeError, err:
		print "Missing configuration:", err
		sys.exit(2)

if __name__=='__main__':
	# parse the program arguments
	parser = optparse.OptionParser()
	parser.add_option('-q', '--query', action='append', help='search query (may be repeated)')
	parser.add_option('-m', '--min-ask', action='store', dest='min_ask', help='minimum asking price', type="int", default=1)
	parser.add_option('-M', '--max-ask', action='store', dest='max_ask', help='maximum asking price', type="int")
	parser.add_option('-b', '--bedrooms', action='store', dest='bedrooms', help='number of bedrooms', type="int")
	parser.add_option('-u', '--url', action='store', dest='url', help='the search url (e.g. http://newyork.craigslist.org/search/aap/brk)', 
							default='http://newyork.craigslist.org/search/aap/brk')
	parser.add_option('-s', '--batch-size', action='store', dest='batch_size', help='override the batch size (should be >= 1)', type="int")

	# make sure the configuration is in place
	assert_conf()
	
	# go!
	opts,_ = parser.parse_args()
	try:
		main(opts)
	except KeyboardError:
		print "Goodbye."
