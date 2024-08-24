import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)  # Using padding to keep spatial dimensions
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, 3, padding=1)

        #Batch normalization after convolutional layers can stablize and speed up training
        self.bn1 = nn.BatchNorm2d(64)
        self.bn2 = nn.BatchNorm2d(128)
        self.bn3 = nn.BatchNorm2d(256)

        #Prevents overfitting by randomly dopping units during training
        self.dropout = nn.Dropout(0.5)

       # Dummy input to calculate the size of the fully connected layer
        x = torch.randn(1, 3, 128, 128)  # Adjust based on the image size
        self._to_linear = None
        self.convs(x)
        
        self.fc1 = nn.Linear(self._to_linear, 512)
        self.fc2 = nn.Linear(512, 53)

    def convs(self, x):
        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), (2,2)) #Attemp with different activation functions
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), (2,2))
        x = F.max_pool2d(F.relu(self.bn3(self.conv3(x))), (2,2))

        if self._to_linear is None:
            self._to_linear = x.numel() // x.size(0)  # Number of features

        return x

    def forward(self, x):
        x = self.convs(x)
        x = x.reshape(x.size(0), -1)  # Flatten the tensor using reshape
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return F.softmax(x, dim=1)