import urllib2
from bs4 import BeautifulSoup
import time
import csv
import re
import funcs
import sys

################################################################################
# Collects Kelly Blue Book pricing information on popular year, make and models
# of motorcycles, formatting into a file that can be queried by the craigslist.py
# script in evaluating bike prices. 
################################################################################



# notes
#   - 12 min to go through 98-07 honda cruiser ~ 110
#   - on craigslist one is more likely to put the cc that is associated with the name
#     i.e. 800 for a "VS800GL Intruder 800" instead of kbb actual CC of 805cc
# bugs
#   - skipping last model in every year 

start_year = 1980
end_year = 2012
file_name = 'mortocycles.csv'

f = open(file_name, 'wb')
writer = csv.writer(f)
writer.writerow(['make']+[',year']+[',model']+[',cc (size)']+[',trade-in value']+[',suggested retail value']) 
make = ['honda', 'bmw', 'harley-davidson'] #'yamaha', 'kawasaki', 'suzuki', 

for m in make:
        http='http://www.kbb.com/motorcycles/street-standard--cruiser/%s/'%m   # inside make page
        request = urllib2.urlopen(http)
        html = request.read()
        soup=BeautifulSoup(html)

        for year in range(start_year, end_year):
                print'               %d'%(year)
                try:
                  http = "http://www.kbb.com/motorcycles/%s/%d/?categoryname=streetstandardcruiser"%(m,year)   # inside year page
                  request = urllib2.urlopen(http)
                  html = request.read()
                  Ysoup = BeautifulSoup(html)
          # inside each year must determine how many models there are and go into each


                  modelList = Ysoup.findAll('div', 'grid-4 alpha with-text')
                  CClist = Ysoup.findAll('div', 'grid-2 omega with-text')
                  numModels = len(modelList)      # from 1 to numModels
                  for model in range(1,(numModels)):   # move past first item, always junk
                          price_found = 1
                          trade_in_value = -1
                          retail_value = -1
                          try:                    # if not in space holder for next line and not a bike
                                  name = str(modelList[model].contents[1].contents[0])            
                          except:
                                  continue
 
                          args = name.split()
                          numArgs = len(args)
                          modelName = ""
                          first_type = ""
                          for a in range(0,numArgs):
                                  if(a == numArgs-1):
                                          first_type += args[a]
                                  else:
                                          first_type += args[a] + "-"
                                        
                          second_type = str(year) + "-" + m + '-' + first_type   # 2007-honda-cb250-nighthawk-250
                          print(first_type)
 
                                  # get CC
                          CC = -1
                          CC = funcs.getCC(first_type)
                          if(CC == 'error: no size found'):
                            try:
                              CC = int(CClist[model].contents[0])          # if no apparent CC use actual kbb
                            except:
                              CC = "enter manually"
                      
                                  # get prices
                          try:
                            http = modelList[model].a['href']
                          except:
                            price_found = 0
                            writer.writerow([m,year,name, CC, -1, -1])
                            print("enter manually")
                            continue
                          if(http == '#'):
                            price_found = 0
                            writer.writerow([m,year,name, CC, 'N/A', 'N/A'])
                        
                        
                          if(price_found == 1):
                            request = urllib2.urlopen(http)
                            html = request.read()
                            valsoup = BeautifulSoup(html)
                            pricepages = valsoup.findAll('a', 'btn-cta-a with-box')
                            try:
                               request = urllib2.urlopen(pricepages[0]['href'])
                               html = request.read()
                               valsoup = BeautifulSoup(html)
                               var = valsoup.findAll('span', 'color-g')
                               tradeIn_value = int(funcs.addNuminString(var[0].contents[0].contents[0]))


                               request = urllib2.urlopen(pricepages[1]['href'])
                               html = request.read()
                               valsoup = BeautifulSoup(html)
                               var = valsoup.findAll('span', 'color-g')
                               retail_value = int(funcs.addNuminString(var[0].contents[0].contents[0]))

                               writer.writerow([m,year,name, CC, tradeIn_value, retail_value])
                            except:
                               pass
                except:
                  continue

f.close()
