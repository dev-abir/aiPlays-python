from __future__ import annotations

import copy
import numpy as np


class NeuralNet:
    def __init__(self, dimensions: list):
        self.layers = []
        self.biases = []
        # TODO: do a study on these output activation funcs...
        self.output = self._activation()
        for i in range(len(dimensions) - 1):
            shape = (dimensions[i], dimensions[i + 1])
            std = np.sqrt(2 / sum(shape))  # TODO: why std dev is calculated like this...?
            layer = np.random.normal(0, std, shape)
            bias = np.random.normal(0, std, (1, dimensions[i + 1]))
            self.layers.append(layer)
            self.biases.append(bias)

    def _activation(self, output: str = 'linear'):
        if output == 'sigmoid':
            return lambda X: (1 / (1 + np.exp(-X)))
        else:
            return lambda X: X  # linear output

    def mutate(self, stdev=0.03):
        # TODO: change stdev...?
        for i in range(len(self.layers)):
            self.layers[i] += np.random.normal(0, stdev, self.layers[i].shape)
            self.biases[i] += np.random.normal(0, stdev, self.biases[i].shape)

    def mate(self, other: NeuralNet) -> NeuralNet:
        # TODO: remove the checks...?
        if not len(self.layers) == len(other.layers):
            raise ValueError('Both parents must have same number of layers')
        if not all(self.layers[x].shape == other.layers[x].shape for x in range(len(self.layers))):
            raise ValueError('Both parents must have same shape')

        child = copy.deepcopy(self)
        for i in range(len(child.layers)):
            pass_on = np.random.rand(1, child.layers[i].shape[1]) < 0.5
            child.layers[i] = pass_on * self.layers[i] + ~pass_on * other.layers[i]
            child.biases[i] = pass_on * self.biases[i] + ~pass_on * other.biases[i]
            child.mutate()
        return child

    def get_choice(self, X: np.ndarray) -> float:
        # TODO: remove the checks...?
        if not X.ndim == 2:
            raise ValueError(f'Input has {X.ndim} dimensions, expected 2')
        if not X.shape[1] == self.layers[0].shape[0]:
            raise ValueError(f'Input has {X.shape[1]} features, expected {self.layers[0].shape[0]}')
        for index, (layer, bias) in enumerate(zip(self.layers, self.biases)):
            X = X @ layer + np.ones((X.shape[0], 1)) @ bias
            if index == len(self.layers) - 1:
                X = self.output(X)  # output activation
            else:
                X = np.clip(X, 0, np.inf)  # ReLU

        return X[0][0]
        # return np.argmax(X, axis=1).reshape((-1, 1))  # TODO: is it reshaping from -1 to +1?
