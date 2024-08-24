import cv2
import numpy as np
import torch
from maps import card_map
from model import Net

net = Net()
MODEL_PATH = "model.pth"
net.load_state_dict(torch.load(MODEL_PATH))
net.eval()

IMG_SIZE = 128

#Determines if the process will be run on GPU or CPU
if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print("running on gpu")
else:
    device = torch.device("cpu")
    print("running on cpu")

net.to(device)

def extractModelData(playerImageList, dealerImageList):

    playerPrediction = []
    dealerPrediction = []

    #PLAYER
    for x in playerImageList:
        image_tensor = preprocess_image(x)

        image_tensor = image_tensor.to(device)

        #Make the prediction
        with torch.no_grad():  #Disable gradient computation so model doesn't get updated
            output = net(image_tensor)
        
        #Gets the most likely value from the list of 53 items
        predicted_class = torch.argmax(output, dim=1).item()
        card_name = card_map[predicted_class]
        playerPrediction.append(card_name)


    #DEALER
    for x in dealerImageList:
        image_tensor = preprocess_image(x)

        image_tensor = image_tensor.to(device)

        # Make the prediction
        with torch.no_grad():  #Disable gradient computation so model doesn't get updated
            output = net(image_tensor)
        
        #Gets the most likely value from the list of 53 items
        predicted_class = torch.argmax(output, dim=1).item()
        card_name = card_map[predicted_class]
        dealerPrediction.append(card_name)

    return playerPrediction, dealerPrediction

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    # Resize the image
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    
    # Convert the image to a numpy array and normalize it
    img = np.array(img, dtype=np.float32) / 255.0
    
    # Transpose the dimensions to match the model's input (channels, height, width)
    img = np.transpose(img, (2, 0, 1))
    
    # Convert the numpy array to a tensor
    img_tensor = torch.tensor(img, dtype=torch.float32)
    
    # Add a batch dimension (since the model expects a batch of images)
    img_tensor = img_tensor.unsqueeze(0)
    
    return img_tensor