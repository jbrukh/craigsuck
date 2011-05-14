import craigslist

CACHE_FILE = 'listings.cache'

def load_cache():
    """Load the titles cache."""
    # check whether the file exists
    if not os.path.exists(CACHE_FILE):
        cache(set())

    file = open(CACHE_FILE,'r')
    titles = pickle.load(file)
    file.close()

    return titles

def save_cache( titles ):
    """Cache a bunch of listings."""
    file = open(CACHE_FILE,'w')
    pickle.dump(titles, file)
    file.close()

def update():
	try:
        titles = load_cache()
    except IOError, errstr:
        print "Could not retrieve cache: ", errstr
	
	new_listings = [listing[1] for listing in craigslist.
