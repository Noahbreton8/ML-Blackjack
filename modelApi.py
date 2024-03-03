from tensorflow.keras.models import load_model #might need to be from tensorflow.python.keras.models import load_model
import tensorflow as tf
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, subplots, show

card_map = {
    0: "Eight of Hearts",
    1: "Three of Diamonds",
    2: "Three of Clubs",
    3: "Nine of Spades",
    4: "Four of Diamonds",
    5: "Six of Diamonds",
    6: "Queen of Clubs",
    7: "Eight of Diamonds",
    8: "King of Spades",
    9: "Three of Hearts",
    10: "Jack of Diamonds",
    11: "Five of Hearts",
    12: "Six of Clubs",
    13: "Nine of Hearts",
    14: "Four of Clubs",
    15: "Jack of Clubs",
    16: "Five of Diamonds",
    17: "Seven of Clubs",
    18: "King of Hearts",
    19: "Ten of Spades",
    20: "Two of Spades",
    21: "Nine of Clubs",
    22: "Two of Diamonds",
    23: "Three of Spades",
    24: "Eight of Spades",
    25: "Two of Hearts",
    26: "Two of Clubs",
    27: "Ace of Hearts",
    28: "Queen of Diamonds",
    29: "Jack of Hearts",
    30: "Ten of Hearts",
    31: "Seven of Diamonds",
    32: "Jack of Spades",
    33: "Queen of Spades",
    34: "Four of Hearts",
    35: "Six of Hearts",
    36: "Seven of Hearts",
    37: "Four of Spades",
    38: "Ten of Clubs",
    39: "Six of Spades",
    40: "Eight of Clubs",
    41: "Ten of Diamonds",
    42: "Five of Clubs",
    43: "Ace of Clubs",
    44: "King of Clubs",
    45: "King of Diamonds",
    46: "Nine of Diamonds",
    47: "Ace of Spades",
    48: "Five of Spades",
    49: "Seven of Spades",
    50: "Ace of Diamonds",
    51: "Queen of Hearts"
}

model = load_model("./goodModeLastModel22")

def extractModelData(playerImageList, dealerImageList):

    test_images_data=[]##numpyarrays
    test_images_data2=[]

    for x in playerImageList:
        #image = x[0]

        # Resize all images to a consistent size
        image = imread(x)
        image = cv2.resize(image, (180, 180))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Normalize pixel values to be between 0 and 1
        image = image / 255.0

        test_images_data.append(image)

    imageData = np.array(test_images_data)

    # print(imageData)

    predictions=model.predict(imageData)

    # print(predictions[0])
    playerPrediction = []

    for s in predictions:
        biggest = 0
        biggestIndex = -1
        for i in range(52):
            if s[i] > biggest:
                biggest = s[i]
                biggestIndex = i

        playerPrediction.append(card_map[biggestIndex])

    #DEALER
        
    for x in dealerImageList:
        #image = x[0]

        # Resize all images to a consistent size
        image = imread(x)
        image = cv2.resize(image, (180, 180))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Normalize pixel values to be between 0 and 1
        image = image / 255.0

        test_images_data2.append(image)

    imageData2 = np.array(test_images_data2)

    print(imageData)

    predictions2=model.predict(imageData2)

    # print(predictions[0])
    dealerPrediction = []

    for s in predictions2:
        biggest = 0
        biggestIndex = -1
        for i in range(52):
            if s[i] > biggest:
                biggest = s[i]
                biggestIndex = i

        dealerPrediction.append(card_map[biggestIndex])

    return playerPrediction, dealerPrediction