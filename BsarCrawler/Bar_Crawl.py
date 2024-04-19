'''
Use various sequential and non-sequential networks in order to predict your alcohol level from your cell phone's
accelerometer. Use the BarCrawl dataset. Experiment with various options such as activation functions, number of layers,
number of hidden nodes per layer, optimization algorithms, loss functions, sequence length, batch size and type of
target variable.

For each option plot the loss function over several epochs. Submit your notebook and present your best results.
'''

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import bc_data as bc



class Net(nn.Module):

    def __init__(self, input_size):
        super(Net, self).__init__()
        self.layer_1 = torch.nn.RNN(input_size,20, batch_first=True)
        self.layer_2 = torch.nn.RNN(20,15, batch_first=True)
        self.layer_3 = nn.Linear(15,1)



    def forward(self, x):
        out, hidden = self.layer_1(x) # returns tuple consisting of output and sequence
        out, hidden = self.layer_2(out)
        output = torch.relu(self.layer_3(hidden))
        return output

seq_size = 100
batch_size = 64
input_size = 3

# https://pytorch.org/docs/stable/data.html
dataset = bc.BarCrawlDataset(seq_size)
loader = DataLoader(dataset=dataset, batch_size=batch_size)

net = Net(input_size)

criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for epoch in range(50):

    running_loss = 0

    for inputs, labels in loader:
        optimizer.zero_grad()
        outputs = net(inputs.float())
        loss = criterion(torch.squeeze(outputs), labels.float())
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print('Epoch loss: ' + str(running_loss / len(loader)))
