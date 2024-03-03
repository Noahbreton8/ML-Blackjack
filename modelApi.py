from tensorflow.keras.models import load_model
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

model = load_model("C:/Users/nmb20/UNiversities/Projects/Hackathon/UOttaHack6/ML-Blackjack/ML-Blackjack/goodModel2")

def extractModelData(playerImageList2, dealerImageList2):
    #structure is [(image, id), (image,id) ....]

    test_images_data=[]##numpyarrays
    test_labels_data=[]

    for x in playerImageList2:
        #image = x[0]

        # Resize all images to a consistent size
        image = imread(x)
        image = cv2.resize(image, (180, 180))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Normalize pixel values to be between 0 and 1
        image = image / 255.0

        # Expand dimensions to make it compatible with the model
        #image = np.expand_dims(image, axis=-1)

        test_images_data.append(image)

    imageData = np.array(test_images_data)

    # np.save('C:/Users/nmb20/UNiversities/Projects/Hackathon/UOttaHack6/ML-Blackjack/ML-Blackjack/images_dataAPI.npy', test_images_data)
    # imageData = np.load('C:/Users/nmb20/UNiversities/Projects/Hackathon/UOttaHack6/ML-Blackjack/ML-Blackjack/images_dataAPI.npy', allow_pickle=True)

    # np.save('images_dataAPI.npy', test_images_data)
    # imageData = np.load('images_dataAPI.npy', allow_pickle=True)

    print(imageData)

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