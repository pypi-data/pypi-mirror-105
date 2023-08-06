from tensor import Tensor
import numpy as np


class Loss():
    def loss(self, y, y_hat):
        assert y.shape == y_hat.shape.axis

    def acc(self, y, y_hat):
        pass


class CrossEntropy(Loss):
    def __init__(self):
        pass

    def lossCompute(self, y, y_hat):
        # super().loss(y, y_hat)
        N = y.shape[0]
        loss = - np.sum(y * np.log(y_hat.elements)) / N
        acc = self.acc(y, y_hat)
        self.loss_grad = - (y / y_hat.elements)
        return loss, acc

    def acc(self, y, y_hat):
        return np.sum(y == y_hat.elements) / len(y)

    def name(self):
        return "CrossEntropy"


class MeanSquaredError(Loss):

    def loss(self, y, y_hat):
        super().loss(y, y_hat.elements)
        self.grad = - (y / y_hat.elements.elements)
        loss = np.sum(np.square(y - y_hat.elements.elements)) / 2
        return loss, 0

    def name(self):
        return "MeanSquaredError"
