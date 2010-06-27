'''
Created on Jun 26, 2010

@author: jbrukh
'''

#
# SET THE SMTP CREDENTIALS
#
SMTP_USER   ='username'    # these defaults seem to work on gmail
SMTP_PASS   ='password'    # haha
SERVER      ='smtp.gmail.com'

#
# SET THE RECIPIENT
#
RECIPIENT   ='you@poop.com'

#
# SET THE BASE CRAIGSLIST URL TO SCRAPE
#
CRAIGS_URL  ="http://newyork.craigslist.org/search/aap/brk"  # search Brooklyn

#
# OTHER VARIABLES
#
CACHE_FILE  ='titles.cache'     # title of the cache file
CACHE_SIZE  =1000               # maximum size of the cache
SENDER='poop@poop.com'          # the e-mail sender (may not work with all SMTP providers e.g. gmail)
