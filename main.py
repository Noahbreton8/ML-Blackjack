import cv2 as cv
from cv2.typing import MatLike
import os
from gameStrategy import tts
from gameStrategy import cardCounting as cc
from gameStrategy import decisionmaking
import modelApi as mapi
from maps import card_deck_translation, deck, wordToMap

#Game stats
player_hand = [-1,-1,-1,-1] #-1 -> no card, int -> image is processing, str -> name of card
dealer_hand = [-1,-1,-1,-1]
player_hand_size = 0
dealer_hand_size = 0
currentCount = 0
#tts and openCV
tts = tts.TTS()
font = cv.FONT_HERSHEY_SIMPLEX 
text_font_scale = 1
text_color = (0,255,0)
text_thickness = 2

# set up video capture
capture = cv.VideoCapture(0) #Might need to change to 0 or 1
WIDTH, HEIGHT = 1280, 1024
capture.set(3,  WIDTH)
capture.set(4, HEIGHT)

if not os.path.exists('images'):
    os.makedirs('images')


#Determines if a card exists within subsection of entire frame by comparing white space
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

    # if cv.waitKey(1) == ord('b'):
    #     cv.imwrite('./images/bg.png', frame)
    # if cv.waitKey(1) == ord('s'):
    #     cv.imwrite('./images/cam.png', frame)
    if cv.waitKey(1) == ord('n'):
        player_hand_size = 0
        player_hand = [-1,-1,-1,-1] #-1 -> no card, int -> image is processing, str -> name of card
        dealer_hand = [-1,-1,-1,-1]
    read_loud = False
    if cv.waitKey(1) == ord('l'):
        read_loud = True
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
                    dealer_hand[i] = len(dealerHand)-1
        #call to api
        playerData, dealerData = mapi.extractModelData(playerHand, dealerHand)

        print("Here is player and dealer data")
        print(playerData, dealerData)

        if player_hand_size <= 3:
            i = 0
            j = 0
            while True:
                if i >= len(player_hand): #if we have looked at all cards
                        break
                elif isinstance(player_hand[i], int):
                    if player_hand[i] != -1: #if card needs to be counted and saved, do so
                        card_name = playerData[player_hand[i]]
                        currentCount += cc.update_count(card_deck_translation[card_name], deck, 2)#might change to 1
                        # newcc = cc.update_count(card_deck_translation[playerData[player_hand]], deck, 2)#might change to 1<- might need this instead
                        # if newcc != currentCount: <- might need this
                        #     currentCount += newcc
                        player_hand[i] = playerData[player_hand[i]]
                        i += 1
                        j += 1
                        player_hand_size += 1
                    elif player_hand[i] == -1: #no card, or cards already been looked at
                        i += 1
                        continue
                elif isinstance(player_hand[i], str): #no card, or cards already been looked at
                    i += 1
                    continue
        if dealer_hand_size <= 2:
            i = 0
            j = 0
            while True:
                if i >= len(dealer_hand): #if we have looked at all cards
                        break
                elif isinstance(dealer_hand[i], int):
                    if dealer_hand[i] != -1: #if card needs to be counted and saved, do so
                        card_name = dealerData[dealer_hand[i]]
                        currentCount += cc.update_count(card_deck_translation[card_name], deck, 2)#might change to 1
                        # newcc = cc.update_count(card_deck_translation[playerData[player_hand]], deck, 2)#might change to 1<- might need this instead
                        # if newcc != currentCount: <- might need this
                        #     currentCount += newcc
                        dealer_hand[i] = dealerData[dealer_hand[i]]
                        i += 1
                        j += 1
                        dealer_hand_size += 1
                    elif dealer_hand[i] == -1: #no card, or cards already been looked at
                        i += 1
                        continue
                elif isinstance(dealerData[i], str): #no card, or cards already been looked at
                    i += 1
                    continue
        #debuging prints, remove later
        print(f"Dealer Hand ({dealer_hand_size} cards): -> {dealer_hand}")
        print(f"Player Hand ({player_hand_size} cards): -> {player_hand}")
        print()

    # alignment guides
    cv.line(frame, (0, int(HEIGHT/3)), (WIDTH, int(HEIGHT/3)), (0, 255, 0), 2)
    for i in range(1, 4):
        cv.line(frame, (int(WIDTH*i/4), 0), (int(WIDTH*i/4), HEIGHT), (0, 255, 0), 2)

    if currentCount > 0:
        cv.putText(frame, f"Card Count Score: +{currentCount}", (15, 40), font, text_font_scale, text_color, text_thickness, cv.LINE_AA)
    else:
        cv.putText(frame, f"Card Count Score: {currentCount}", (15, 40), font, text_font_scale, text_color, text_thickness, cv.LINE_AA)

    cards_in_dealer = {}
    cards_in_player = {}
    for i in range(0, 4):
        if dealer_hand[i] != -1:
            cv.putText(frame, f"{dealer_hand[i]}", (60 + int(WIDTH/4-10) * i, int(HEIGHT/3-10)), font, text_font_scale, text_color, text_thickness, cv.LINE_AA)
            # if dealer_hand[i] not in cards_in_dealer:
            #     cards_in_dealer.update({dealer_hand[i]: 1})
            # else:
            #     cards_in_dealer.update({cards_in_dealer.get(dealer_hand[i]): 1})
    for i in range(0, 4):
        if player_hand[i] != -1:
            cv.putText(frame, f"{player_hand[i]}", (60 + int(WIDTH/4-10) * i, int(HEIGHT*2/3)-10), font, text_font_scale, text_color, text_thickness, cv.LINE_AA)
            # if dealer_hand[i] not in cards_in_dealer:
            #     cards_in_player.update({player_hand[i]: 1})
            # else:
            #     cards_in_player.update({cards_in_player.get(player_hand[i]): 1})

    cv.imshow('stream', frame)

    if read_loud:
        for i in range(0, 4):
            if dealer_hand[i] != -1:
                tts.speak(f"dealer has a {dealer_hand[i]}")

        for i in range(0, 4):
            if player_hand[i] != -1:
                tts.speak(f"player has a {player_hand[i]}")


    # for card in cards_in_dealer.keys():
    #     tts.speak(f"dealer has {cards_in_dealer[card]} {card}")
    # for card in cards_in_player.keys():
    #     tts.speak(f"player has has {cards_in_player[card]} {card}")
    

    if cv.waitKey(1) == ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()