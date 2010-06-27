'''
Created on Jun 26, 2010

@author: jbrukh
'''

from BeautifulSoup import BeautifulStoneSoup
import urllib2

def scrape( url ):
    """Retrieves the Craigslist page as XML in a BeautifulStoneSoup object."""
    page = urllib2.urlopen(url)
    return BeautifulStoneSoup(page)

def extract( soup ):
    """Retrieves the titles and links of listings from the scrape as tuples."""
    return [(strip_cdata(item.title.string), item.link.string) for item in soup('item')]

def strip_cdata( item ):
    """Removes ugly CDATA tags."""
    return str(item).replace('<![CDATA[','').replace(']]>','')

def build_url( base_url, query="", min_ask="", max_ask="", bedrooms="" ):
    # at least one of the parameters must be non-trivial,
    # or else the url will not produce RSS
    if not min_ask:
        min_ask = "1"  # ensures RSS is delivered
    
    # checks
    if query:
        query = query.replace(' ', '+')
    if min_ask:
        int(min_ask)  # raises ValueError if not integer
    if max_ask:
        int(max_ask)  # same
    if bedrooms:
        int(bedrooms) # same
    
    return "%s?format=rss&query=%s&minAsk=%s&maxAsk=%s&bedrooms=%s" %\
                ( base_url, query, str(min_ask), str(max_ask), str(bedrooms) )