from __future__ import division
import re
import csv

# Can I use regular expressions in keywords e.g. r'xxx'
# redo harley spreadsheet
makesList = ['honda', 'yamaha', 'kawasaki', 'harley', 'davidson', 'Harley-Davidson',  'bmw', 'suzuki', 'indian', ]
makeString = 'honda yamaha kawasaki harley davidson Harley-Davidson bmw suzuki indian'
keywords = dict(honda=[],  yamaha=[], kawasaki=[], harley=[], victory=[]) 
keywords['honda']=['shadow', 'hawk', 'cj', 'vt', 'aero', 'sabre', 'spirit', 'tour', 'vlx', 'deluxe', 'ace', 'sabre', 'saber', 'VT600C', 'VT1100', 'VT750C', 'VT750D']
keywords['yamaha']=['FJ1200', 'VMX12', 'Vmax', 'virago',  'xv', 'yx', 'tdm', 'gts', 'xj', 'xvz', 'royal', 'star', 'vstar', 'v-star', 'v', 'fz', 'classic', 'custom', 'road', 'roadstar', 'boulevard', 'cheyenne', 'silverado', 'midnight', 'roadliner']
keywords['kawasaki']=['en', 'ks', 'vn', 'zr', 'el', 'zl', 'ej', 'bn', 'ltd', 'vulcan', 'police', 'se', 'zephyr', ' hs ', ' l ', 'classic', 'eliminator', 'nomad', 'drifter', ' fi ', 'mean streak', 'anniversary', 'lt'] 
keywords['harley']=['heritage', 'softail', 'soft', 'tail', 'fat boy', 'fatboy', 'low rider', 'lowrider', 'sport', 'glide', 'sturgis', 'super', 'fat', 'bob', 'rider', 'wilde', 'roadster', 'road', 'sportster', 'II', ' 2 ',  'anniversary', 'liberty', 'custom', 'deluxe', 'special', 'hugger'] 
keywords['suzuki']=['intruder', 'marauder', 'gs', 'el', 'em', 'bandit', 'gn', 'ls', 'savage', 'gsf', 'abs', 'gz', 'lc', 'vl', 'sv', 'volusia', 's ', 'anniversary', 'black', 'limited', 'fairing', 'c90', 's83', 's50', 'm50', 'b ', 'edition', 'c50', 'z ', 'c ', 'vl', 'vs']

def month2Int(month):
  if(month == 'Jan'):
      return(1)
  elif(month == 'Feb'):
      return(2)
  elif(month == 'Mar'):
      return(3)
  elif(month == 'Apr'):
      return(4)
  elif(month == 'May'):
      return(5)
  elif(month == 'Jun'):
      return(6)
  elif(month == 'Jul'):
      return(7)
  elif(month == 'Aug'):
      return(8)
  elif(month == 'Sep'):
      return(9)
  elif(month == 'Oct'):
      return(10)
  elif(month == 'Nov'):
      return(11)
  elif(month == 'Dec'):
      return(12)
  else:
      return(month)

 # given year format xx' convert to 4 digit year
 # assume no other 2 digit number will appear in title
def short2fullYear(short):
  if(int(short) <= 15):
    return(int('20' + short))
  elif(int(short) >= 60):
    return(int('19' + short))
  else:
    return('fail')
  
  

  #  craigslist 
def numPosts(soup):
  x = soup.findAll('b')
  try:
        return(int(x[3].contents[0].split()[1]))
  except:
        return('error: Numposts')

      
minCC = 249
maxCC = 1950     # may to conflict with year
minYear = 1960
maxYear = 2015
nonNum = re.compile('\D')
number = re.compile('[0-9]{2,5}')
shortYear = re.compile('[0-9]{2}\'?')     # optional ' i.e. 03' or 04
xxx = re.compile(r'(xxx)')
isWord = re.compile('[a-zA-Z]+')
miles = re.compile(r'[0-9]+?,?[0-9]*\s?k?\s?(?=miles?)|(?<=mileage:)\s+[0-9]+,?[0-9]+|[0-9]+?,?[0-9]+k?(?=\s?original)|[0-9]+,?x*\s?k?\s?(?=miles?)', re.I)
title = " Honda 03\' Shadow Spirit 04 750"
desc = 'This is a great bike to have even if youre just starting out to ride. It has a low seat height which really helps if youre just learning too. I really love it, but I have to sell due to personal reasons. Serious inquiries only. No test rides. <br>This bike has windscreen, back rest, K&N air filter and I also installed a cigarette lighter socket to power my iPhone or other devices on long rides. It has 10k miles on it.<br><br>Cruiser, road bike, touring, cruising'
year_start = 1995
year_end = 2012
price = 2009
desch = '***2007 Honda VT750 Shadow in GREAT CONDITION! ONLY 3400 MILES! Dark Silver. . . $4650. . .READY TO RIDE TODAY!! Rich at 619-929-1047---- Just had a full tune-up! Fully serviced. . .with warranty!!! Financing available! NO CREDIT CHECK!!!...Military Welcome!! !! Financing in San Diego Area only!!. . . ask about our other bikes for sale and financing!!! ..RIDE THIS WEEKEND!!! FREE GEAR FOR MILITARY!! ***Special. . .FREE Delivery within a 20 mile radius!!'
titley = '07 Yamaha V Star (NEED TO SELL! ASAP LOW MILES)'
descy = '2007 Yamaha V Star 650 Just under 2K miles Garage Kept Clean Title In Hand! Vance and Hines Short Shots Exhaust Still My Daily Rider No problems Shaft Drive Motivated Seller $4000 obo  Make me an offer Call or Text at 951=813=6591 kawasaki, vulcan, 250, 600, 650, 900, 883, iron 883, hd, harley, sportster, yamaha, vstar, v-star, honda, shadow'
titlek = '2001 Kawasaki Vulcan vn750'
desck = 'The bike has 22194 miles on it. I have the title (clean) in hand and the bike is registered till 2014.'
titleb = '2011 bmw S 1000 RR Thunder Grey Metallic'
descb = '2011 BMW  S 1000 RR Premium  perfect condition!This 2011 adult owned BMW S 1000 RR is equipped with all the factory installed options which include ABS  Traction Control  and electronic quick shift. Only 5 500 miles are on this immaculate S1000RR. It has adjustable CRG clutch & brake lever and a rear fender eliminator kit installed. The rear passenger pegs come with it as do 2 keys and the owners manual. This perfect condition 2011 BMW S 1000 RR is offered at $13 799. CA residents will pay sales tax  registration & doc fees. Financing is available and we ship nationwide.    <p>The latest in racing power. With an aluminum bridge  radial brakes  the BMW S1000RR comes standard in Canada with Race ABS  Dynamic Traction Control (DTC) and Gear Shift Assist. Never before is it so easy to keep so much power under control. This is just as true on public roads as it is down on the racetrack. The RR label shows that it is a full-blooded racing bike  even though it can also be ridden with a number plate attached. To top it all off is an engine which is our absolute pride and joy. And our motorsports team agrees wholeheartedly.'


  # case: no make in title and multiple makes in post.
    # solution: regex words from post and search them against model list,
    #           the first make is very likely to be the true one
def getMake(title, desc):
  for make in makesList:                      
    if(re.search(make, title, re.M|re.I)):        # search title for make
       return(make.lower())
  for word in isWord.findall(desc):
    if(re.search(word, makeString, re.M|re.I)):         # search description for make
       return(word.lower())
  return('no make')                                  # if no make found return none
 

 # under assumption year will be between 1980 and 2014, and know it's not the price
 # short year e.g. 88
def getYear(title, desc):
  titleYear = []
  descYear = []
  shortY = False
  for a in number.findall(title):
    if(int(a) > minYear and int(a) < maxYear):        # number within year plausible year ranges
      titleYear.append(int(a))

  if(len(titleYear) == 1):
    return(titleYear[0])
        
  if(len(titleYear) == 0):                 # if empty search for format xx' i.e. 03' Only for title
    for a in shortYear.findall(title):
      y = -1
      if(a[-1:] == "'"):          # last char in string is '
        y = short2fullYear(a[:-1])
      else:
        y = short2fullYear(a)
        
      if(y != 'fail'):
        titleYear.append(y)                # titleYear will only have 1 item in it if here 
        shortY = True

  for a in number.findall(desc):
    if((int(a) > minYear) and (int(a) < maxYear)):        # check desc for year
      descYear.append(int(a))

  if((len(descYear) > 1)):     # if more than 1 year in desc and short year found just use short year
    if(shortY == True):
     return(titleYear[0])
    else:
      print('\r\n\n  no year in title and multiple poss in desc \r\n\n')
      return(descYear[0])
     
  elif((len(descYear) == 1)):  
    if(shortY == True):        # if one short year and desc year found compare to ensure same year
      if(descYear[0] != titleYear[0]):
        print('\r\n\n  title and desc year dont match  %d  %d \r\n\n'%(titleYear[0], descYear[0]))
      return(titleYear[0])
    else:
       return(descYear[0])
  else:                      # if no desc or title year found
    return('no year')
  
       


 # assume: 249 < engine size < 1500,
def getCC(title, desc):
  titleSizes = []
  descSizes = []

  for s in number.findall(title):
    if(int(s) >= minCC and int(s) < maxCC):      # look for all numbers within plausible CC range 
      titleSizes.append(int(s))
      
  if(len(titleSizes) > 1):            # if more than 1 found check if even STUPID CHECK
    for s in titleSizes:
      if(s % 2 == 0):
        return(s)
  elif(len(titleSizes) == 1):
    return(titleSizes[0])  
  else:                           # if no CC found in title
    
    for s in number.findall(desc):
      if(int(s) >= minCC and int(s) < 1950):
        descSizes.append(int(s))

    if(len(descSizes) > 1):
      for s in descSizes:
        if(s % 2 == 0):
          return(s)
    elif(len(descSizes) == 1):
      return(descSizes[0]) 
    else:
      return('no CC')


def getMileage(string):
  for a in miles.findall(string.lower()):
    if(a.isdigit()):
      if(int(a) > 200):    # assuming >200 miles,a has only [0-9]
        return(int(a))
    else:
      x = (addNuminString(a))
      if(x > 100):           
        return(addNuminString(a))   # probably more than 100 miles
      elif(str(a)[-2:-1] == 'k'):   # if xx k miles
        return(int(x) * 1000)
      
  return(-1)      # if not found
  



 # adds all number consecutively from a string no matter separation
def addNuminString(string):
  num = ''
  xxxFormat = False
  if(xxx.match(string) != None):       # has xxx in string 
    xxxFormat = True
  x = nonNum.split(string)
  for m in x:
    if(m.isdigit()):
      num += m
  if(xxxFormat):
    return(int(num)*1000)
  else:
    return(int(num))
      
		


def numPosts(soup):
  x = soup.findAll('b')
  try:
        return(int(x[3].contents[0].split()[1]))
  except:
        return('error: Numposts')



def getKeywords(make, title, desc):
  titleKeys = []
  descKeys = []
  numTerms = 0
  if(make.lower() == 'honda'):      
        l = re.findall(isWord, title)
        for word in l:
          for key in keywords['honda']:       # comb over title for more accuracy
            if(word.lower() == key.lower()):
              titleKeys.append(word.lower())
        if(len(titleKeys) > 3):
          return(titleKeys)
        for key in keywords['honda']:       # comb over title for more accuracy
          if(re.search(key, desc, re.M|re.I)):    # if not found in title search desc, but watch for spam
            descKeys.append(key.lower())
          if(len(descKeys) > 5):                 # if spam in post
            return(titleKeys)
        for key in descKeys:
          if(key not in titleKeys):
            titleKeys.append(key)        
  elif(make.lower() == 'yamaha'):
        l = re.findall(isWord, title)
        for word in l:
          for key in keywords['yamaha']:
            if(word.lower() == key.lower()):
              titleKeys.append(word.lower())
        if(len(titleKeys) > 3):
          return(titleKeys)
        for key in keywords['yamaha']:
          if(re.search(key, desc, re.M|re.I)):    
            descKeys.append(key.lower())
          if(len(descKeys) > 5):                 
            return(titleKeys)
        for key in descKeys:
          if(key.lower() not in titleKeys):
            titleKeys.append(key)        
  elif((make.lower() == 'harley') or (make.lower() == 'davidson') or (make.lower() == 'Harley-Davidson')):
        l = re.findall(isWord, title)
        for word in l:
          for key in keywords['harley']:
            if(word.lower() == key.lower()):
              titleKeys.append(word.lower())
        if(len(titleKeys) > 3):
          return(titleKeys)
        for key in keywords['harley']:
          if(re.search(key, desc, re.M|re.I)):    # if not found in title search desc, but watch for spam
            descKeys.append(key.lower())
          if(len(descKeys) > 5):                 # if spam in post
            return(titleKeys)
        for key in descKeys:
          if(key.lower() not in titleKeys):
            titleKeys.append(key)
  elif(make.lower() == 'kawasaki'):
        l = re.findall(isWord, title)
        for word in l:
          for key in keywords['kawasaki']:
            if(word.lower() == key.lower()):
              titleKeys.append(word.lower())
        if(len(titleKeys) > 3):
          return(titleKeys)
        for key in keywords['kawasaki']:
          if(re.search(key, desc, re.M|re.I)):    # if not found in title search desc, but watch for spam
            descKeys.append(key.lower())
          if(len(descKeys) > 5):                 # if spam in post
            return(titleKeys)
        for key in descKeys:
          if(key.lower() not in titleKeys):
            titleKeys.append(key)
  elif(make.lower() == 'suzuki'):
        l = re.findall(isWord, title)
        for word in l:
          for key in keywords['suzuki']:
            if(word.lower() == key.lower()):
              titleKeys.append(word.lower())
        if(len(titleKeys) > 3):
          return(titleKeys)
        for key in keywords['suzuki']:
          if(re.search(key, desc, re.M|re.I)):    # if not found in title search desc, but watch for spam
            descKeys.append(key.lower())
          if(len(descKeys) > 5):                 # if spam in post
            return(titleKeys)
        for key in descKeys:
          if(key.lower() not in titleKeys):
            titleKeys.append(key)
  else:
        return('no MAKE match')
      
  return(titleKeys)
  


def makeToDocName(make):
  if(make == 'honda'):
    return('honda-kbb.csv')
  elif(make == 'yamaha'):
    return('yamaha-kbb.csv')
  elif(make == 'kawasaki'):
    return('kawasaki-kbb.csv')
  elif(make == 'suzuki'):
    return('suzuki-kbb.csv')
  elif((make.lower() == 'harley') or (make.lower() == 'davidson') or (make.lower() == 'Harley-Davidson')):
    return('hd-kbb.csv')
  else:
    return('make not found')



 # new approach = must match greatest percent of model keywords
 # retreive the specific model and return its two prices in a list
 # return -1 -1 if can't match
def getKBB(make, year, words, CC):
    trade_price = -1
    retail_price = -1
    bike_name = 'none'
    d = dict(bn='make not found', rp='', tp='')
    match_terms = 0
    accuracy = 0.0
    most_accurate = 0.0


    ccMatch = -1
    kbbFilename = makeToDocName(make)
    if(kbbFilename == 'make not found'):
        return(d)

    f = open(kbbFilename, 'rb')
    reader = csv.reader(f)
    reader.next()

#    print'words %s %s      %s'%(year, title, words)
    
    for row in reader:                # look through all rows
        if(year != int(row[1])):       # compare year
            continue
        if(CC != int(row[3])):
            ccMatch = False
            continue
        else:
            ccMatch = True             # not ruling a line out but simply more infor        

        k = getKeywords(make, '', row[2])
        if(len(k) == 0):                # don't divide by zero
            continue
        words_matched = 0

        for key in k:          
          if(key in words):           # if key from post is not in name of bike continue 
            words_matched += 1
 #           print(key)
        accuracy = (words_matched / len(k)) 
 #       print'keys %s, %d, %d, %s'%(k, words_matched, len(words), str(accuracy))

        
        if(accuracy > most_accurate):
          most_accurate = accuracy
          bike_name = row[2]
          trade_price = row[4]
          retail_price = row[5]
#          print 'accuracy:%s   %s: %s, %s,    %s'%(str(accuracy), bike_name, trade_price, retail_price, k)
    f.close()
    
    d['bn'] = str(bike_name)
    d['rp'] = str(retail_price)
    d['tp'] = str(trade_price)
    return(d)



        
        

           




  
