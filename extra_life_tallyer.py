import sqlite3
import re

class Game:
   def __init__(self, amount, prettyTitle):
      self.amount = amount
      self.prettyTitle = prettyTitle

dbConnection = sqlite3.connect("extra_life.db")
cursor = dbConnection.cursor()

cursor.execute('select sum(amount) from donation_votes')
totalDonationAmount = cursor.fetchone()[0]

gameDict = {'total':Game(totalDonationAmount, 'Total'), 'voteTotal':Game(0, 'Vote Total')}

cursor.execute('select * from donation_votes where gameTitle is not null order by date asc, amount desc')

for row in cursor.fetchall():
   gameTitleKey = re.sub('[^a-z0-9]+', '', row[3].lower())

   gameDict['voteTotal'].amount = gameDict['voteTotal'].amount + row[2]   

   if(gameTitleKey not in gameDict):
      gameDict[gameTitleKey] = Game(row[2], row[3])
   else:
      gameDict[gameTitleKey].amount = gameDict[gameTitleKey].amount + row[2]

cursor.execute('DELETE FROM tallied_votes')

for key in gameDict.keys():
   params = (key, gameDict[key].prettyTitle, gameDict[key].amount)
   cursor.execute('INSERT INTO tallied_votes VALUES (?,?,?)', params)

dbConnection.commit()
dbConnection.close()
