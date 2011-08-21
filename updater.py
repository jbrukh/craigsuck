#!/usr/bin/python

"""
craigsuck, a Craigslist RSS poller.
Copyright (c) 2011. Jake Brukhman <jbrukh@gmail.com>. See LICENSE. 
"""

import craigslist
import optparse
import time
from string import Template

class LookupQueue(object):
    """
    A bounded queue backed by a set for fast
    membership lookup and which does not accept
    duplicate elements.
    """

    def __init__(self, size):
        self.s = set()
        self.q = []
        self.size = size
    
    def push(self, *items):
        for item in items:
            if item not in self.s:
                if len(self.q) == self.size:
                    self.pop()
                self.s.add(item)
                self.q.append(item)
                return item
        
    def pop(self):
        item = self.q.pop(0)
        self.s.remove(item)
        return item
        
    def __contains__(self, item):
        return item in self.s
    
    def __len__(self):
        return len(self.q)
        
    def __str__(self):
        return self.q.__str__()

    def __repr__(self):
        return self.q.__str__()

def main(query, opts):
    """
    Indefinitely cycles through the queries provided to the program,
    and extracts the new apartment information.
    """
    queue = LookupQueue(opts.memory)
    while True:
        listings = craigslist.fetch_with_pages_back(query, pages=opts.pages)
        new_listings = [l for l in listings if queue.push(l['link'])]
        for listing in new_listings:
            print Template(opts.format).safe_substitute(listing)
        process_new(new_listings)
        time.sleep(opts.sleep)

def process_new(listings):
    pass


if __name__ == '__main__':
    USAGE = '%prog [options] <url>'
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-m', '--memory', dest='memory', type='int', default=1000,
            help='number of historical items against which to test for uniqueness (set high)')
    parser.add_option('-s', '--sleep', dest='sleep', type='int', default=30, 
            help='polling period, in seconds')
    parser.add_option('-f', '--format', dest='format', default='${date}\t${title}', type='string',
            help="output format, using Python formatting; available fields are ['date', 'title', 'link'] and \
			the default format is '${date}\\t${title}'")
    parser.add_option('-p', '--pages', dest='pages', default=1, type='int',
            help="the number of pages back from this url, if possible")
    opts, args = parser.parse_args()
    
    try:
        main(args[0], opts)
    except KeyboardInterrupt:
        print "Goodbye!"
