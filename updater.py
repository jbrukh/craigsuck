#!/usr/bin/python

"""
craigsuck, a Craigslist RSS poller.
Copyright (c) 2011. Jake Brukhman <jbrukh@gmail.com>. See LICENSE. 
"""

import craigslist
import optparse
import time

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

def main(queries, opts):
    """
    Indefinitely cycles through the queries provided to the program,
    and extracts the new apartment information.
    """
    queue = LookupQueue(opts.memory)
    while True:
        for query in queries:
            new_listings = update(queries, queue)
            for listing in new_listings:
                print opts.format % listing
            process_new(new_listings)
        time.sleep(opts.sleep)

def process_new(listings):
    pass

def update(queries, queue):
    """
    Fetches the listings and returns the new ones, if any.
    """
    listings = craigslist.fetch_all(queries)
    return [l for l in listings if queue.push(l['link'])]   

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-m', '--memory', dest='memory', type='int', default=1000,
            help='number of historical items against which to test for uniqueness (set high)')
    parser.add_option('-s', '--sleep', dest='sleep', type='int', default=30, 
            help='polling period, in seconds')
    parser.add_option('-f', '--format', dest='format', default='%(date)s\t%(title)s', type='string',
            help="output format, using Python formatting; available fields are ['date', 'title', 'link'] and \
			the default format is '%(date)s\\t%(title)s'") 
    opts, args = parser.parse_args()
    
    try:
        main(args, opts)
    except KeyboardInterrupt:
        print "Goodbye!"
