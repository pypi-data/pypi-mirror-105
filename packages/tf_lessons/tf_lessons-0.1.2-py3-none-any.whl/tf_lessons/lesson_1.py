import numpy as np
from tensorflow import keras

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)


class Neuron:
    def __init__(self):
        self.model = keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
        self.model.compile(optimizer="sgd", loss="mean_squared_error")
        self.fit = self.model.fit(xs, ys, epochs=500, verbose=0)

    def predict(self, input):
        return self.model.predict(input)

    @property
    def paramas_for_fit(self):
        return self.fit.params
