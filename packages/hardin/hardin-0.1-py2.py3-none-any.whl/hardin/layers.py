import numpy as np
from ./tensor import Tensor


class Layer():
    def __init__(self, inputs, neurons):
        w = np.random.uniform(-1, 1, (inputs, neurons))
        b = np.ones((neurons,)) * 0.5
        self.w = Tensor(w)
        self.b = Tensor(b)
        self.y = Tensor(0)

    def forward(self, x):
        self.x = x
        # if not isinstance(x, Tensor()):
        #     raise NameError(f"{x} is not Tensor")
        pass

    def backward(self, y):
        pass

    def calculateDeltaWeights(self):
        pass


class InputLayer(Layer):
    def __init__(self):
        self.name = "InputLayer"

    def forward(self, x):
        self.x = x


class Dense(Layer):
    def __init__(self, inputs, neurons, id=None):
        super().__init__(inputs, neurons)
        self.name = "Dense" + str(id)

    def forward(self, x):
        super().forward(x)
        # print(f"DENSE HERE\n{self.b.elements}\n{self.w.elements} ")
        # print(f"{x.elements.shape}  * {self.w.elements.shape}")
        self.y.elements = np.matmul(x.elements, self.w.elements)
        # print(f"{self.y.elements.shape}  + {self.b.elements.shape}")
        self.y.elements = self.y.elements + self.b.elements

    def backward(self, y):
        self.y.grad = y.grad
        # print(f"{self.name} \n {self.y.grad.shape}, \n{self.w.elements.shape}")
        # print(f"{y.grad.shape}  * {self.w.elements.shape}")
        self.x.grad = np.matmul(y.grad, self.w.elements.T)

    def updateParams(self, lr):
        self.w.grad = np.matmul(self.x.elements.T, self.y.grad)
        self.b.grad = self.y.grad
        self.w.elements = self.w.elements - lr * self.w.grad
        self.b.elements = self.b.elements - lr * self.b.grad


class Activation(Layer):
    def __init__(self, activation):
        self.activation = activation
        self.name = "Activation: " + activation
        self.y = Tensor(0)
        self.x = None

    def forward(self, x):
        super().forward(x)
        if self.activation == 'relu':
            self.y.elements = np.maximum(x.elements, 0)

        elif self.activation == 'sigmoid':
            self.y.elements = 1/(1+np.exp(-x.elements))

        elif self.activation == 'tanh':
            self.y.elements = np.tanh(x.elements)

        return self.y

    def backward(self, y):
        if self.activation == 'relu':
            pass  # Not Implemented

        elif self.activation == 'sigmoid':
            self.y.grad = y.grad

            aux = self.y.elements * (1 - self.y.elements)
            # print(f"{aux.shape}  * {y.grad.shape}")
            self.x.grad = np.multiply(aux, y.grad)

        elif self.activation == 'tanh':
            pass  # Not Implemented

        return self.y

    @staticmethod
    def sigmoid(x):
        return 1/(1+np.exp(-x))


class Softmax(Layer):
    def __init__(self, inputs, neurons):
        self.y = Tensor(np.zeros((inputs, neurons)))
        self.name = "Softmax"

    def forward(self, x):
        super().forward(x)
        self.y.elements = np.exp(x.elements) / \
            np.sum(np.exp(x.elements))

    def backward(self, y):
        super().backward(y)
        # https://stackoverflow.com/questions/54976533/derivative-of-softmax-function-in-python
        self.y.grad = y
        s = self.y.elements.reshape(-1, 1)
        s = np.diagflat(s) - np.dot(s, s.T)
        self.x.grad = np.matmul(self.y.grad, s)

        # print(f"x.grad {self.x.grad.shape}")
        # print(f"y.grad {self.y.grad.shape}")
