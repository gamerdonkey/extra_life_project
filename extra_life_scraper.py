from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import sqlite3
import time
import string

def processDonations(donations, numToProcess):
   for i in range(0, numToProcess):
      donation = donations[i]
      strongTag = donation.strong
      smallTag = donation.small
      emTag = donation.em

      strongTagString = donation.strong.string.strip()
      smallTagString = donation.small.string.strip()
      if emTag is not None:
         emTagString = donation.em.string.strip()
      else:
         emTagString = ''

      parseDonationData(strongTagString, smallTagString, emTagString, cursor)

def parseDonationData(strongString, smallString, emString, dbCursor):
   gameTitlePattern = re.compile(r"vote (.+)", re.IGNORECASE)
   donorNameAndAmountPattern = re.compile(r"(.+) donated..(.+)")
   
   gameTitleMatch = gameTitlePattern.search(emString)
   donorNameAndAmountMatch = donorNameAndAmountPattern.search(strongString)

   if gameTitleMatch:
      gameTitle = gameTitleMatch.group(1)
   else:
      gameTitle = None
   
   donorName = donorNameAndAmountMatch.group(1)
   amount = float(donorNameAndAmountMatch.group(2))
   date = time.strptime(smallString,"%m/%d/%Y")
   formattedDate = time.strftime("%Y-%m-%d", date)
     
   params = (formattedDate, donorName, amount, gameTitle)
      
   dbCursor.execute('INSERT INTO donation_votes VALUES (?,?,?,?)', params)

baseUrl = "http://www.extra-life.org/index.cfm"
urlOptions = "fuseaction=donordrive.participant&participantID=51042"
#urlOptions = "fuseaction=donorDrive.participant&participantID=47568"
html = urlopen(string.join([baseUrl,urlOptions],"?")).read()
soup = BeautifulSoup(html, "lxml")
donations = soup.find("table").find_all("div", "pull-left")

dbConnection = sqlite3.connect("extra_life.db")
cursor = dbConnection.cursor()

cursor.execute('select count(*) from donation_votes')
voteCount = cursor.fetchone()[0]

print len(donations)
print voteCount

if len(donations) > voteCount:
   difference = (len(donations)-voteCount)
   processDonations(donations, difference)

dbConnection.commit()
dbConnection.close()
