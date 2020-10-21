#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT

class ASCII(object):
    def __init__(self):
        self.p = Popen(['python3', '-u', './9.py', '17/asciicomp.txt'],
                       stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.coords = {}

    def readandplot(self):
        coord = (0,0)
        while True:
            char = self.p.stdout.readline().decode('utf-8').strip('\n')

            if char == '':
                break
            else:
                char = int(char)

            if char == 10:
                print("")
                coord = (0, coord[1] + 1)
            else:
                self.coords[coord] = chr(char)
                print(chr(char), end="")
                coord = (coord[0] + 1, coord[1])

    def find_alignment_parameters(self):
        # search for any coords of intersections
        sum = 0
        for coord in self.coords.keys():
            if self.coords[coord] == "#":
                neighbours =  [(coord[0], coord[1] + 1),
                               (coord[0], coord[1] - 1),
                               (coord[0] + 1, coord[1]),
                               (coord[0] - 1, coord[1])]

                if all(n in self.coords and self.coords[n] == "#" for n in neighbours):
                    sum += coord[0] * coord[1]

        print(f"found alignment parameters, sum = {sum}")

bot = ASCII()
bot.readandplot()
bot.find_alignment_parameters()