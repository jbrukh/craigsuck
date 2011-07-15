Craigslist Apartment Scraper
============================

Copyright (c) 2010 Jake Brukhman

Periodically checks a Craigslist RSS feed for new apartment listings and e-mails


INSTALLATION

* Install `BeautifulSoup`. See [this page][http://stackoverflow.com/questions/452283/how-can-i-install-the-beautiful-soup-module-on-the-mac] for Mac instructions.
* Run:

   `updater.py --help`

USAGE

Find your favorite craigslist apartments URL, and set the CRAIGS_URL variable in conf.py.  For instance,
to search for "all apartments in Brooklyn", find the Craigslist 3-letter code for Brooklyn: "brk".  Set
the url to:

  http://newyork.craigslist.org/search/aap/brk

You can also set "abo" for "apartments by owner" and other Craigslist codes.  To run the script:

  $ python craigslist-mailer.py --query "williamsburg" --maxAsk 3000

will find all Williamsburg apartments with a maximum price of $3000.  You can search for multiple
neighborhoods simultaneously by separating them with a comma:

  $ python craigslist-mailer.py --query "williamsburg,park slope,clinton hill" --maxAsk 3000 --bedrooms 2

And so forth.  See --help for further usage.
