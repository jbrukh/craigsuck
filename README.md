## craigsuck
### A Craigslist RSS poller.

Copyright (c) 2010 Jake Brukhman

Periodically checks a Craigslist RSS feed for listings. The goal is to then send an e-mail
containing the listings to interested party, though this feature is unimplemented in this
version.  See the legacy `craigslist-mailer` tags (`1.0.x`) for e-mail functionality.

INSTALLATION

* `craigsuck` depends on `BeautifulSoup`. See [this page][http://stackoverflow.com/questions/452283/how-can-i-install-the-beautiful-soup-module-on-the-mac] for Mac instructions.

USAGE

Navigate to the Craigslist page you'd like to keep an eye on and copy the URL.  Examples:

* http://newyork.craigslist.org/rnr/
* http://sfbay.craigslist.org/search/apa/sby?query=&srchType=A&minAsk=&maxAsk=&bedrooms=&addTwo=purrr

Give a list of URLS to `craigsuck`.