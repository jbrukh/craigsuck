## craigsuck: A Craigslist RSS poller.

Copyright (c) 2010 Jake Brukhman. (`jbrukh@gmail.com`)

Periodically checks a Craigslist RSS feed for listings and pipes them to output.  See the legacy `craigslist-mailer` tags (`1.0.x`) for e-mail functionality.

## Installation

* `craigsuck` depends on `BeautifulSoup`. See [this page](http://stackoverflow.com/questions/452283/how-can-i-install-the-beautiful-soup-module-on-the-mac) for Mac instructions.

## Motivation

Sometimes one desires to keep abreast of craigslist postings in real-time. One application is apartment listings in large cities, such as New York, where reading a listing early might confer a particular advantage on the apartment seeker. Real-time postings can also be filtered and the user notified of certain goings-on of interest -- such as Missed Connections posts that mention a "green scarf".

To aid in this process, `craigsuck` provides a commandline way of keeping track of incoming listings in perpetuity. It polls the craigslist RSS feed for a particular page and sends you the new additions every polling period.

# Usage

Navigate to the Craigslist page you'd like to keep an eye on and copy the URL.  Examples:

* http://newyork.craigslist.org/rnr/
* http://sfbay.craigslist.org/search/apa/sby?query=&srchType=A&minAsk=&maxAsk=&bedrooms=&addTwo=purrr

Give a list of URLS to `craigsuck`, for instance:

    ./craigsuck "http://newyork.craigslist.org/brk/aap/"

To change the output format, you can specify it using the `--format` option. Format is given in Python style, with `link`, `title`, or `date` as possible parameters.

    ./craigsuck --format "%(date)s - %(title)s" "http://newyork.craigslist.org/brk/aap/"

See `--help` for details.