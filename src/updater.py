import craigslist
import os.path
import pickle
import optparse
import random
import time

CACHE_FILE = 'urls.cache'

def main(queries):
	visited = set()
    while True:
        print "Updating..."
        for query in queries:
            listings = update(queries, visited)
            for listing in listings:
                print listing 
        time.sleep(10)

def update(queries, visited):
    new_listings = []
    listings = craigslist.fetch_all(queries)
    for listing in listings:
        link = listing['link']
        if link not in visited:
            new_listings.append(listing)
            visited.add(link)
    return new_listings

if __name__ == '__main__':
    parser = optparse.OptionParser()
    _,args = parser.parse_args()
    
    try:
        main(args)
    except KeyboardInterrupt:
        print "Goodbye!"
