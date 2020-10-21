#!/usr/bin/python3

import math
import itertools

class FFT(object):
    SEQUENCE=[0, 1, 0, -1]
    def __init__(self):
        with open("16/inputsignal.txt", 'r') as f:
            line = f.readline().strip('\n')

        #@@@ testing
        #line = "19617804207202209144916044189917"

        self.input_sig= list(int(i) for i in line)

    def calc_element(self, index, input_sig_cpy):
        # find the multiplier: 0, 1, 0, -1 * (index + 1) - 1st element
        repeats = math.ceil((len(input_sig_cpy) + 1.0)/((index + 1) * 4))

        # times by calculated repeat number to make sufficiently long
        m = self.SEQUENCE * repeats
        # repeat each element
        m = list(itertools.chain.from_iterable(itertools.repeat(x, (index + 1)) for x in m))
        # truncate the list
        multiplier = m[1:len(input_sig_cpy) + 1]

        # pairwise multiple each element of the input array
        return abs(sum([a * b for a, b in zip(input_sig_cpy, multiplier)])) % 10

    def phase_increment(self):
        input_sig_cpy = self.input_sig[:]

        for i in range(len(self.input_sig)):
            self.input_sig[i] = self.calc_element(i, input_sig_cpy)

    def phase_traverse(self, num):
        for i in range(num):
            self.phase_increment()

    def print_first_eight(self):
        print("".join(str(i) for i in self.input_sig[0:8]))

fft = FFT()
fft.phase_traverse(100)
fft.print_first_eight()

