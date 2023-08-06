import matplotlib.pyplot as plt
import numpy as np


def plot_hist(history):

    epochs = len(history)
    errs, accs = [], []
    for err, acc in history:
        errs.append(err)
        accs.append(acc)

    plt(err, epochs)
