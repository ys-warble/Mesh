import numpy as np


class Space:
    def __init__(self, x, y, z):
        self.value = np.zeros((x, y, z))
