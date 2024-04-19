# https://pytorch.org/docs/stable/index.html
# --> torch.nn --> Containers --> Module
import torch
import torch.nn as nn
import torch.optim as optim


class Net(nn.Module):  # https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module
                        # basisklasse für neuronale netzwerke

    def __init__(self): #heißt, dass passiert bei intitilisierung
        super(Net, self).__init__()
        #hier mit mehreren layern...
        self.layer_1 = nn.Linear(3, 3)  # https://pytorch.org/docs/stable/generated/torch.nn.Linear.html#torch.nn.Linear
                        # linear, 3 input, 3 output (ist abhängig von den nodes im nächsten layer) werte
                        # nn.Linear ist standardlayer in pytorch
        self.layer_2 = nn.Linear(3, 3)
        self.output_layer = nn.Linear(3, 2)
                        #weil nur 2 outputs
    def forward(self, x):
        x = torch.relu(self.layer_1(x))
        x = torch.sigmoid(self.layer_2(x))
        x = self.output_layer(x)
        return x


net = Net()

# The weights of the neural network have been initialized:
print(net.layer_1.weight)
print(net.layer_2.weight)
print(net.output_layer.weight)

# https://pytorch.org/docs/stable/tensors.html
inputs = torch.randn(20, 3)
labels = torch.randn(20, 2)

# https://pytorch.org/docs/stable/nn.html#loss-functions
criterion = nn.MSELoss()

# https://pytorch.org/docs/stable/optim.html
#hier ist autograd default =true
# sgd ist optimierungs algorithmus, net.parameters sagt aus, dass nur gewichte optimiert werden
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# Forward step is executed in Net class.
outputs = net(inputs)
print(outputs)
print(labels)

# Loss is calculated.
#weil autograd = true, kann hier rückwärts kalkuliert werden
loss = criterion(outputs, labels)
print(loss.item())

# If any input Tensor of an operation has 'requires_grad=True', the computation will be tracked
# (e.g. the initialized weight matrices above).
# See also here: https://pytorch.org/tutorials/beginner/former_torchies/autograd_tutorial.html
print(loss.grad_fn.next_functions)

# Backward propagation of error:
loss.backward()

# Weights are updated:
#optimizer wird genutzt, um 1. epoche durchzuführen
optimizer.step()
print(net.layer_1.weight)
print(net.layer_2.weight)

# Loop over dataset multiple times. Pytorch accumulates gradients per default, so it is required to
# zero the parameter gradients before each iteration with 'zero_grad()' function.
loss_vals = list()
for epoch in range(100):
    #forward pass
    optimizer.zero_grad()
    outputs = net(inputs)
    #berechne fehler
    loss = criterion(outputs, labels)
    #backward
    loss.backward()
    #
    optimizer.step()
    loss_vals.append(loss.item())

# Plot loss:
import matplotlib.pyplot as plt

plt.plot(range(100), loss_vals)
plt.show()
