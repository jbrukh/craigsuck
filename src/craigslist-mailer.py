'''
Created on Jun 26, 2010

@author: jbrukh

Craigslist Mailer
Copyright (c) 2010-2011 Jake Brukhman
LICENSE: Public domain.

Periodically checks a Craigslist RSS feed for new listings and e-mails
them to a recipient. Set all configuration in conf.py. See README.
'''

import sys
import random
import time
import os.path
import pickle
import conf
import getopt
import urllib2
import smtplib
from BeautifulSoup import BeautifulStoneSoup
from collections import defaultdict

QUERIES=[]
MIN_ASK=""
MAX_ASK=""
BEDROOMS=""
LISTINGS=defaultdict(list)

def main():
    """The main loop."""
    while True:
        if len(QUERIES)==0:
            retrieve_listings("",MIN_ASK,MAX_ASK,BEDROOMS)
        else:
            for query in QUERIES:
                retrieve_listings(query,MIN_ASK,MAX_ASK,BEDROOMS)
        sleep_randomly()

def retrieve_listings(query, min_ask, max_ask, bedrooms):
    """Retrieve the listings and e-mail them."""
    global LISTINGS

    try:
        titles = load_cache()
    except IOError, errstr:
        print "Could not retrieve cache: ", errstr

    try:
        url = build_url(conf.CRAIGS_URL, query, min_ask, max_ask, bedrooms)
        print url
        items = extract(scrape(url))
    except AttributeError:
        # one of CRAIGS_URL or --url must be set!
        print "Set the CRAIGS_URL variable or specify --url."
        sys.exit(2)
    except:
        print "Could not retrieve listings:", sys.exc_info()[0]
        return
    
    new_listings = []
    for item in items:
        title = ("%s %s" % (item[0], item[1])).encode("ascii","ignore")
        if not title in titles:
            print title
            new_listings.append(item)
            titles.add(title)

    # store the new listings from this round
    LISTINGS[query] += new_listings
     
    if len(LISTINGS[query])>=conf.BATCH_SIZE:
        # send the e-mail
        msg = get_msg(LISTINGS[query], query)
        try:
            send_email(conf.SENDER, conf.RECIPIENTS.split(';'), msg)
            LISTINGS[query]=[]
        except:
            print "Could not send email: ", sys.exc_info()[0]
    else:
        print "Not enough new listings. (%d, while BATCH_SIZE is %d.)"\
                    % (len(LISTINGS[query]), conf.BATCH_SIZE)
    
    # persist
    if len(titles)>conf.CACHE_SIZE:
        # keep the cache at conf.CACHE_SIZE
        # you want to keep this number relatively large: if the cache is too small
        # the application will forget that it has already seen certain recent listings
        # and will e-mail them again
        titles = set(list(titles)[1:conf.CACHE_SIZE])
    cache(titles)

def get_msg( new_listings, query ):
    """Create the listing summary email."""
    subject = "Apartments -- %d for Query: %s" % (len(new_listings), query)
    header = "From: %s\nTo: %s\nSubject: %s\n\n" % (conf.SENDER, conf.RECIPIENTS, subject)
    body = header+"\n\n".join(["%s %s\n%s"%(item) for item in new_listings])  
    return body    
    
def load_cache():
    """Load the titles cache."""
    # check whether the file exists
    if not os.path.exists(conf.CACHE_FILE):     
        cache(set())
    
    file = open(conf.CACHE_FILE,'r')
    titles = pickle.load(file)
    file.close()
    
    return titles
            
def cache( titles ):
    """Cache a bunch of titles."""
    file = open(conf.CACHE_FILE,'w')
    pickle.dump(titles,file)
    file.close()

def sleep_randomly():
    """Sleep for 1-5 minutes."""
    sleep_time = random.randint(60,60*5)
    print "Sleeping %d seconds before next retrieve..." % sleep_time
    time.sleep(sleep_time)
    
def scrape( url ):
    """Retrieves the Craigslist page as XML in a BeautifulStoneSoup object."""
    page = urllib2.urlopen(url)
    return BeautifulStoneSoup(page)

def extract( soup ):
    """Retrieves the titles and links of listings from the scrape as tuples."""
    return [(item('dc:date')[0].string, strip_cdata(item.title.string), item.link.string) for item in soup('item')]

def strip_cdata( item ):
    """Removes ugly CDATA tags."""
    return item.encode('ascii', 'ignore').replace('<![CDATA[','').replace(']]>','')

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

def send_email( sender, recipients, msg ):
    """Send an email."""
    session = smtplib.SMTP(conf.SMTP_SERVER)
    session.starttls()
    session.login(conf.SMTP_USER, conf.SMTP_PASS)
    smtpresult = session.sendmail(sender, recipients, msg)
  
    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = """Could not delivery mail to: %s
  
  Server said: %s
  %s
  
  %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
        raise smtplib.SMTPException, errstr
    
def usage():
    """Usage."""
    print """
        Craigslist Mailer.  Copyright (c) 2010 Jake Brukhman.
        
        python craigslist-mailer.py
        
            [-q,--queries <STRING,STRING,...>]   -- search queries
            [-m,--minAsk <INTEGER>]              -- minimum price
            [-M,--maxAsk <INTEGER>]              -- maximum price
            [-b,--bedrooms <INTEGER>]            -- number of bedrooms
                
            [-u,--url <STRING>]                  -- override the url
            [-s,--batch-size <INTEGER>]          -- override the batch size (should be >= 1)
    """

def get_args():
    global QUERIES, MIN_ASK, MAX_ASK, BEDROOMS
    """Get the commandline arguments."""
    opts,args = getopt.getopt(sys.argv[1:],\
            "q:m:M:b:u:s:h", ['help', 'query=', 'minAsk=', 'maxAsk=', 'bedrooms=', 'url=', 'batch-size='])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        if opt in ('-q', '--queries'):
            QUERIES=arg.split(',')
        if opt in ('-m', '--minAsk'):
            MIN_ASK=str(int(arg)) # checks for integer
        if opt in ('-M', '--maxAsk'):
            MAX_ASK=str(int(arg))
        if opt in ('-b', '--bedrooms'):
            BEDROOMS=str(int(arg))
        if opt in ('-u', '--url'):
            conf.CRAIGS_URL=arg
        if opt in ('-s'  '--batch-size'):
            arg = int(arg)          # raises ValueError if not integer
            if arg<1:               # BATCH_SIZE must be >= 1
                raise ValueError
            conf.BATCH_SIZE=arg

def check_conf():
    """Make sure configuration variables are set."""
    # check SMTP credentials
    try:
        conf.SMTP_USER
        conf.SMTP_PASS
        conf.SMTP_SERVER
    except AttributeError:
        print "SMTP credentials are missing."
        sys.exit(2)
    
    try:
        conf.RECIPIENTS
    except AttributeError:
        print "RECIPIENTS variable is missing."
        sys.exit(2)
        
    try:
        conf.BATCH_SIZE
        conf.CACHE_FILE
        conf.CACHE_SIZE
    except AttributeError:
        print "One of mandatory variables BATCH_SIZE, CACHE_SIZE, or CACHE_FILE is missing."
        sys.exit(2)

#        
#
#
if __name__=='__main__':
    try:
        # get the configuration
        check_conf()
        # check and read the options
        get_args();
        # go...
        main()
    except ValueError, strerror:
        print "Error: ", strerror
        usage()
    except getopt.GetoptError:
        usage()
    except KeyboardInterrupt:
        print "Goodbye."
        sys.exit(0)
    sys.exit(2)
