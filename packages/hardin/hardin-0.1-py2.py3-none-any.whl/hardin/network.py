import numpy as np
from tensor import Tensor
from loss import CrossEntropy
from loss import MeanSquaredError


class Network():
    def __init__(self, inputLayer, layers=None, loss=None):
        self.input = inputLayer
        self.layers = layers
        self.loss = loss if loss else MeanSquaredError()
        self.deltaParams = None

    def forward(self, x):
        y = None
        for i, layer in enumerate(self.layers):
            # print(f"\t Step :{i}, layer: {layer.name}")
            if i == 0:
                layer.forward(x)
                y = layer.y
            else:
                layer.forward(y)
                y = layer.y
            # print(f"y.shape = {y.elements.shape}")
        return y

    def backward(self, loss_grad):

        x = None
        reversed_layers = self.layers[::-1]
        for i, layer in enumerate(reversed_layers):
            # print(f"\t Step :{i}, layer: {layer.name}")
            if i == 0:
                layer.backward(loss_grad)
                x = layer.x
            else:
                layer.backward(x)
                x = layer.x

            # print(f"x ={x.grad.shape}")
            # print(x.grad)

    def updateParams(self, lr):
        # print("Parameters Updating")
        for i, layer in enumerate(self.layers):
            # print(f"\t Step :{i}, layer: {layer.name}")
            try:
                layer.updateParams(lr)
            except:
                pass
