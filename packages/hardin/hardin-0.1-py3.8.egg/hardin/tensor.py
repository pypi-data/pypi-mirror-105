import numpy as np


class Shape():
    def __init__(self, axis):
        self.axis = axis
        self.volume = np.prod(axis)

    def shape(self):
        return self.axis


class Tensor():
    def __init__(self, x):
        self.elements = np.array(x)
        self.shape = Shape(self.elements.shape)
        self.grad = None
        self.delta = None

    def shape(self):
        return self.shape.shape()
