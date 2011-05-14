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
        save_cache(set())
    file = open(CACHE_FILE,'r')
    urls = pickle.load(file)
    file.close()
    return urls

def save_cache( urls ):
    """Cache an object."""
    file = open(CACHE_FILE,'w')
    pickle.dump(urls, file)
    file.close()

def main(opts):
    if not opts.query:
        opts.query = [""]
    while True:
        for query in opts.query:
            try:
                listings = update(url=opts.url, query=query, minAsk=opts.minAsk,maxAsk=opts.maxAsk, 
						bedrooms=opts.bedrooms, srchType=opts.srchType, catAbb=opts.catAbb, s=opt.s)
            except Exception, err:
                print "Error", err
		sleep_time = random.randint(60,60*5)
		print "Sleeping %d seconds..." % sleep_time
		time.sleep(sleep_time)



def update(**kwargs):
	"""
	Given the particular craigslist arguments in kwargs, retrieve
	new listings that haven't yet been cached and return them. 
	"""
	visited = load_cache()
	new_listings = []
	listings = craigslist.listings(**kwargs)
	for listing in listings:
		link = listing['link']
		if link not in visited:
			print listing['title']
			new_listings.append(listing)
			visited.add(link)
	save_cache(visited)	
	return new_listings

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-u', '--url', action='store', dest='url', help='the search url (default: http://newyork.craigslist.org/search/aap/brk)',
                            default='http://newyork.craigslist.org/search/aap/brk')
	parser.add_option('-q', '--query', action='append', help='search query (may be repeated)')
	parser.add_option('-m', '--min-ask', action='store', dest='minAsk', help='minimum asking price', type="int", default=1)
	parser.add_option('-M', '--max-ask', action='store', dest='maxAsk', help='maximum asking price', type="int")
	parser.add_option('-b', '--bedrooms', action='store', dest='bedrooms', help='number of bedrooms', type="int")
	cats = " | ".join([" ~ ".join(map(str,item)) for item in craigslist.categories.items()])
	parser.add_option('-c', '--category', action='store', dest='catAbb', help="TYPES: "+cats, default='aap') 
	parser.add_option('-t', '--search-title-only', action='store_true', dest='titleOnly', help='search title only (as opposed to whole post)', default=False)
	opts,_ = parser.parse_args()
	try:
		main(opts)
	except KeyboardInterrupt:
		print "Goodbye!"
