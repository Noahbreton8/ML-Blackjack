#keeps track of cards that have been played 
# +1 for 2-6
# 0 for 7-9 
# -1 for 10-Ace

#raise bet as the count goes up

#inputs: current cards on table, currentCount and number of decks in play
#output updated count
def update_count(card:str, deck: dict, deck_count: int):
    if 2 <= deck[card] <= 6:
        return 1 / deck_count
    elif 10 <= deck[card] <= 11:
        return -1 / deck_count
    else:
        return 0