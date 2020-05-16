## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
# import torch.nn.init as I
from torch.nn import init


class MyNetwork(nn.Module):

    def __init__(self):
#         super().__init__()
        
        self.conv1 = nn.Conv2d(1, 32, kernel_size=(4, 4))
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3), stride=1, padding=0)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(2, 2), stride=1, padding=0)
        
        # Max-Pool layer that we will use multiple times
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        # Dropout layers
        self.dropout1 = nn.Dropout(p=0.1)
        self.dropout2 = nn.Dropout(p=0.2)
        
        # Fully connected layers
        self.fc1 = nn.Linear(in_features=6400, out_features=1000)
        self.fc2 = nn.Linear(in_features=1000, out_features=500)
        self.fc3 = nn.Linear(in_features=500, out_features=128)

        # Custom weights initialization
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                m.weight = nn.init.uniform(m.weight, a=0, b=1) # nn.init.uniform_ does not seem to work for in-place change
            elif isinstance(m, nn.Linear):
                m.weight = nn.init.xavier_uniform(m.weight, gain=1)
        
    def forward(self, x):
        ## Conv layers
        x = self.pool(F.elu(self.conv1(x)))
        x = self.pool(F.elu(self.conv2(x)))
        x = self.pool(F.elu(self.conv3(x)))
                
        ## Flatten
        x = x.view(x.size(0), -1) # .view() can be thought as np.reshape
                
        ## Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.dropout1(x)
                
        x = F.relu(self.fc2(x))
        x = self.dropout2(x)
                
        x = self.fc3(x)

        return x


class AlexNet(nn.Module):
    
    def __init__(self):
        super().__init__()
        
        # input of size (1 x 227 x 227)
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=96, kernel_size=(4, 4), stride=4, padding=0) # VALID
        self.conv2 = nn.Conv2d(in_channels=96, out_channels=256, kernel_size=(5, 5), stride=1, padding=2) # SAME
        self.conv3 = nn.Conv2d(in_channels=256, out_channels=384, kernel_size=(3, 3), stride=1, padding=1) # SAME
        self.conv4 = nn.Conv2d(in_channels=384, out_channels=384, kernel_size=(3, 3), stride=1, padding=1) # SAME
        self.conv5 = nn.Conv2d(in_channels=384, out_channels=256, kernel_size=(3, 3), stride=1, padding=1) # SAME
        
        ## Max-Pool layer 
        self.pool = nn.MaxPool2d(kernel_size=3, stride=2)
        
        ## Linear layers
        self.fc1 = nn.Linear(in_features=9216, out_features=4096)
        self.fc2 = nn.Linear(in_features=4096, out_features=4096)
        self.fc3 = nn.Linear(in_features=4096, out_features=136)
        
        ## Dropout 
        self.dropout2 = nn.Dropout(p=0.2)
        self.dropout4 = nn.Dropout(p=0.4)
        self.dropout6 = nn.Dropout(p=0.6)
        
        # Batch Normalization
        self.bn1 = nn.BatchNorm2d(num_features=96, eps=1e-05)
        self.bn2 = nn.BatchNorm2d(num_features=256, eps=1e-05)
        self.bn3 = nn.BatchNorm2d(num_features=384, eps=1e-05)
        self.bn4 = nn.BatchNorm2d(num_features=384, eps=1e-05)
        self.bn5 = nn.BatchNorm2d(num_features=256, eps=1e-05)
        self.bn6 = nn.BatchNorm1d(num_features=4096, eps=1e-05)
        self.bn7 = nn.BatchNorm1d(num_features=4096, eps=1e-05)
        
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                m.weight = nn.init.xavier_uniform(m.weight, gain=1)
            elif isinstance(m, nn.Linear):
                m.weight = nn.init.xavier_uniform(m.weight, gain=1)

    def forward(self, x):
        
        ## Conv layers
        x = F.elu(self.conv1(x))
        x = self.pool(x)
        x = self.dropout2(x)
        
        x = F.elu(self.conv2(x))
        x = self.bn2(x)
        x = self.pool(x)
        
        x = F.elu(self.conv3(x))
        x = self.bn3(x)
        x = self.dropout4(x)
        
        x = F.elu(self.conv4(x))
        x = self.bn4(x)
        x = self.dropout4(x)
        
        x = F.elu(self.conv5(x))
        x = self.bn5(x)
        x = self.pool(x)

        x = x.view(x.size(0), -1) 
        
        x = F.elu(self.fc1(x))
        x = self.bn6(x)
        x = self.dropout6(x)
        
        x = F.elu(self.fc2(x))
        x = self.bn6(x)
        x = self.dropout6(x)
        
        x = self.fc3(x)
    
        return x