'''
Please load the winequality-white dataset and use a dense fully connected network to predict the quality of a wine.
Experiment with various options such as activation functions, learning rate, number of layers, number of hidden nodes per layer,
optimization algorithms, and loss functions. For each option plot the loss function over several epochs.
Submit your notebook and present your best results.
'''

import torch
import pandas
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import torch.nn as nn
import torch.optim as optim

df = pandas.read_csv('winequality-white.csv', sep=';')

df_train, df_test = train_test_split(df, test_size=0.2)

inputs = torch.tensor(df_train.iloc[:,0:11].values,  dtype=torch.float32)
labels = torch.tensor(df_train.iloc[:,11:12].values, dtype=torch.float32)

inputs_test = torch.tensor(df_test.iloc[:,0:11].values, dtype=torch.float32)
labels_test = torch.tensor(df_test.iloc[:,11:12].values, dtype=torch.float32)

min_max_scaler = preprocessing.MinMaxScaler()

##fitting NUR(!!!!) mit input

min_max_scaler.fit(inputs)
#skaliert alle werte auf uniforme größen
inputs_scaled = min_max_scaler.transform(inputs)
#numpy nimmt array, deswegen muss wieder tensor
inputs_scaled = torch.tensor(inputs_scaled)

inputs_test_scaled = min_max_scaler.transform(inputs_test)
inputs_test_scaled = torch.tensor(inputs_test_scaled)





criterion = nn.MSELoss()

class Net(nn.Module):  # https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module
    def __init__(self): #heißt, dass passiert bei intitilisierung
        super(Net, self).__init__()
        self.layer_1 = nn.Linear(11, 1500)
        self.layer_2 = nn.Linear(1500,1500)
        self.output_layer = nn.Linear(1500, 1)

    def forward(self, x):
        x = torch.relu(self.layer_1(x))
        x = torch.sigmoid(self.layer_2(x))
        x = self.output_layer(x)
        return x

net = Net()

#lr: produkt von learning rate und ermitteltem gradient wird als update für nächste epoche an weight benutzt
#wenn lr zu groß können sprünge zu groß sein, wenn zu klein ist training ggf. langsam
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

#outputs = net(inputs)


loss_vals = list()

#loss = criterion(outputs, labels)
#print(loss.item())

#loss.backward()
#optimizer.step()



for epoch in range(150):
    #forward pass
    #muss passieren, weil pytorch gradienten akkumuliert
    optimizer.zero_grad()
    #nimmt skalierte inputs und kalkuliert diese mit den intial (zufälligen) weights
    outputs = net(inputs_scaled.float())
    #berechne fehler zwischen kalkuliertem und tatsächlichen
    loss = criterion(outputs, labels.float())
    #backwardpropagation --> hier wird berechnet, welche veränderung an weight was bewirkt (gradient of loss function)
    #-->positiver gradient: vergrößert loss; loss soll mininiert werden, ergo: bei positivim gradient wird weight kleiner
    # theoretisch will ich also alle gradients = 0
    loss.backward()
    #weights werden mit berechneten gradienten geupdated
    # new weight = old weight - learning rate * gradient
    optimizer.step()
    loss_vals.append(loss.item())

outputs_test = net(inputs_test_scaled.float())
loss_test = criterion(outputs_test, labels_test.float())

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


plt.plot(range(50,150), loss_vals[50:150])
plt.show()

print(loss_vals[149])
print(loss_test)
