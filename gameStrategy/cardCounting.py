#keeps track of cards that have been played 
# +1 for 2-6
# 0 for 7-9 
# -1 for 10-Ace

#raise bet as the count goes up

#inputs: current cards on table, currentCount and number of decks in play
#output updated count
def updateCount(cardList, currentCount, deckNumber, deck):
    for card in cardList:
        if (6>=deck[card]>=2):
            currentCount += 1
        elif(11>=deck[card]>=10):
            currentCount -= 1
        else:
            print ("card not in deck")
    return currentCount