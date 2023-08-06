import numpy as np
from tensor import Tensor


class SGDTrainer():
    def __init__(self, batchSize=1, learningRate=.5, amountEpochs=20, Shuffle=True):
        self.bs = batchSize
        self.lr = learningRate
        self.epochs = amountEpochs
        self.shuffle = Shuffle
        self.net = None

        self.updateMechanism = "SGDFlavor"

    def optimize(self, network, data):

        self.net = network
        history = []
        epochs = self.epochs
        # epochs = 2
        x = Tensor(data['x'])
        y = np.array(data['y'])
        print(y)
        for i in range(epochs):
            # print("Forward")
            y_hat = self.net.forward(x)
            print(y_hat.elements)
            # print(f"Loss \n {y} \n {y_hat.elements}")
            err, acc = self.net.loss.lossCompute(y=y, y_hat=y_hat)

            history.append((err, acc))
            # print("Backward")
            self.net.backward(self.net.loss.loss_grad)
            self.net.updateParams(self.lr)
            print(f"Epoch: {i + 1}/{epochs}, accuracy = {acc}%, loss= {err}")

        return history
