from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, subplots, show

card_map = {
    1: "Ace of Hearts",
    2: "Three of Diamonds",
    3: "Jack of Hearts",
    4: "Seven of Spades",
    5: "Seven of Clubs",
    6: "Queen of Spades",
    7: "Three of Hearts",
    8: "Queen of Clubs",
    9: "King of Diamonds",
    10: "Ace of Spades",
    11: "Ten of Hearts",
    12: "Three of Spades",
    13: "Four of Spades",
    14: "Six of Spades",
    15: "Seven of Hearts",
    16: "Five of Spades",
    17: "Four of Clubs",
    18: "Nine of Spades",
    19: "Ten of Clubs",
    20: "Six of Diamonds",
    21: "Nine of Diamonds",
    22: "Two of Hearts",
    23: "Jack of Clubs",
    24: "Ten of Diamonds",
    25: "Nine of Clubs",
    26: "Nine of Hearts",
    27: "Ace of Diamonds",
    28: "Two of Clubs",
    29: "Five of Diamonds",
    30: "King of Clubs",
    31: "Queen of Diamonds",
    32: "Eight of Hearts",
    33: "Two of Diamonds",
    34: "Six of Hearts",
    35: "Eight of Clubs",
    36: "Eight of Spades",
    37: "Four of Hearts",
    38: "King of Hearts",
    39: "Two of Spades",
    40: "Five of Clubs",
    41: "Jack of Spades",
    42: "Three of Clubs",
    43: "Ten of Spades",
    44: "Five of Hearts",
    45: "Jack of Diamonds",
    46: "Ace of Clubs",
    47: "Seven of Diamonds",
    48: "Queen of Hearts",
    49: "King of Spades",
    50: "Four of Diamonds",
    51: "Eight of Diamonds",
    52: "Six of Clubs"
}

model = load_model("C:/Users/nmb20/UNiversities/Projects/Hackathon/UOttaHack6/ML-Blackjack/ML-Blackjack/goodModel2")

def extractModelData(playerImageList2, dealerImageList2):
    #structure is [(image, id), (image,id) ....]

    test_images_data=[]##numpyarrays
    test_labels_data=[]

    for x in playerImageList2:
        image = x[0]

        # Resize all images to a consistent size
        image = imread(x)
        image = cv2.resize(image, (180, 180))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Normalize pixel values to be between 0 and 1
        image = image / 255.0

        # Expand dimensions to make it compatible with the model
        image = np.expand_dims(image, axis=-1)

        test_images_data.append(image)
        test_labels_data.append(x[1])

    # np.save('C:/Users/nmb20/UNiversities/Projects/Hackathon/UOttaHack6/ML-Blackjack/ML-Blackjack/images_dataAPI.npy', test_images_data)
    # imageData = np.load('C:/Users/nmb20/UNiversities/Projects/Hackathon/UOttaHack6/ML-Blackjack/ML-Blackjack/images_dataAPI.npy', allow_pickle=True)

    np.save('images_dataAPI.npy', test_images_data)
    imageData = np.load('images_dataAPI.npy', allow_pickle=True)

    print(imageData)

    predictions=model.predict(imageData)

    # print(predictions[0])
    playerPrediction = []

    for s in enumerate(predictions[:16]):
        
        biggest = 0
        biggestIndex = -1
        for i in range(53):
            if s[1][i] > biggest:
                biggest = s[1][i]
                biggestIndex = i

        playerPrediction.append(card_map[biggestIndex])

    #DEALER

    test_images_data2 = []
    test_labels_data2 = []

    for x in dealerImageList2:
        image = x[0]

        # Resize all images to a consistent size
        image = imread(x)
        image = cv2.resize(image, (180, 180))

        # Normalize pixel values to be between 0 and 1
        image = image / 255.0

        # Expand dimensions to make it compatible with the model
        image = np.expand_dims(image, axis=-1)

        test_images_data2.append(image)
        test_labels_data2.append(x[1])

    np.save('images_dataAPIDealer.npy', test_images_data2)
    imageDataDealer = np.load('images_dataAPIDealer.npy', allow_pickle=True)

    predictions2=model.predict(imageDataDealer)

    dealerPrediction = []

    for s in enumerate(predictions2[:16]):
        
        biggest = 0
        biggestIndex = -1
        for i in range(53):
            if s[1][i] > biggest:
                biggest = s[1][i]
                biggestIndex = i

        dealerPrediction.append(card_map[biggestIndex])

    return playerPrediction, dealerPrediction