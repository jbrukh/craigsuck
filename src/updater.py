import craigslist
import os.path
import pickle
import optparse
import random
import time

CACHE_FILE = 'urls.cache'

def load_cache():
    """Load the cache."""
    # check whether the file exists
    if not os.path.exists(CACHE_FILE):
        return set()
    fp = open(CACHE_FILE,'r')
    urls = pickle.load(fp)
    fp.close()
    return urls

def save_cache( urls ):
    """Cache an object."""
    fp = open(CACHE_FILE,'w')
    pickle.dump(urls, fp)
    fp.close()

def main(queries):
    while True:
        print "Updating..."
        for query in queries:
            listings = update(queries)
            for listing in listings:
                print listing 
        time.sleep(10)

def update(queries):
    """
    Given the particular craigslist arguments in kwargs, retrieve
    new listings that haven't yet been cached and return them.
    """
    visited = load_cache()

    new_listings = []
    listings = craigslist.fetch_all(queries)
    for listing in listings:
        link = listing['link']
        if link not in visited:
            new_listings.append(listing)
            visited.add(link)
   # save_cache(visited)
    return new_listings

if __name__ == '__main__':
    parser = optparse.OptionParser()
    _,args = parser.parse_args()
    
    try:
        main(args)
    except KeyboardInterrupt:
        print "Goodbye!"
