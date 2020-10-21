#!/usr/bin/python3

import math
import itertools

class FFT(object):
    SEQUENCE=[0, 1, 0, -1]
    def __init__(self):
        with open("16/inputsignal.txt", 'r') as f:
            line = f.readline().strip('\n')

        #@@@ testing
        #line = "03036732577212944063491565474664"

        self.input_sig= list(map(int, line))

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

    def part_1_phase_traverse(self, num):
        for i in range(num):
            self.phase_increment()
        print("".join(str(i) for i in self.input_sig[0:8]))

    def part_2_phase_traverse(self, num):
        offset = int("".join(map(str, self.input_sig[0:7])))

        if (offset < len(self.input_sig) * 10000 / 2):
            print("This method will not work: assumes offset is greater than "
                  "halfway through so that subsequent multipliers are 1")
            return

        self.input_sig *= 10000
        self.input_sig = self.input_sig[offset:]
        for i in range(100):
            # Each entry changed to sum of itself and later indices in list.
            # Traverse backwards summing so O(n)
            for index in range(len(self.input_sig)- 2, -1, -1):
                self.input_sig[index] = abs(self.input_sig[index] + self.input_sig[index + 1]) % 10

        print("".join(str(i) for i in self.input_sig[0:8]))

print("PART 1:")
fft = FFT()
fft.part_1_phase_traverse(100)

print("PART 2:")
fft=FFT()
fft.part_2_phase_traverse(100)




