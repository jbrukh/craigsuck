import craigslist

for listing in craigslist.listings('http://newyork.craigslist.org/search/aap/brk'):
	print listing
