import unittest
import numpy as np

class FIR_filter:

    def __init__(self, coeffiients):
        self.bufferlength = 500
        self.buffer = list(np.zeros(self.bufferlength - 1))
        self.coeffiients = coeffiients
        self.output = 0

    def dofilter(self, v):
        self.buffer.append(v)
        self.output = 0
        for i in range(self.bufferlength):
            self.output += self.coeffiients[i] * self.buffer[(self.bufferlength - 1) - i]
        self.buffer = self.buffer[1:]
        return self.output

if __name__ == '__main__':
    unittest.main()


