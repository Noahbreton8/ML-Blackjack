import cv2 as cv
from cv2.typing import MatLike
import os
from gameStrategy import tts
from gameStrategy import cardCounting as cc
import modelApi as mapi

card_deck_translation = {
    "Eight of Hearts": '8h',
    "Three of Diamonds": '3d',
    "Three of Clubs": '3c',
    "Nine of Spades": '9s',
    "Four of Diamonds": '4d',
    "Six of Diamonds": '6d',
    "Queen of Clubs": 'qc',
    "Eight of Diamonds": '8d',
    "King of Spades": 'ks',
    "Three of Hearts": '3h',
    "Jack of Diamonds": 'jd',
    "Five of Hearts": '5h',
    "Six of Clubs": '6c',
    "Nine of Hearts": '9h',
    "Four of Clubs": '4c',
    "Jack of Clubs": 'jc',
    "Five of Diamonds": '5d',
    "Seven of Clubs": '7c',
    "King of Hearts": 'kh',
    "Ten of Spades": '10s',
    "Two of Spades": '2s',
    "Nine of Clubs": '9c',
    "Two of Diamonds": '2d',
    "Three of Spades": '3s',
    "Eight of Spades": '8s',
    "Two of Hearts": '2h',
    "Two of Clubs": '2c',
    "Ace of Hearts": 'ah',
    "Queen of Diamonds": 'qd',
    "Jack of Hearts": 'jh',
    "Ten of Hearts": '10h',
    "Seven of Diamonds": '7d',
    "Jack of Spades": 'js',
    "Queen of Spades": 'qs',
    "Four of Hearts": '4h',
    "Six of Hearts": '6h',
    "Seven of Hearts": '7h',
    "Four of Spades": '4s',
    "Ten of Clubs": '10c',
    "Six of Spades": '6s',
    "Eight of Clubs": '8c',
    "Ten of Diamonds": '10d',
    "Five of Clubs": '5c',
    "Ace of Clubs": 'ac',
    "King of Clubs": 'kc',
    "King of Diamonds": 'kd',
    "Nine of Diamonds": '9d',
    "Ace of Spades": 'as',
    "Five of Spades": '5s',
    "Seven of Spades": '7s',
    "Ace of Diamonds": 'ad',
    "Queen of Hearts": 'qh'
}

deck = {
    '2h': 2, '3h': 3, '4h': 4, '5h': 5, '6h': 6, '7h': 7, '8h': 8, '9h': 9, '10h': 10, 'jh': 10, 'qh': 10, 'kh': 10, 'ah': 11,
    '2d': 2, '3d': 3, '4d': 4, '5d': 5, '6d': 6, '7d': 7, '8d': 8, '9d': 9, '10d': 10, 'jd': 10, 'qd': 10, 'kd': 10, 'ad': 11,
    '2c': 2, '3c': 3, '4c': 4, '5c': 5, '6c': 6, '7c': 7, '8c': 8, '9c': 9, '10c': 10, 'jc': 10, 'qc': 10, 'kc': 10, 'ac': 11,
    '2s': 2, '3s': 3, '4s': 4, '5s': 5, '6s': 6, '7s': 7, '8s': 8, '9s': 9, '10s': 10, 'js': 10, 'qs': 10, 'ks': 10, 'as': 11,
}
#Game stats
player_hand = [-1,-1,-1,-1] #-1 -> no card, int -> image is processing, str -> name of card
dealer_hand = [-1,-1,-1,-1]
player_hand_size = 0
dealer_hand_size = 0

#tts
tts = tts.TTS()

# set up video capture
capture = cv.VideoCapture(1) #Might need to change to 0 or 1
WIDTH, HEIGHT = 1280, 1024
capture.set(3,  WIDTH)
capture.set(4, HEIGHT)

if not os.path.exists('images'):
    os.makedirs('images')


def contains_card(frame: MatLike) -> bool:
    WHITE_BOUND = 120
    width = frame.shape[1] #320
    height = frame.shape[0] #341
    matchesRequired = 25000 #max pixel count is around 109,000
    pixelMatches = 0

    for y in range(0, width):
        for x in range(0, height):
            (blue, green, red) = frame[x, y]
            # print(f"RGB: {red}, {green}, {blue}")

            if blue >= WHITE_BOUND and green >= WHITE_BOUND and red >= WHITE_BOUND:
                pixelMatches += 1
            if pixelMatches >= matchesRequired:
                return True
    return False



while (True):
    _, frame = capture.read()

    if cv.waitKey(1) == ord('b'):
        cv.imwrite('./images/bg.png', frame)
    if cv.waitKey(1) == ord('s'):
        cv.imwrite('./images/cam.png', frame)
    if cv.waitKey(1) == ord('n'):
        player_hand_size = 0
        player_hand = [-1,-1,-1,-1] #-1 -> no card, int -> image is processing, str -> name of card
        dealer_hand = [-1,-1,-1,-1]
    if cv.waitKey(1) == ord('l'):
        partitions = []
        for i in range(3):
            for j in range(4):
                partitions.append(frame[int(HEIGHT/3)*i:int(HEIGHT/3)*(i+1), int(WIDTH/4)*j:int(WIDTH/4)*(j+1)])    
        playerHand = []
        dealerHand = []
        for i in range(0, 8):
            if contains_card(partitions[i]):
                img_path = f'./images/partition_{i}.png'
                cv.imwrite(img_path, partitions[i])
                if 4 <= i and i <= 7:
                    playerHand.append(img_path)
                    player_hand[i-4] = len(playerHand)-1
                else:
                    dealerHand.append(img_path)
                    dealer_hand[i] = len(dealer_hand)-1
        #call to api
        playerData, dealerData = mapi.extractModelData(playerHand, dealerHand)
        if player_hand_size <= 4:
            i = 0
            j = 0
            while True:
                if isinstance(player_hand[i], int) and player_hand[i] != -1: #if card needs to be counted and saved, do so
                    card_name = playerHand[player_hand]
                    cc.update_count(card_deck_translation[playerData[player_hand]], deck, 2)#might change to 1
                    player_hand[i] = playerData[j]
                    i += 1
                    j += 1
                    player_hand_size += 1
                elif i >= len(player_hand): #if we have looked at all cards
                    break
                elif player_hand[i] == -1 or isinstance(player_hand[i], str): #no card, or cards already been looked at
                    i += 1
                    continue
        if dealer_hand_size <= 2:
            i = 0
            j = 0
            while True:
                if isinstance(dealer_hand[i], int) and dealer_hand[i] != -1: #if card needs to be counted and saved, do so
                    cc.update_count(card_deck_translation[dealerData[dealer_hand]], deck, 2)#might change to 1
                    dealer_hand[i] = dealerData[j]
                    i += 1
                    j += 1
                    dealer_hand_size += 1
                elif i >= len(dealer_hand): #if we have looked at all cards
                    break
                elif dealer_hand[i] == -1 or isinstance(dealer_hand[i], str): #no card, or cards already been looked at
                    i += 1
                    continue
        #debuging prints, remove later
        print(f"Player Hand ({player_hand_size} cards): -> {player_hand}")
        print(f"Dealer Hand ({dealer_hand_size} cards): -> {dealer_hand}")
        print()

    # alignment guides
    cv.line(frame, (0, int(HEIGHT/3)), (WIDTH, int(HEIGHT/3)), (0, 255, 0), 2)
    for i in range(1, 4):
        cv.line(frame, (int(WIDTH*i/4), 0), (int(WIDTH*i/4), HEIGHT), (0, 255, 0), 2)

    cv.imshow('stream', frame)

    if cv.waitKey(5) == ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()