from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import time
import csv
import re
import funcs

#   TO DO
# -if no CC assume lowest that matches keys
# -go older?  CHECK 1980 -> 2012
# -know when at end and go to next 100 if more   CHECK
# - harley often do not match CC
# - 

newerThan = 1990
olderThan = 2009
max_posts = 15
max_keys = 0
keyCount = 3
lessThanTrade = False
lessThanRetail = False
linksArray = ['','','','','','','','']
checkMoreThanFirst100 = True

searchTerms=['vulcan', 'shadow']  #'v-star', 
for term in searchTerms:
    print('\r\n')
    print(term)
    print('\r\n')

    http='http://sandiego.craigslist.org/search/mca?zoomToPosting=&altView=&query=%s&srchType=A&minAsk=2000&maxAsk=9999'%term
    request = urllib2.urlopen(http)
    html = request.read()
    soup=BeautifulSoup(html)
    post = soup.findAll('p')
    count = 0
    keyCount = keyCount + 1
    if(keyCount > max_posts):
        break           

    for x in post:
        try:
            loc = str(x.findAll('small')[1].contents[0])        # could be absent
        except:
            pass
        date = str(x.find('span', attrs={'class':'date'}).contents[0])
        price = int(str(x.find('span', attrs={'class':'price'}).contents[0])[1:])
        http = 'http://sandiego.craigslist.org'+ str(x.a['href'])
        request = urllib2.urlopen(http)
        html = request.read()
        Psoup=BeautifulSoup(html)
        title = str(Psoup.title)[7:][:-8]
        d = Psoup.find('section', attrs={'id':'postingbody'})
        d = d.__str__
        desc = d()

 
        year = funcs.getYear(title, desc)           # first check title, then descript for year
        CC = funcs.getCC(title, desc) 
        make = funcs.getMake(title, desc)
        keywords = funcs.getKeywords(make, title, desc)
        mileage = funcs.getMileage(desc)

        if((year < newerThan) or (year > olderThan)):      # range of years wanted 
            continue
        if(make == 'no make' or CC == 'no CC' or year =='no year'): 
            print('make:%s  , CC:%s  , year:%s  ,miles:%s  ,keys:%s'%(make, str(CC), str(year), str(mileage), keywords))  
            continue
          
        d = funcs.getKBB(make, year, keywords, CC)
        if((d['bn'] == 'make not found') or (d['bn'] == 'none')):                    # getKBB unsuccessful 
            print'%s,   %s'%(title, d)
            print('\r\n')
            continue

        percentOfRetail = price / int(d['rp'])        
        print' %d %s %s,  %d, %d    %s'%(year, make, title, CC, mileage, loc)
        print '       %s,  $%d__ trade:%s, retail:%s        %s'%(d['bn'], price, d['tp'], d['rp'], str(percentOfRetail))
        print(http)
        if(price < int(d['tp'])):
            lessThanTrade = True
            print'************amazing deal****  %s  %s'%(str(price), int(d['tp']))
        if(price < int(d['rp'])):
            lessThanRetail = True
            print('************fair deal**** %s  %s'%(str(price), int(d['rp'])))
        print('\r\n')

        count = count + 1
        if(count > max_posts):
            break


        # if more than one page of links
    if(checkMoreThanFirst100 == True):
        pageLinks = soup.find('span', attrs={'class':'pagelinks'})
        if(str(pageLinks) != 'None'):  # check for changing numbers
            numPages = int((len(pageLinks)-1)/2 -1)             # create array of links
            continue                # go to next key
            for page in range(0, numPages):          # starts at contents[3] and continues to 3+2*(numPages-1)
                 linksArray[page] = str(pageLinks.contents[3+2*page]['href'])
                    
            for link in linksArray:
                request = urllib2.urlopen(link)
                html = request.read()
                soup=BeautifulSoup(html)
                post = soup.findAll('p')          

                for x in post:
                    loc = str(post[2].findAll('small')[1].contents[0])
                    date = str(x.find('span', attrs={'class':'date'}).contents[0])
                    price = int(str(x.find('span', attrs={'class':'price'}).contents[0])[1:])
                    http = 'http://sandiego.craigslist.org'+ str(x.a['href'])
                    request = urllib2.urlopen(http)
                    html = request.read()
                    Psoup=BeautifulSoup(html)
                    title = str(Psoup.title)[7:][:-8]
                    d = Psoup.find('section', attrs={'id':'postingbody'})
                    d = d.__str__
                    desc = d()
             
                   
                    year = -1     # first check title, then descript for year
                    if (funcs.getYear(title) == 'error: no year found'):
                      if(funcs.getYear(desc) == 'error: no year found'):
                        year = -1
                      else:
                        year = funcs.getYear(desc)
                    else:
                      year = funcs.getYear(title)

                    if((year < 1990) or (year > 2009)):      # don't have data for old or new models
                        continue

                    CC = -1    # first check title, then descript for engine size
                    if (funcs.getCC(title) == 'error: no size found'):
                      if(funcs.getCC(desc) == 'error: no size found'):
                        CC = -1
                      else:
                        CC = funcs.getCC(desc)
                    else:
                      CC = funcs.getCC(title)

                    make = "none"    # first check title, then descript for make
                    if (funcs.getMake(title) == 'no make found'):
                      if(funcs.getMake(desc) == 'no make found'):
                        make = "none"
                      else:
                        make = funcs.getMake(desc)
                    else:
                      make = funcs.getMake(title)          
                    mileage = funcs.getMileage(desc)
                    keywords = funcs.getKeywords(make, title, desc)
                    d = funcs.getKBB(make, year, keywords, CC)
                    if((d['bn'] == 'make not found') or (d['bn'] == 'none')):                    # getKBB unsuccessful 
                        print 
                        continue

                    percentOfRetail = price / int(d['rp'])
                    
                    print' %d %s %s,  %d, %d    %s'%(year, make, title, CC, mileage, loc)
                    print '       %s,  $%d__ trade:%s, retail:%s        %s'%(d['bn'], price, d['tp'], d['rp'], str(percentOfRetail))

                    if(price < int(d['tp'])):
                        lessThanTrade = True
                        print'************amazing deal****  %s  %s'%(str(price), int(d['tp']))
                    if(price < int(d['rp'])):
                        lessThanRetail = True
                        print('************fair deal**** %s  %s'%(str(price), int(d['rp'])))

